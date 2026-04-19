from PySide6.QtGui import QPaintEvent, QPainter, QResizeEvent, QSurfaceFormat, Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QSizePolicy
from OpenGL import GL
import numpy as np

from piano_roll.view.notes.grid_renderer import GridRenderer
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class NotesView(QOpenGLWidget):
    N = 1000

    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__()
        self.viewport = viewport

        rng = np.random.default_rng(0)
        self._pos = rng.uniform(0, 500, size=(self.N, 2)).astype(np.float32)
        self._size = rng.uniform(6, 80, size=(self.N, 2)).astype(np.float32)

        self._instance_data = np.empty((self.N, 4), dtype=np.float32)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def initializeGL(self):
        # set bg color
        GL.glClearColor(0.08, 0.08, 0.10, 1.0)

        self.program = None  # link program here
        self.loc_viewport = None  # uViewport location here

        # Our unit quad
        quad = np.array(
            [
                0.0,
                0.0,
                1.0,
                0.0,
                0.0,
                1.0,
                0.0,
                1.0,
                1.0,
                0.0,
                1.0,
                1.0,
            ],
            dtype=np.float32,
        )

        # Create and bind VAO
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        # Quad VBO setup
        self.quad_VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.quad_VBO)

        return super().initializeGL()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.viewport.set_viewport_size((self.size().width(), self.size().height()))

        return super().resizeEvent(event)
