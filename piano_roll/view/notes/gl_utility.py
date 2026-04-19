from OpenGL import GL


def compile_shader(src, kind):
    s = GL.glCreateShader(kind)
    GL.glShaderSource(s, src)
    GL.glCompileShader(s)
    if not GL.glGetShaderiv(s, GL.GL_COMPILE_STATUS):
        log = GL.glGetShaderInfoLog(s).decode()
        raise RuntimeError(f"Shader compile error:\n{log}")
    return s


def link_program(vs_src, fs_src):
    vs = compile_shader(vs_src, GL.GL_VERTEX_SHADER)
    fs = compile_shader(fs_src, GL.GL_FRAGMENT_SHADER)
    prog = GL.glCreateProgram()
    GL.glAttachShader(prog, vs)
    GL.glAttachShader(prog, fs)
    GL.glLinkProgram(prog)
    if not GL.glGetProgramiv(prog, GL.GL_LINK_STATUS):
        log = GL.glGetProgramInfoLog(prog).decode()
        raise RuntimeError(f"Program link error:\n{log}")
    GL.glDeleteShader(vs)
    GL.glDeleteShader(fs)
    return prog
