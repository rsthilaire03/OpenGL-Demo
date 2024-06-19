import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from PyQt5.QtCore import QTimer

class AtomViewer(QOpenGLWidget):
    def __init__(self):
        super(AtomViewer, self).__init__()
        self.shell_rotations = [
            {'angle': 0, 'axis': (0, 0, 1), 'speed': 1},   # K-shell
            {'angle': 0, 'axis': (0, 1, 0), 'speed': 0.8}, # L-shell
            {'angle': 0, 'axis': (0, 0, 1), 'speed': 0.6}, # M-shell
            {'angle': 0, 'axis': (1, 1, 0), 'speed': 0.4}, # N-shell
            {'angle': 0, 'axis': (0, 1, 1), 'speed': 0.2}, # O-shell
        ]
        self.electron_rotations = [
            {'angle': 0, 'speed_factor': 10},  # K-shell
            {'angle': 0, 'speed_factor': 15},  # L-shell
            {'angle': 0, 'speed_factor': 20},  # M-shell
            {'angle': 0, 'speed_factor': 25},  # N-shell
            {'angle': 0, 'speed_factor': 30},  # O-shell
        ]

    def initializeGL(self):
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)

        for shell, electron_rotation in zip(self.shell_rotations, self.electron_rotations):
            shell['angle'] += shell['speed']
            electron_rotation['angle'] += shell['speed'] * electron_rotation['speed_factor']

        self.draw_atom()

    def draw_atom(self):
        # Draw nucleus
        glColor3f(1.0, 0.0, 0.0)
        self.draw_sphere(0, 0, 0, 0.5)

        # Draw electron shells
        for shell, electron_rotation in zip(self.shell_rotations, self.electron_rotations):
            self.draw_electron_shell(shell, electron_rotation)

    def draw_sphere(self, x, y, z, radius):
        glPushMatrix()
        glTranslatef(x, y, z)
        quad = gluNewQuadric()
        gluSphere(quad, radius, 32, 32)
        gluDeleteQuadric(quad)
        glPopMatrix()

    def draw_electron_shell(self, shell, electron_rotation):
        angle = shell['angle']
        axis_x, axis_y, axis_z = shell['axis']
        glPushMatrix()
        glRotatef(angle, axis_x, axis_y, axis_z)
        glColor3f(0.0, 0.0, 1.0)
        radius = 1.5 + self.get_electron_radius(shell)
        for i in range(2 * int(np.pi * (1.5 + self.get_electron_radius(shell)))):
            electron_angle = electron_rotation['angle'] + i * (360 / (2 * int(np.pi * (1.5 + self.get_electron_radius(shell)))))
            x = radius * np.cos(np.radians(electron_angle))
            y = radius * np.sin(np.radians(electron_angle))
            self.draw_sphere(x, y, 0, 0.05)
        glPopMatrix()

    def get_electron_radius(self, shell):
        return shell['speed'] * 1.5  # Adjust the coefficient for realistic speed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AtomViewer()
    window.resize(800, 600)

    # Timer to update the rotation
    timer = QTimer()
    timer.timeout.connect(window.update)
    timer.start(16)  # Approximately 60 frames per second

    window.show()
    sys.exit(app.exec_())
