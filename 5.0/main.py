#!/usr/bin/env python3
import sys
import numpy as np
import math
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

N = 50


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def draw_egg(vertex_array):

    for u in range(0, N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for v in range(0, N):
            glColor3f(vertex_array[u, v, 3], vertex_array[u, v, 4], vertex_array[u, v, 5])
            glVertex3f(vertex_array[u, v, 0], vertex_array[u, v, 1], vertex_array[u, v, 2])
            glColor3f(vertex_array[u+1, v, 3], vertex_array[u+1, v, 4], vertex_array[u+1, v, 5])
            glVertex3f(vertex_array[u+1, v, 0], vertex_array[u+1, v, 1], vertex_array[u+1, v, 2])
        glEnd()


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def render(time, vertex_array, seed):
    random.seed(seed)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()
    spin(time * 180 / math.pi)
    draw_egg(vertex_array)
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    vertex_array = np.zeros(shape=[N, N, 6], dtype=float)
    u_array = np.linspace(start=0, stop=1, num=N, dtype=float)
    v_array = np.linspace(start=0, stop=1, num=N, dtype=float)
    vertex_array = calculate_egg_values(u_array, v_array, vertex_array)
    seed = random.random()
    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime(), vertex_array, seed)
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


def calculate_egg_values(u_array, v_array, vertex_array):
    for u in range(0, N):
        for v in range(0, N):
            x = (-90 * pow(u_array[u], 5) + 225 * pow(u_array[u], 4) - 270 * pow(u_array[u], 3) +
                 180 * pow(u_array[u], 2) - 45 * u_array[u]) * math.cos(math.pi * v_array[v])
            y = 160 * pow(u_array[u], 4) - 320 * pow(u_array[u], 3) + 160 * pow(u_array[u], 2) - 5
            z = (-90 * pow(u_array[u], 5) + 225 * pow(u_array[u], 4) - 270 * pow(u_array[u], 3)
                 + 180 * pow(u_array[u], 2) - 45 * u_array[u]) * math.sin(math.pi * v_array[v])
            vertex_array[u][v][0] = x
            vertex_array[u][v][1] = y
            vertex_array[u][v][2] = z
            vertex_array[u][v][3] = random.random()
            vertex_array[u][v][4] = random.random()
            vertex_array[u][v][5] = random.random()

        for i in range(0, N):
            for j in range(0, 2):
                vertex_array[i][N - 1 - j][3] = vertex_array[N - 1 - i][j][3]
                vertex_array[i][N - 1 - j][4] = vertex_array[N - 1 - i][j][4]
                vertex_array[i][N - 1 - j][5] = vertex_array[N - 1 - i][j][5]

    return vertex_array


if __name__ == '__main__':
    main()
