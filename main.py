import tkinter as tk
import numpy as np
import math
from Cube import Cube

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BG_COLOR = "white"
LINE_COLOR = "black"
DEBUG_COLOR = "lightgray"

# Global variables
selected_algorithm = None
debug_mode = False
start_point = (0, 0)
end_point = (0, 0)
start_velocity = (0, 0)
end_velocity = (0, 0)
file = ""
points = []

def select_algorithm(algorithm):
    global selected_algorithm
    selected_algorithm = algorithm


def load_data(filename):
    with open(filename, 'r') as file_obj:
        data = file_obj.readlines()
    file_obj.close()
    return data


def toggle_debug_mode():
    data = load_data(file_name)

    root = tk.Tk()
    root.title("Data Viewer")

    frame = tk.Frame(root)
    frame.pack()

    for line in data:
        label = tk.Label(frame, text=line.strip())
        label.pack()

    root.mainloop()


def dda_algorithm(canvas):
    global file_name
    file_name = "dda_algorithm_steps.txt"
    x0, y0 = start_point
    x1, y1 = end_point

    x_r = x1 - x0
    y_r = y1 - y0
    length = max(abs(x_r), abs(y_r))

    if length == 0:
        length = 1
    # print(x_r, y_r, length)
    dx = x_r / length
    dy = y_r / length

    x = x0 + 0.5 * np.sign(dx)
    y = y0 + 0.5 * np.sign(dy)

    for i in range(length):
        x = x + dx
        y = y + dy
        canvas.create_rectangle(x, y, x + 1, y + 1, fill=LINE_COLOR)
        with open("dda_algorithm_steps.txt", "a") as file:
            file.write(f"Step {i}, x:{x}, y:{y}, Plot({x},{y})\n")
        file.close()


def bresenham_algorithm(canvas):
    global file_name
    file_name = "bresenham_algorithm_steps.txt"

    x0, y0 = start_point
    x1, y1 = end_point

    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = abs(y1 - y0)
    error = dx // 2
    y_step = 1 if y0 < y1 else -1
    y = y0
    i = 0
    for x in range(x0, x1 + 1):
        i = i + 1
        if steep:
            canvas.create_rectangle(y, x, y + 1, x + 1, fill=LINE_COLOR)
        else:
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=LINE_COLOR)

        error -= dy
        if error < 0:
            y += y_step
            error += dx
        with open("bresenham_algorithm_steps.txt", "a") as file:
            file.write(f"Step {i}, e:{error}, x:{x}, y:{y}, Plot({x},{y})\n")
        file.close()


def wu_algorithm(canvas):
    global file_name
    file_name = "wu_algorithm_steps.txt"
    x1, y1 = start_point
    x2, y2 = end_point

    if x1 == x2 or y1 == y2:
        bresenham_algorithm(canvas)
        return

    x = x1
    y = y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    changeX = 1 if x1 < x2 else -1
    changeY = 1 if y1 < y2 else -1

    canvas.create_rectangle(x, y, x + 1, y + 1)

    i = 1
    if dx >= dy:
        e = dy / dx - 0.5

        while i <= dx:
            if e >= 0:
                y += changeY
                e -= 1
            x += changeX
            e += dy / dx
            a = abs(e)
            fill_color = "#%02x%02x%02x" % (int(a * 255), int(a * 255), int(a * 255))
            if e <= 0:
                canvas.create_rectangle(x - changeX, y - changeY, x - changeX + 1, y - changeY + 1, fill=fill_color,
                                        outline=fill_color)
            else:
                canvas.create_rectangle(x + changeX, y + changeY, x + changeX + 1, y + changeY + 1, fill=fill_color,
                                        outline=fill_color)
            # print(f"Step {i}: e:{e}, x:{x}; y:{y}, a:{a} Plot({x},{y})")
            i += 1
    else:
        e = dx / dy - 0.5
        # print(f"Step 0: x:{x}; y:{y}, e':{e} Plot({x},{y})")
        while i <= dy:
            if e >= 0:
                x += changeX
                e -= 1
            y += changeY
            e += dx / dy
            a = abs(e)
            fill_color = "#%02x%02x%02x" % (int(a * 255), int(a * 255), int(a * 255))
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=fill_color, outline=fill_color)
            if e <= 0:
                canvas.create_rectangle(x - changeX, y - changeY, x - changeX + 1, y - changeY + 1, fill=fill_color,
                                        outline=fill_color)
            else:
                canvas.create_rectangle(x + changeX, y + changeY, x + changeX + 1, y + changeY + 1, fill=fill_color,
                                        outline=fill_color)
            # print(f"Step {i}: e:{e}, x:{x}; y:{y}, a:{a} Plot({x},{y})")
            with open("wu_algorithm_steps.txt", "a") as file:
                file.write(f"Step {i}: e:{e}, x:{x}; y:{y}, a:{a} Plot({x},{y})\n")
            i += 1
        file.close()


def find_radius(x1, y1, x2, y2):
    r1 = x2 - x1
    r2 = y2 - y1
    l_max = max(abs(r1), abs(r2))
    l_min = min(abs(r1), abs(r2))
    return math.sqrt(pow(l_max, 2) + pow(l_min, 2))


def find_a_b(x1, y1, x2, y2):
    a = abs(x2 - x1)
    b = abs(y2 - y1)
    return a, b


def draw_circle(x, origin_x, y, origin_y):
    radius = 1
    canvas.create_oval(x - radius + origin_x, y - radius + origin_y, x + radius + 1 + origin_x,
                       y + radius + 1 + origin_y, fill="black")
    canvas.create_oval(x - radius + origin_x, -y - radius + origin_y, x + radius + 1 + origin_x,
                       -y + radius + 1 + origin_y, fill="black")
    canvas.create_oval(-x - radius + origin_x, y - radius + origin_y, -x + radius + 1 + origin_x,
                       y + radius + 1 + origin_y, fill="black")
    canvas.create_oval(-x - radius + origin_x, -y - radius + origin_y, -x + radius + 1 + origin_x,
                       -y + radius + 1 + origin_y, fill="black")


def circle_algorithm(canvas):
    global file_name
    file_name = "circle_steps.txt"

    x1, y1 = start_point
    x2, y2 = end_point
    y = find_radius(x1, y1, x2, y2)

    x = 0
    radius = y

    limit = y - radius

    delta = 2 - 2 * radius

    # Перемещение начала координат в центр холста
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    origin_x = canvas_width // 2
    origin_y = canvas_height // 2
    i = 0
    with open("circle_steps.txt", "a") as file:
        while y > limit:
            dz = 2 * delta - 2 * x - 1
            if delta > 0 and dz > 0:
                y -= 1
                delta += 1 - 2 * y
                draw_circle(x, origin_x, y, origin_y)
                continue
            d = 2 * delta + 2 * y - 1
            if delta < 0 and d <= 0:
                x += 1
                delta += 1 + 2 * x
                draw_circle(x, origin_x, y, origin_y)
                continue
            x += 1
            y -= 1
            delta += 2 * x - 2 * y + 2
            draw_circle(x, origin_x, y, origin_y)
            i = i + 1
            file.write(
                f"Step {i}, e:{delta},d:{d},,d*{dz} x:{x + origin_x}, y:{y + origin_y}, Plot({x + origin_x},{y + origin_y})\n")
    file.close()


def ellipse_algorithm(canvas):
    global file_name
    file_name = "ellipse_steps.txt"

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    origin_x = canvas_width // 2
    origin_y = canvas_height // 2

    x1, y1 = start_point
    x2, y2 = end_point

    a, b = find_a_b(x1, y1, x2, y2)

    aPow2 = int(math.pow(a, 2))
    bPow2 = int(math.pow(b, 2))
    x = 0
    y = b
    limit = y - b
    delta = aPow2 + bPow2 - 2 * aPow2 * b
    i = 0
    with open("ellipse_steps.txt", "a") as file:
        while y > limit:
            dz = 2 * delta - 2 * x * bPow2 - 1
            if delta > 0 and dz > 0:
                y -= 1
                delta += aPow2 - 2 * y * aPow2
                draw_circle(x, origin_x, y, origin_y)
                continue
            d = 2 * delta + 2 * y * aPow2 - 1
            if delta < 0 and d <= 0:
                x += 1
                delta += bPow2 + 2 * x * bPow2
                draw_circle(x, origin_x, y, origin_y)
                continue
            x += 1
            y -= 1
            delta += bPow2 * (2 * x + 1) + aPow2 * (1 - 2 * y)
            draw_circle(x, origin_x, y, origin_y)
            i += 1
            file.write(
                f"Step {i}, e:{delta},d:{d},,d*{dz} x:{x + origin_x}, y:{y + origin_y}, Plot({x + origin_x},{y + origin_y})\n")
    file.close()

def draw_point(x, y, x1, y1):
    canvas.create_oval(x, y, x1, y1, fill="black")


def calculation_S(x, p, y, direction):
    if direction == "horizontal":
        Sd = (y + 1) ** 2 - 2 * p * (x + 1)
        Sv = (y + 1) ** 2 - 2 * p * x
        Sh = y ** 2 - 2 * p * (x + 1)
        return Sd, Sv, Sh
    elif direction == "vertical":
        Sd = (x + 1) ** 2 - 2 * p * (y + 1)
        Sv = (x + 1) ** 2 - 2 * p * y
        Sh = x ** 2 - 2 * p * (y + 1)
        return Sd, Sv, Sh
    elif direction == "default":
        Sd = y ** 2 - 2 * p * x
        Sv = y ** 2 - 2 * p * x
        Sh = y ** 2 - 2 * p * x
        return Sd, Sv, Sh


def parabola_draw():
    global file_name
    file_name = "parabola_steps.txt"

    # Перемещение начала координат в центр холста

    x0, y0 = start_point
    x1, y1 = end_point

    x, y = 0, 0

    p = abs(y0 - y1)

    Sd, Sv, Sh = calculation_S(x, p, y, 'default')

    i = 0

    if x0 < x1 and y0 < y1:
        draw_point(x0, y0, x0, y0)
        with open("parabola_steps.txt", "a") as file:
            while x + x0 < x1:
                if abs(Sh) - abs(Sv) <= 0:
                    if abs(Sd) - abs(Sh) < 0:
                        x += 1
                    y += 1
                else:
                    if abs(Sv) - abs(Sd) > 0:
                        y += 1
                    x += 1

                draw_point(x + x0, y + y0, x + x0, y + y0)
                draw_point(-x + x0, y + y0, -x + x0, y + y0)

                Sd, Sv, Sh = calculation_S(x, p, y, 'vertical')

                i += 1

                file.write(
                    f"Step {i}, x:{x}, y:{y}, Plot({x + x0},{y + y0})\n")
            file.close()

    elif x0 > x1 and y0 > y1:
        draw_point(x0, y0, x0, y0)
        with open("parabola_steps.txt", "a") as file:
            while -x + x0 > x1:
                if abs(Sh) - abs(Sv) <= 0:
                    if abs(Sd) - abs(Sh) < 0:
                        x += 1
                    y += 1
                else:
                    if abs(Sv) - abs(Sd) > 0:
                        y += 1
                    x += 1
                draw_point(-x + x0, -y + y0, -x + x0, -y + y0)
                draw_point(x + x0, -y + y0, x + x0, -y + y0)

                Sd, Sv, Sh = calculation_S(x, p, y, 'vertical')

                i += 1

                file.write(
                    f"Step {i}, x:{x}, y:{y}, Plot({x + x0},{y + y0})\n")
            file.close()


def hyperbola_draw():
    global file_name
    file_name = "hyperbola_steps.txt"

    x0, y0 = start_point[0], start_point[1]
    x1, y1 = end_point[0], end_point[1]

    x, y = 0, 0

    p = abs(y0 - y1)

    Sd, Sv, Sh = calculation_S(x, p, y, 'default')

    i = 0

    if x0 < x1 and y0 < y1:
        draw_point(x0, y0 - 40, x0, y0 - 40)
        draw_point(x0, y0, x0, y0)
        with open("hyperbola_steps.txt", "a") as file:
            while x + x0 < x1 or -x + x0 > x1:
                if abs(Sh) - abs(Sv) <= 0:
                    if abs(Sd) - abs(Sh) < 0:
                        x += 1
                    y += 1
                else:
                    if abs(Sv) - abs(Sd) > 0:
                        y += 1
                    x += 1

                draw_point(x + x0, y + y0, x + x0, y + y0)
                draw_point(-x + x0, y + y0, -x + x0, y + y0)
                draw_point(-x + x0, -y + y0 - 40, -x + x0, -y + y0 - 40)
                draw_point(x + x0, -y + y0 - 40, x + x0, -y + y0 - 40)

                Sd, Sv, Sh = calculation_S(x, p, y, 'vertical')

                i += 1

                file.write(
                    f"Step {i}, x:{x}, y:{y}, Plot({x + x0},{y + y0})\n")
            file.close()

def hermite_algorithm(canvas):
    P0 = start_velocity
    P1 = start_point
    V0 = end_velocity
    V1 = end_point

    t = 0.0
    step = 0.01

    a = np.matrix([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ])

    b = np.matrix([
        [P0[0], P0[1]],
        [P1[0], P1[1]],
        [V0[0] - P0[0], V0[1] - P0[1]],
        [V1[0] - P1[0], V1[1] - P1[1]]
    ])

    c = np.matmul(a, b)

    while t <= 1:
        tMatrix = np.matrix([t * t * t, t * t, t, 1])
        r = np.matmul(tMatrix, c)
        x = r.item(0)
        y = r.item(1)
        t += step
        canvas.create_rectangle(x, y, x + 1, y + 1, fill=LINE_COLOR)



def bezie_algoritm(canvas):
    P0 = start_velocity
    P1 = start_point
    V0 = end_velocity
    V1 = end_point
    t = 0.0
    step = 0.005

    a = np.matrix([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0]
    ])

    b = np.matrix([
        [P0[0], P0[1]],
        [P1[0], P1[1]],
        [V0[0], V0[1]],
        [V1[0], V1[1]]
    ])

    c = np.matmul(a, b)

    while t <= 1:
        tMatrix = np.matrix([t * t * t, t * t, t, 1])
        r = np.matmul(tMatrix, c)
        x = r.item(0)
        y = r.item(1)
        t += step
        canvas.create_rectangle(x, y, x + 1, y + 1, fill=LINE_COLOR)


def v_spline_algorithm(canvas):
    n = len(points)
    step = 0.01

    a = np.matrix([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 0, 3, 0],
        [1, 4, 1, 0]
    ])

    for i in range(len(points)):
        x, y = points[i]
        canvas.create_oval(x, y, x + 3, y + 3, fill="red")

    i = 1
    while i <= n-3:
        x1, y1 = points[i-1]
        x2, y2 = points[i]
        x3, y3 = points[i + 1]
        x4, y4 = points[i + 2]

        b = np.matrix([
            [x1, y1],
            [x2, y2],
            [x3, y3],
            [x4, y4]
        ])
        c = np.matmul(a, b)
        t = 0.0
        while t <= 1:
            tMatrix = np.matrix([t * t * t, t * t, t, 1])
            r = np.matmul(tMatrix, c)
            x = r.item(0)/6
            y = r.item(1)/6
            t += step
            canvas.create_rectangle(x, y, x + 1, y + 1, fill=LINE_COLOR)
        i += 1


def animate():
    cube.show_cube_options(root, start_point)


def handle_click(event):
    global start_point
    start_point = (event.x, event.y)


def handle_click_3(event):
    global start_velocity, points
    start_velocity = (event.x, event.y)
    points.append(start_velocity)


def handle_release_3(event):
    global end_velocity
    end_velocity = (event.x, event.y)


def handle_release(event):
    global end_point
    end_point = (event.x, event.y)
    points.append(end_point)
    draw_line_based_on_algorithm(canvas)
    points.clear()


def draw_line_based_on_algorithm(canvas):
    if selected_algorithm == "DDA":
        dda_algorithm(canvas)
    elif selected_algorithm == "bresenham":
        bresenham_algorithm(canvas)
    elif selected_algorithm == "Wu":
        wu_algorithm(canvas)
    elif selected_algorithm == "circle":
        circle_algorithm(canvas)
    elif selected_algorithm == "ellipse":
        ellipse_algorithm(canvas)
    elif selected_algorithm == "giperbola":
        hyperbola_draw()
    elif selected_algorithm == "parabola":
        parabola_draw()
    elif selected_algorithm == "hermite":
        hermite_algorithm(canvas)
    elif selected_algorithm == "bezie":
        bezie_algoritm(canvas)
    elif selected_algorithm == "vspline":
        v_spline_algorithm(canvas)
    elif selected_algorithm == "cube":
        animate()


def main():
    global canvas, file, root, cube

    root = tk.Tk()
    root.title("Графический редактор")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
    canvas.pack()

    cube = Cube(canvas)

    delite_button = tk.Button(text="Очистить", command=lambda: canvas.delete("all"))
    delite_button.pack(side=tk.RIGHT)

    dda_button = tk.Button(root, text="ЦДА", command=lambda: select_algorithm("DDA"))
    dda_button.pack(side=tk.LEFT)

    brasenham_button = tk.Button(root, text="Брезенхэм", command=lambda: select_algorithm("bresenham"))
    brasenham_button.pack(side=tk.LEFT)

    wu_button = tk.Button(root, text="Ву", command=lambda: select_algorithm("Wu"))
    wu_button.pack(side=tk.LEFT)

    circle_button = tk.Button(root, text="Окружность", command=lambda: select_algorithm("circle"))
    circle_button.pack(side=tk.LEFT)

    ellipse_button = tk.Button(root, text="Эллипс", command=lambda: select_algorithm("ellipse"))
    ellipse_button.pack(side=tk.LEFT)

    debug_button = tk.Button(root, text="Гипербола", command=lambda: select_algorithm("giperbola"))
    debug_button.pack(side=tk.LEFT)

    debug_button = tk.Button(root, text="Парабола", command=lambda: select_algorithm("parabola"))
    debug_button.pack(side=tk.LEFT)

    hermite_button = tk.Button(root, text="Эрмита", command=lambda: select_algorithm("hermite"))
    hermite_button.pack(side=tk.LEFT)

    bezie_button = tk.Button(root, text="Безье", command=lambda: select_algorithm("bezie"))
    bezie_button.pack(side=tk.LEFT)

    vspline_button = tk.Button(root, text="В-сплайн", command=lambda: select_algorithm("vspline"))
    vspline_button.pack(side=tk.LEFT)

    cube_button = tk.Button(root, text="Куб", command=lambda: select_algorithm("cube"))
    cube_button.pack(side=tk.LEFT)

    debug_button = tk.Button(root, text="Отладка", command=toggle_debug_mode)
    debug_button.pack(side=tk.RIGHT)

    canvas.bind("<Button-3>", handle_click_3)
    canvas.bind("<ButtonRelease-3>", handle_release_3)
    canvas.bind("<Button-1>", handle_click)
    canvas.bind("<ButtonRelease-1>", handle_release)

    root.mainloop()


if __name__ == "__main__":
    main()
