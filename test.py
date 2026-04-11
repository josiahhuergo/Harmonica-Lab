"""
Piano roll rendering demo: PySide6 QOpenGLWidget + moderngl on macOS.

Architecture (MVVM-ish):

    Model:      notes (immutable song data, numpy structured array)
    ViewModel:  NotesViewModel { notes, selected, cached visible_indices }
    View:       PianoRollView (scroll/zoom state) + RectRenderer (GL)

    NotesViewModel.build_rects(view) ──► rects ──► RectRenderer

Layers:
    PianoRollView   -- scroll/zoom state + viewport size (dumb data)
    NotesViewModel  -- selection state, visibility cache, rect building.
                       Culling is cached; invalidated on view/notes change,
                       NOT on selection change.
    RectBatch       -- one GPU instance buffer + VAO. update() refills from numpy.
    RectRenderer    -- owns the GL program + unit quad. draw(batch, viewport).
    PianoRollWidget -- wires viewmodel + view + renderer together,
                       handles mouse drag (scroll) and wheel (zoom),
                       calls viewmodel.invalidate_visible() when the view
                       transforms.

Controls:
    drag           - scroll
    wheel          - zoom horizontally (time)
    shift + wheel  - zoom vertically (pitch lane height)

Run:
    pip install pyside6 moderngl numpy
    python instanced_rects.py
"""

import sys
from dataclasses import dataclass
import numpy as np
import moderngl
from PySide6.QtCore import Qt, QTimer, QElapsedTimer, QPoint
from PySide6.QtGui import QSurfaceFormat, QMouseEvent, QWheelEvent
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication


# Float32s per rect in the instance buffer:
# pos.xy(2) + size.xy(2) + fill.rgb(3) + border.rgb(3) = 10
# Border thickness is a global uniform, not per-rect.
RECT_STRIDE = 10


# ---------------------------------------------------------------------------
# Domain: notes and view state
# ---------------------------------------------------------------------------

# A "song" is a structured numpy array with these fields. Easy to read
# (notes['pitch']) and trivially vectorizable.
NOTE_DTYPE = np.dtype(
    [
        ("pitch", np.float32),  # MIDI note number, 0..127 (60 = middle C)
        ("onset", np.float32),  # start time in beats
        ("duration", np.float32),  # length in beats
    ]
)


@dataclass
class PianoRollView:
    """Scroll + zoom state, plus viewport size in logical pixels."""

    scroll_x: float = 0.0  # beat at the left edge of the view
    scroll_y: float = 84.0  # MIDI pitch at the TOP edge of the view (high pitch)
    zoom_x: float = 40.0  # pixels per beat
    zoom_y: float = 12.0  # pixels per semitone (lane height)
    width: float = 800.0  # viewport width in logical pixels
    height: float = 600.0  # viewport height in logical pixels


# 12 pleasant colors, one per pitch class (C, C#, D, ...). Same C across octaves
# always gets the same color, which is useful for spotting key/scale patterns.
_PITCH_CLASS_COLORS = np.array(
    [
        [0.91, 0.30, 0.35],  # C
        [0.95, 0.55, 0.25],  # C#
        [0.97, 0.78, 0.20],  # D
        [0.80, 0.88, 0.25],  # D#
        [0.50, 0.85, 0.35],  # E
        [0.25, 0.82, 0.55],  # F
        [0.20, 0.78, 0.80],  # F#
        [0.25, 0.60, 0.92],  # G
        [0.40, 0.40, 0.95],  # G#
        [0.60, 0.35, 0.92],  # A
        [0.82, 0.35, 0.85],  # A#
        [0.92, 0.35, 0.62],  # B
    ],
    dtype=np.float32,
)


_SELECTION_STROKE = np.array([1.0, 0.95, 0.2], dtype=np.float32)  # bright yellow


class NotesViewModel:
    """UI state that sits between the song (notes) and the view (rects).

    Holds:
      - notes:              the song itself (reference, not a copy)
      - selected:           boolean mask, True where a note is selected
      - _visible_indices:   cached integer array of which notes are currently
                            in view. Invalidated on view/notes change, NOT on
                            selection change. Recomputed lazily.

    The widget owns one of these, mutates its selection directly, and calls
    invalidate_visible() whenever scroll/zoom/resize happens.
    """

    def __init__(self, notes: np.ndarray):
        self.notes = notes
        self.selected = np.zeros(len(notes), dtype=bool)
        self._visible_indices: np.ndarray | None = None
        self._visible_dirty = True

    # ---- selection mutation ----

    def select(self, indices) -> None:
        self.selected[indices] = True

    def deselect(self, indices) -> None:
        self.selected[indices] = False

    def toggle(self, indices) -> None:
        self.selected[indices] = ~self.selected[indices]

    def clear_selection(self) -> None:
        self.selected.fill(False)

    # ---- visibility cache ----

    def invalidate_visible(self) -> None:
        """Mark the visible set as stale. Call this when the view changes
        (scroll/zoom/resize) or when notes are added/removed/edited."""
        self._visible_dirty = True

    def _recompute_visible(self, view: PianoRollView) -> None:
        """Run culling against the current view, write self._visible_indices."""
        notes = self.notes
        if len(notes) == 0:
            self._visible_indices = np.empty(0, dtype=np.int64)
            self._visible_dirty = False
            return

        # Same transformation as before, but only to determine visibility -
        # we don't keep the transformed coords, we'll recompute them per frame
        # in build_rects (cheap; only for the visible subset).
        x = (notes["onset"] - view.scroll_x) * view.zoom_x
        w = notes["duration"] * view.zoom_x
        y = (view.scroll_y - notes["pitch"]) * view.zoom_y
        h = view.zoom_y  # scalar; every note is one lane tall

        visible = (x + w > 0) & (x < view.width) & (y + h > 0) & (y < view.height)
        self._visible_indices = np.nonzero(visible)[0]
        self._visible_dirty = False

    # ---- rect building ----

    def build_rects(self, view: PianoRollView) -> np.ndarray:
        """Produce the (M, 10) float32 rect array for the current view.

        Uses the cached visible set (recomputing it if dirty). Selection state
        is applied here: selected notes get a bright yellow stroke instead of
        the default darkened-fill stroke.
        """
        if self._visible_dirty:
            self._recompute_visible(view)

        idx = self._visible_indices
        m = idx.size
        if m == 0:
            return np.zeros((0, RECT_STRIDE), dtype=np.float32)

        notes = self.notes
        # Pull out just the visible notes' fields. These are small arrays of
        # length m, not len(notes), so this is cheap even for big songs.
        v_pitch = notes["pitch"][idx]
        v_onset = notes["onset"][idx]
        v_duration = notes["duration"][idx]
        v_selected = self.selected[idx]

        # Per-frame transform (cheap: only touches visible notes).
        x = (v_onset - view.scroll_x) * view.zoom_x
        w = v_duration * view.zoom_x
        y = (view.scroll_y - v_pitch) * view.zoom_y

        rects = np.empty((m, RECT_STRIDE), dtype=np.float32)
        rects[:, 0] = x
        rects[:, 1] = y
        rects[:, 2] = w
        rects[:, 3] = view.zoom_y  # broadcasts scalar into column

        # Fill color by pitch class.
        pitch_class = v_pitch.astype(np.int32) % 12
        fill = _PITCH_CLASS_COLORS[pitch_class]
        rects[:, 4:7] = fill

        # Default stroke = darkened fill, then overwrite with yellow for
        # selected notes. np.where would also work, but a mask assignment is
        # clearer and avoids building an intermediate array.
        rects[:, 7:10] = fill * 0.35
        rects[v_selected, 7:10] = _SELECTION_STROKE

        return rects

    # ---- read-only accessors ----

    @property
    def visible_count(self) -> int:
        """How many notes are currently in view (0 if not yet computed)."""
        return 0 if self._visible_indices is None else self._visible_indices.size


# ---------------------------------------------------------------------------
# Renderer + Batch (the GL layer; no domain knowledge)
# ---------------------------------------------------------------------------

_VERTEX_SHADER = """
#version 330 core

in vec2 in_corner;       // unit quad corner [0,1], per vertex
in vec2 in_pos;          // top-left in pixels, per instance
in vec2 in_size;         // width, height in pixels, per instance
in vec3 in_fill;         // per instance
in vec3 in_border;       // per instance

uniform vec2 u_viewport; // widget size in logical pixels

out vec2 v_uv;           // [0,1] across the rect
out vec2 v_size;         // rect size in pixels (passed to FS for edge math)
out vec3 v_fill;
out vec3 v_border;

void main() {
    vec2 pixel = in_pos + in_corner * in_size;
    vec2 clip = (pixel / u_viewport) * 2.0 - 1.0;
    clip.y = -clip.y;  // (0,0) is top-left
    gl_Position = vec4(clip, 0.0, 1.0);

    v_uv     = in_corner;
    v_size   = in_size;
    v_fill   = in_fill;
    v_border = in_border;
}
"""

_FRAGMENT_SHADER = """
#version 330 core

in vec2 v_uv;
in vec2 v_size;
in vec3 v_fill;
in vec3 v_border;

uniform float u_border_px;  // border thickness in pixels

out vec4 frag_color;

void main() {
    // Distance in pixels from this fragment to the nearest edge of the rect.
    // v_uv * v_size = our position in pixels from the top-left of the rect.
    // (1 - v_uv) * v_size = distance from the bottom-right.
    vec2 from_tl = v_uv * v_size;
    vec2 from_br = (1.0 - v_uv) * v_size;
    float edge_dist = min(min(from_tl.x, from_tl.y), min(from_br.x, from_br.y));

    // Inside the border band -> border color, otherwise fill.
    vec3 rgb = (edge_dist < u_border_px) ? v_border : v_fill;
    frag_color = vec4(rgb, 1.0);
}
"""


class RectBatch:
    """A GPU buffer holding up to `capacity` rects. Created by RectRenderer."""

    def __init__(self, ctx, program, quad_vbo, capacity: int):
        self._ctx = ctx
        self._capacity = capacity
        self._count = 0
        self._vbo = ctx.buffer(reserve=capacity * RECT_STRIDE * 4, dynamic=True)
        self._vao = ctx.vertex_array(
            program,
            [
                (quad_vbo, "2f", "in_corner"),
                (
                    self._vbo,
                    "2f 2f 3f 3f /i",
                    "in_pos",
                    "in_size",
                    "in_fill",
                    "in_border",
                ),
            ],
        )

    @property
    def count(self) -> int:
        return self._count

    @property
    def capacity(self) -> int:
        return self._capacity

    def update(self, rects: np.ndarray) -> None:
        """Upload `rects` (shape (N, 7) float32) to the GPU."""
        if rects.dtype != np.float32:
            raise TypeError(f"rects must be float32, got {rects.dtype}")
        if rects.ndim != 2 or rects.shape[1] != RECT_STRIDE:
            raise ValueError(
                f"rects must have shape (N, {RECT_STRIDE}), got {rects.shape}"
            )
        n = rects.shape[0]
        if n > self._capacity:
            raise ValueError(f"batch capacity is {self._capacity}, got {n} rects")
        if n > 0:
            self._vbo.write(np.ascontiguousarray(rects).tobytes())
        self._count = n


class RectRenderer:
    """Draws rectangles via instanced quads. Create batches, then draw them."""

    def __init__(self, ctx: moderngl.Context):
        self._ctx = ctx
        self._program = ctx.program(
            vertex_shader=_VERTEX_SHADER,
            fragment_shader=_FRAGMENT_SHADER,
        )
        # Unit quad shared by all batches: (0,0)(1,0)(0,1)(1,1) as TRIANGLE_STRIP.
        quad = np.array([0, 0, 1, 0, 0, 1, 1, 1], dtype=np.float32)
        self._quad_vbo = ctx.buffer(quad.tobytes())

    def create_batch(self, capacity: int) -> RectBatch:
        return RectBatch(self._ctx, self._program, self._quad_vbo, capacity)

    def draw(
        self, batch: RectBatch, viewport: tuple[float, float], border_px: float = 1.0
    ) -> None:
        if batch.count == 0:
            return
        self._program["u_viewport"].value = viewport
        self._program["u_border_px"].value = float(border_px)
        batch._vao.render(mode=moderngl.TRIANGLE_STRIP, instances=batch.count)


# ---------------------------------------------------------------------------
# Demo: build a fake "song" and show it in a piano roll widget
# ---------------------------------------------------------------------------


def make_random_song(
    num_notes: int = 5000, num_beats: float = 200.0, seed: int = 42
) -> np.ndarray:
    """Generate a random pile of notes for the demo."""
    rng = np.random.default_rng(seed)
    notes = np.empty(num_notes, dtype=NOTE_DTYPE)
    notes["pitch"] = rng.integers(36, 96, size=num_notes).astype(np.float32)
    notes["onset"] = rng.uniform(0, num_beats, size=num_notes).astype(np.float32)
    notes["duration"] = rng.uniform(0.25, 2.0, size=num_notes).astype(np.float32)
    return notes


class PianoRollWidget(QOpenGLWidget):
    def __init__(self, notes: np.ndarray, parent=None):
        super().__init__(parent)
        self.viewmodel = NotesViewModel(notes)
        self.view = PianoRollView()

        # Demo: pre-select every note whose pitch is a multiple of 7, so you
        # can see the selection stroke in action without needing click logic.
        demo_sel = np.nonzero(notes["pitch"].astype(np.int32) % 7 == 0)[0]
        self.viewmodel.select(demo_sel)

        self.ctx: moderngl.Context | None = None
        self.renderer: RectRenderer | None = None
        self.batch: RectBatch | None = None

        # Mouse drag state
        self._drag_last: QPoint | None = None

        # FPS counter
        self.elapsed = QElapsedTimer()
        self.elapsed.start()
        self.last_ns = self.elapsed.nsecsElapsed()
        self.frame_count = 0
        self.fps_accum = 0.0

        # Repaint on a timer so the FPS counter has something to count.
        # In a "real" piano roll you'd only call update() in response to user input.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(0)

    # ---- GL lifecycle ----

    def initializeGL(self):
        self.ctx = moderngl.create_context()
        print(
            f"GL: {self.ctx.info['GL_VENDOR']} / "
            f"{self.ctx.info['GL_RENDERER']} / {self.ctx.info['GL_VERSION']}"
        )

        self.renderer = RectRenderer(self.ctx)
        # Capacity = total notes. In a real app you'd size this for the max
        # possible visible count, not the whole song.
        self.batch = self.renderer.create_batch(capacity=len(self.viewmodel.notes))

    def resizeGL(self, w: int, h: int):
        dpr = self.devicePixelRatio()
        if self.ctx is not None:
            self.ctx.viewport = (0, 0, int(w * dpr), int(h * dpr))
        self.view.width = float(w)
        self.view.height = float(h)
        self.viewmodel.invalidate_visible()

    def paintGL(self):
        if self.ctx is None:
            return

        # macOS QOpenGLWidget FBO gotcha: bind Qt's current FBO each frame.
        self.ctx.detect_framebuffer(self.defaultFramebufferObject()).use()

        # ---- timing ----
        now_ns = self.elapsed.nsecsElapsed()
        dt = (now_ns - self.last_ns) / 1e9
        self.last_ns = now_ns
        self.frame_count += 1
        self.fps_accum += dt
        if self.fps_accum >= 1.0:
            print(
                f"{self.frame_count / self.fps_accum:6.1f} fps   "
                f"({self.viewmodel.visible_count} visible / "
                f"{len(self.viewmodel.notes)} total, "
                f"{int(self.viewmodel.selected.sum())} selected)"
            )
            self.frame_count = 0
            self.fps_accum = 0.0

        # ---- the whole render: 3 lines ----
        self.ctx.clear(0.08, 0.08, 0.10)
        rects = self.viewmodel.build_rects(self.view)
        self.batch.update(rects)
        self.renderer.draw(
            self.batch,
            viewport=(self.view.width, self.view.height),
            border_px=1.5,
        )

    # ---- input: scroll + zoom ----

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._drag_last = e.position().toPoint()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._drag_last is None:
            return
        pos = e.position().toPoint()
        dx_pix = pos.x() - self._drag_last.x()
        dy_pix = pos.y() - self._drag_last.y()
        self._drag_last = pos

        # Drag right -> see earlier beats -> scroll_x decreases.
        # Drag down  -> see higher pitches -> scroll_y increases.
        self.view.scroll_x -= dx_pix / self.view.zoom_x
        self.view.scroll_y += dy_pix / self.view.zoom_y
        self.viewmodel.invalidate_visible()
        self.update()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._drag_last = None

    def wheelEvent(self, e: QWheelEvent):
        notches = e.angleDelta().y() / 120.0
        factor = 1.15**notches  # smooth exponential zoom

        if e.modifiers() & Qt.ShiftModifier:
            # Zoom pitch, anchored on the cursor's pitch
            cursor_y = e.position().y()
            pitch_at_cursor = self.view.scroll_y - cursor_y / self.view.zoom_y
            self.view.zoom_y = max(2.0, min(60.0, self.view.zoom_y * factor))
            self.view.scroll_y = pitch_at_cursor + cursor_y / self.view.zoom_y
        else:
            # Zoom time, anchored on the cursor's beat
            cursor_x = e.position().x()
            beat_at_cursor = self.view.scroll_x + cursor_x / self.view.zoom_x
            self.view.zoom_x = max(2.0, min(400.0, self.view.zoom_x * factor))
            self.view.scroll_x = beat_at_cursor - cursor_x / self.view.zoom_x

        self.viewmodel.invalidate_visible()
        self.update()


def main():
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setSwapInterval(1)
    QSurfaceFormat.setDefaultFormat(fmt)

    app = QApplication(sys.argv)

    notes = make_random_song(num_notes=5_000_000, num_beats=2000.0)
    print(f"loaded {len(notes)} notes")

    w = PianoRollWidget(notes)
    w.resize(800, 600)
    w.setWindowTitle("piano roll — drag to scroll, wheel to zoom (shift = pitch)")
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
