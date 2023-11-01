import math
import tkinter as tk
import numpy as np
from math import cos, sin, radians


class Cube:
    def __init__(self, canvas):
        self.is_rotate = False
        self.is_move = False
        self.start_point = (0, 0)
        self.z = 0
        self.y = 0
        self.x = 0
        self.canvas = canvas
        self.theta = 0
        self.vertices = []
        self.edges = []

        self.load_data_from_file("cube_data.txt")

    def load_data_from_file(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

            # Обработка строк файла
            for line in lines:
                line = line.strip()
                if line.startswith("v"):
                    # Чтение вершин
                    _, x, y, z = line.split()
                    vertex = (int(x), int(y), int(z))
                    self.vertices.append(vertex)
                elif line.startswith("e"):
                    # Чтение ребер
                    _, v1, v2 = line.split()
                    edge = (int(v1), int(v2))
                    self.edges.append(edge)

    def rotate_x(self, theta):
        return [
            [1, 0, 0],
            [0, math.cos(theta), -math.sin(theta)],
            [0, math.sin(theta), math.cos(theta)],
        ]

    def rotate_y(self, theta):
        return [
            [math.cos(theta), 0, math.sin(theta)],
            [0, 1, 0],
            [-math.sin(theta), 0, math.cos(theta)],
        ]

    def rotate_z(self, theta):
        return [
            [math.cos(theta), -math.sin(theta), 0],
            [math.sin(theta), math.cos(theta), 0],
            [0, 0, 1],
        ]

    def send_values(self, move, rotate, scale, perspective, display):
        self.is_move = move
        self.is_rotate = rotate
        self.is_scale = scale
        self.is_display = display
        self.is_perspective = perspective
        self.x = float(self.x_entry.get()) if self.x_entry.get() else 0.0
        self.y = float(self.y_entry.get()) if self.y_entry.get() else 0.0
        self.z = float(self.z_entry.get()) if self.z_entry.get() else 0.0
        self.theta = math.radians(self.x + self.y + self.z)
        self.draw(self.theta, self.x, self.y, self.z)

    def show_cube_options(self, root, start):
        self.start_point = start
        cube_options_window = tk.Toplevel(root)
        cube_options_window.title("Опции для Куба")

        x_label = tk.Label(cube_options_window, text="x = ")
        x_label.pack(side=tk.LEFT)
        self.x_entry = tk.Entry(cube_options_window)
        self.x_entry.pack(side=tk.LEFT)

        y_label = tk.Label(cube_options_window, text="y = ")
        y_label.pack(side=tk.LEFT)
        self.y_entry = tk.Entry(cube_options_window)
        self.y_entry.pack(side=tk.LEFT)

        z_label = tk.Label(cube_options_window, text="z = ")
        z_label.pack(side=tk.LEFT)
        self.z_entry = tk.Entry(cube_options_window)
        self.z_entry.pack(side=tk.LEFT)

        rotate_button_var = tk.IntVar()
        rotate_button = tk.Checkbutton(cube_options_window, text="Вращение", variable=rotate_button_var)
        rotate_button.pack(side=tk.LEFT)

        resize_button_var = tk.IntVar()
        resize_button = tk.Checkbutton(cube_options_window, text="Перемещение", variable=resize_button_var)
        resize_button.pack(side=tk.LEFT)

        scale_button_var = tk.IntVar()
        scale_button = tk.Checkbutton(cube_options_window, text="Скалирование", variable=scale_button_var)
        scale_button.pack(side=tk.LEFT)

        display_button_var = tk.IntVar()
        display_button = tk.Checkbutton(cube_options_window, text="Отображение", variable=display_button_var)
        display_button.pack(side=tk.LEFT)

        perspective_button_var = tk.IntVar()
        perspective_button = tk.Checkbutton(cube_options_window, text="Перспектива", variable=perspective_button_var)
        perspective_button.pack(side=tk.LEFT)

        send_button = tk.Button(cube_options_window, text="Отправить",
                                command=lambda: self.send_values(resize_button_var.get(),
                                                                 rotate_button_var.get(),
                                                                 scale_button_var.get(),
                                                                 perspective_button_var.get(),
                                                                 display_button_var.get()))
        send_button.pack()

    def rotate_figure(self, theta, x, y, z):
        centered_vertices = [(vertex[0] - 200, vertex[1] - 200, vertex[2] - 200) for vertex in self.vertices]
        rotated_vertices = []
        for vertex in centered_vertices:
            rotated_vertex = np.array(vertex, dtype=np.float64)
            if x != 0:
                rotated_vertex = np.dot(rotated_vertex, self.rotate_x(theta))
            if y != 0:
                rotated_vertex = np.dot(rotated_vertex, self.rotate_y(theta))
            if z != 0:
                rotated_vertex = np.dot(rotated_vertex, self.rotate_z(theta))
            rotated_vertices.append(rotated_vertex.astype(np.int32).tolist())
        self.vertices = [(vertex[0] + 200, vertex[1] + 200, vertex[2] + 200) for vertex in rotated_vertices]
        return self.vertices

    def scale_figure(self, scale_factor):
        scaled_vertices = []
        for vertex in self.vertices:
            scaled_vertex = tuple(coord * scale_factor for coord in vertex)
            scaled_vertices.append(scaled_vertex)
        self.vertices = scaled_vertices
        return scaled_vertices

    def perspective_transform(self, coords, distance):
        transformed_coords = []
        for coord in coords:
            x, y, z = coord
            transformed_x = x * distance / (z + distance)
            transformed_y = y * distance / (z + distance)
            transformed_coords.append((transformed_x, transformed_y))

        return transformed_coords

    def rotate_cube(self, angle, axis):
        # Преобразование угла в радианы
        angle_rad = radians(angle)

        # Перевод координат оси в радианы
        axis_rad = [radians(coord) for coord in axis]

        # Матрица поворота вокруг произвольной оси
        rotation_matrix = [
            [cos(angle_rad) + axis_rad[0] ** 2 * (1 - cos(angle_rad)),
             axis_rad[0] * axis_rad[1] * (1 - cos(angle_rad)) - axis_rad[2] * sin(angle_rad),
             axis_rad[0] * axis_rad[2] * (1 - cos(angle_rad)) + axis_rad[1] * sin(angle_rad)],

            [axis_rad[1] * axis_rad[0] * (1 - cos(angle_rad)) + axis_rad[2] * sin(angle_rad),
             cos(angle_rad) + axis_rad[1] ** 2 * (1 - cos(angle_rad)),
             axis_rad[1] * axis_rad[2] * (1 - cos(angle_rad)) - axis_rad[0] * sin(angle_rad)],

            [axis_rad[2] * axis_rad[0] * (1 - cos(angle_rad)) - axis_rad[1] * sin(angle_rad),
             axis_rad[2] * axis_rad[1] * (1 - cos(angle_rad)) + axis_rad[0] * sin(angle_rad),
             cos(angle_rad) + axis_rad[2] ** 2 * (1 - cos(angle_rad))]
        ]
        rotated_vertices = []
        for vertex in self.vertices:
            rotated_vertex = [0, 0, 0]
            for i in range(3):
                for j in range(3):
                    rotated_vertex[i] += rotation_matrix[i][j] * vertex[j]
            rotated_vertices.append(rotated_vertex)
        return rotated_vertices

    def check_operation(self, theta, x, y, z):
        if self.is_move:
            self.vertices = [(vertex[0] + x, vertex[1] + y, vertex[2] + z) for vertex in self.vertices]
            return self.vertices
        elif self.is_scale:
            scale_factor = 1.0 + theta
            if scale_factor < 0.1:
                scale_factor = 0.1
            vertices = self.scale_figure(scale_factor)
            return vertices
        elif self.is_rotate:
            return self.rotate_figure(theta, x, y, z)
        elif self.is_display:
            self.vertices = self.rotate_cube(theta, [1, 1, 0])
            return self.vertices

    def draw(self, theta, x, y, z):
        self.canvas.delete("all")

        if self.is_perspective:
            vertices = self.perspective_transform(self.vertices, 500)
            for i in range(4):
                self.canvas.create_line(vertices[i][0] + 250, vertices[i][1] + 250, vertices[(i + 1) % 4][0] + 250,
                                        vertices[(i + 1) % 4][1] + 250)
                self.canvas.create_line(vertices[i + 4][0] + 250, vertices[i + 4][1] + 250,
                                        vertices[((i + 1) % 4) + 4][0] + 250,
                                        vertices[((i + 1) % 4) + 4][1] + 250)
                self.canvas.create_line(vertices[i][0] + 250, vertices[i][1] + 250, vertices[i + 4][0] + 250,
                                        vertices[i + 4][1] + 250)

        else:
            vertices = self.check_operation(theta, x, y, z)

            for edge in self.edges:
                x1, y1, _ = vertices[edge[0]]
                x2, y2, _ = vertices[edge[1]]
                self.canvas.create_line(x1 + 250, y1 + 250, x2 + 250, y2 + 250)

        self.canvas.update()
