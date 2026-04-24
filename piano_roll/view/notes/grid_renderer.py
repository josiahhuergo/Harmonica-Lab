import ctypes

from .gl_utility import link_program
from piano_roll.colors import Colors, rgb
from piano_roll.view.viewport import PianoRollViewport

import numpy as np
from OpenGL import GL

VERT_SRC = """
#version 330 core

layout(location = 0) in vec2 aPos;
out vec2 vUV;

void main() 
{
    vUV = (aPos + 1.0) / 2.0;
    gl_Position = vec4(aPos, 0.0, 1.0);
}
"""

FRAG_SRC = """
#version 330 core

in vec2 vUV;
out vec4 FragColor;

uniform float beat_width;
uniform float key_height;
uniform vec2 viewport;
uniform vec2 scroll;
uniform vec3 bg_black;
uniform vec3 bg_white;
uniform vec3 bg_white_2;
uniform vec3 bar_line;
uniform vec3 beat_line;

void main() 
{
    vec3 color = vec3(1.0);
    FragColor = vec4(bar_color(vUV.x), 1.0);
}
"""


class GridRenderer:
    def __init__(self, viewport: PianoRollViewport):
        self.viewport = viewport

        self.program = link_program(VERT_SRC, FRAG_SRC)

        self.uniforms = {}
        self.uniforms["bg_black"] = GL.glGetUniformLocation(self.program, "bg_black")
        self.uniforms["bg_white"] = GL.glGetUniformLocation(self.program, "bg_white")
        self.uniforms["bg_white_2"] = GL.glGetUniformLocation(
            self.program, "bg_white_2"
        )
        self.uniforms["bar_line"] = GL.glGetUniformLocation(self.program, "bar_line")
        self.uniforms["beat_line"] = GL.glGetUniformLocation(self.program, "beat_line")
        self.uniforms["beat_width"] = GL.glGetUniformLocation(
            self.program, "beat_width"
        )
        self.uniforms["key_height"] = GL.glGetUniformLocation(
            self.program, "key_height"
        )
        self.uniforms["viewport"] = GL.glGetUniformLocation(self.program, "viewport")
        self.uniforms["scroll"] = GL.glGetUniformLocation(self.program, "scroll")

        vertices = np.array(
            [
                -1.0,
                -1.0,  # 0: bottom-left
                1.0,
                -1.0,  # 1: bottom-right
                -1.0,
                1.0,  # 2: top-left
                1.0,
                1.0,  # 3: top-right
            ],
            dtype=np.float32,
        )

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_STATIC_DRAW
        )

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(
            0, 2, GL.GL_FLOAT, GL.GL_FALSE, 2 * 4, ctypes.c_void_p(0)
        )

        GL.glBindVertexArray(0)

    def draw(self):
        print("Drawing!")
        print(f"Scroll x: {self.viewport.scroll_x}")
        print(f"Scroll y: {self.viewport.scroll_y}")
        GL.glUseProgram(self.program)

        GL.glClearColor(*rgb(Colors.BG_BLACK), 1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUniform3f(self.uniforms["bg_black"], *rgb(Colors.BG_BLACK))
        GL.glUniform3f(self.uniforms["bg_white"], *rgb(Colors.BG_WHITE))
        GL.glUniform3f(self.uniforms["bg_white_2"], *rgb(Colors.BG_WHITE_2))
        GL.glUniform3f(self.uniforms["bar_line"], *rgb(Colors.BAR_LINE))
        GL.glUniform3f(self.uniforms["beat_line"], *rgb(Colors.BEAT_LINE))
        GL.glUniform1f(self.uniforms["beat_width"], self.viewport.beat_width)
        GL.glUniform1f(self.uniforms["key_height"], self.viewport.key_height)
        GL.glUniform2f(
            self.uniforms["viewport"], *(float(x) for x in self.viewport.viewport_size)
        )
        GL.glUniform2f(
            self.uniforms["scroll"], self.viewport.scroll_x, self.viewport.scroll_y
        )

        GL.glBindVertexArray(self.vao)
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, 4)
