from PySide6.QtGui import QPaintEvent, QPainter, QResizeEvent, QSurfaceFormat, Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QSizePolicy
from OpenGL import GL
import numpy as np

from piano_roll.view.notes.grid_renderer import GridRenderer
from piano_roll.view.notes.notes_renderer import NotesRenderer
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class NotesView(QOpenGLWidget):
    N = 1000

    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__()
        self.viewport = viewport

        self._grid_renderer: GridRenderer | None = None
        self._notes_renderer: NotesRenderer | None = None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def initializeGL(self):
        version = GL.glGetString(GL.GL_VERSION)
        if version is not None:
            print(f"[NotesView] GL_VERSION: {version.decode()}")

        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self._grid_renderer = GridRenderer()
        self._notes_renderer = NotesRenderer()

    def paintGL(self):
        GL.glClearColor(0x21 / 255, 0x21 / 255, 0x21 / 255, 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        if self._grid_renderer is not None:
            self._grid_renderer.draw()

        if self._notes_renderer is not None:
            self._notes_renderer.draw()

    def resizeGL(self, w, h):
        GL.glViewport(0, 0, w, h)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.viewport.set_viewport_size((self.size().width(), self.size().height()))
