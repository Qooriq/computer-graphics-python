import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

lines_data = {
    "step_by_step": {"points": [], "color": "red"},
    "dda": {"points": [], "color": "black"},
    "bresenham": {"points": [], "color": "green"},
    "circle": {"points": [], "color": "blue"}
}

labels = ['step_by_step', 'dda', 'bresenham', 'circle']


def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000
    return result, execution_time


def validate_input_lines(*args):
    try:
        return [int(arg.get()) for arg in args]
    except ValueError:
        error_label.config(text="Ошибка: введите целочисленные значения для полей X1, X2, Y1, Y2.")
        return None


def validate_input_circle(*args):
    try:
        return [int(arg.get()) for arg in args]
    except ValueError:
        error_label.config(text="Ошибка: введите целочисленные значения для полей X1, Y1, Радиус.")
        return None


def step_by_step_line(x1, y1, x2, y2):
    points = []
    if x2 != x1:
        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1
    else:
        if y1 > y2:
            y1, y2 = y2, y1
        for y in range(y1, y2 + 1):
            points.append((x1, y))
        labels.append('step_by_step')
        labels.remove('step_by_step')
        return points
    if x1 > x2:
        x1, x2 = x2, x1
    while x1 <= x2:
        y = k * x1 + b
        points.append((round(x1), round(y)))
        x1 += 0.1
    labels.append('step_by_step')
    labels.remove('step_by_step')
    return points


def dda_line(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    if steps == 0:
        labels.append('dda')
        labels.remove('dda')
        return [(x1, y1)]

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1
    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    labels.append('dda')
    labels.remove('dda')
    return points


def bresenham_line(x1, y1, x2, y2):
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    x, y = x1, y1
    while True:
        points.append((x, y))
        if x == x2 and y == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy

    labels.append('bresenham')
    labels.remove('bresenham')
    return points


def bresenham_circle(x1, y1, radius):
    radius = abs(radius)
    points = []
    x = 0
    y = radius
    d = 3 - 2 * radius
    while y >= x:
        points.extend([
            (x1 + x, y1 + y), (x1 - x, y1 + y), (x1 + x, y1 - y), (x1 - x, y1 - y),
            (x1 + y, y1 + x), (x1 - y, y1 + x), (x1 + y, y1 - x), (x1 - y, y1 - x)
        ])
        if d <= 0:
            d = d + 4 * x + 6
        else:
            d = d + 4 * (x - y) + 10
            y -= 1
        x += 1

    labels.append('circle')
    labels.remove('circle')
    return points


def plot_points(ax, points, color='red'):
    for x, y in points:
        square = patches.Rectangle((x, y), 1, 1, linewidth=0, facecolor=color)
        ax.add_patch(square)


def draw_graph():
    global canvas, fig, ax

    if canvas:
        canvas.get_tk_widget().destroy()

    fig.clf()
    ax = fig.add_subplot(111)

    try:
        a = abs(int(scale_entry.get()))
    except ValueError:
        error_label.config(text='Ошибка: введите целочисленное значение для масштаба')

    ax.set_xticks(range(-a, a + 1, a // 10 if a > 15 else 1))
    ax.set_yticks(range(-a, a + 1, a // 10 if a > 15 else 1))
    ax.grid(True, which='both', color='lightgray', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_aspect('equal')

    ax.set_xlim(-a, a)
    ax.set_ylim(-a, a)

    for label in labels:
        line_data = lines_data[label]
        if line_data['points']:
            plot_points(ax, line_data["points"], color=line_data["color"])

    ax.set_title("Различные алгоритмы линий")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def draw_step_by_step():
    inputs = validate_input_lines(entry_x1, entry_y1, entry_x2, entry_y2)
    if inputs:
        x1, y1, x2, y2 = inputs
        points, exec_time = measure_time(step_by_step_line, x1, y1, x2, y2)
        lines_data["step_by_step"]["points"] = points
        error_label.config(text=f"Пошаговый алгоритм: время выполнения {exec_time:.2f} мс")
        draw_graph()


def draw_dda():
    inputs = validate_input_lines(entry_x1, entry_y1, entry_x2, entry_y2)
    if inputs:
        x1, y1, x2, y2 = inputs
        points, exec_time = measure_time(dda_line, x1, y1, x2, y2)
        lines_data["dda"]["points"] = points
        error_label.config(text=f"Алгоритм ЦДА: время выполнения {exec_time:.2f} мс")
        draw_graph()


def draw_bresenham():
    inputs = validate_input_lines(entry_x1, entry_y1, entry_x2, entry_y2)
    if inputs:
        x1, y1, x2, y2 = inputs
        points, exec_time = measure_time(bresenham_line, x1, y1, x2, y2)
        lines_data["bresenham"]["points"] = points
        error_label.config(text=f"Алгоритм Брезенхема: время выполнения {exec_time:.2f} мс")
        draw_graph()


def draw_circle():
    inputs = validate_input_circle(entry_x1, entry_y1, entry_radius)
    if inputs:
        x1, y1, radius = inputs
        points, exec_time = measure_time(bresenham_circle, x1, y1, radius)
        lines_data["circle"]["points"] = points
        error_label.config(text=f"Алгоритм Брезенхема (окружность): время выполнения {exec_time:.2f} мс")
        draw_graph()


def clear_step_by_step():
    lines_data["step_by_step"]["points"] = []
    error_label.config(text="Пошаговая линия удалена")
    draw_graph()


def clear_dda():
    lines_data["dda"]["points"] = []
    error_label.config(text="Линия DDA удалена")
    draw_graph()


def clear_bresenham():
    lines_data["bresenham"]["points"] = []
    error_label.config(text="Линия Брезенхэма удалена")
    draw_graph()


def clear_circle():
    lines_data["circle"]["points"] = []
    error_label.config(text="Окружность Брезенхема удалена")
    draw_graph()


def clear_all():
    for key in lines_data:
        lines_data[key]["points"] = []
    error_label.config(text="Все линии удалены")
    draw_graph()


def update_scale():
    try:
        a = abs(int(scale_entry.get()))
        draw_graph()
        error_label.config(text=f"Масштаб изменен на [-{a}, {a}] по обеим осям")
    except ValueError:
        error_label.config(text="Ошибка: введите целочисленное значение для масштаба.")


app = tk.Tk()
app.title("Графическое приложение для растеризации")

left_frame = ttk.Frame(app)
left_frame.pack(side=tk.TOP, padx=10, pady=10)

right_frame = ttk.Frame(app)
right_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


ttk.Label(left_frame, text="X1:").grid(row=0, column=0)
entry_x1 = ttk.Entry(left_frame, width=5)
entry_x1.grid(row=0, column=1)

ttk.Label(left_frame, text="Y1:").grid(row=0, column=2)
entry_y1 = ttk.Entry(left_frame, width=5)
entry_y1.grid(row=0, column=3)

ttk.Label(left_frame, text="X2:").grid(row=1, column=0)
entry_x2 = ttk.Entry(left_frame, width=5)
entry_x2.grid(row=1, column=1)

ttk.Label(left_frame, text="Y2:").grid(row=1, column=2)
entry_y2 = ttk.Entry(left_frame, width=5)
entry_y2.grid(row=1, column=3)

ttk.Label(left_frame, text="Радиус:").grid(row=2, column=0)
entry_radius = ttk.Entry(left_frame, width=5)
entry_radius.grid(row=2, column=1)

button1 = ttk.Button(left_frame, text="Пошаговая линия", command=draw_step_by_step)
button1.grid(row=3, column=0, padx=5, pady=5)

button2 = ttk.Button(left_frame, text="Линия DDA", command=draw_dda)
button2.grid(row=3, column=1, padx=5, pady=5)

button3 = ttk.Button(left_frame, text="Линия Брезенхэма", command=draw_bresenham)
button3.grid(row=3, column=2, padx=5, pady=5)

button4 = ttk.Button(left_frame, text="Окружность Брезенхэма", command=draw_circle)
button4.grid(row=3, column=3, padx=5, pady=5)

button_clear_step_by_step = ttk.Button(left_frame, text="Удалить пошаговую линию", command=clear_step_by_step)
button_clear_step_by_step.grid(row=4, column=0, padx=5, pady=5)

button_clear_dda = ttk.Button(left_frame, text="Удалить линию DDA", command=clear_dda)
button_clear_dda.grid(row=4, column=1, padx=5, pady=5)

button_clear_bresenham = ttk.Button(left_frame, text="Удалить линию Брезенхэма", command=clear_bresenham)
button_clear_bresenham.grid(row=4, column=2, padx=5, pady=5)

button_clear_circle = ttk.Button(left_frame, text="Удалить окружность", command=clear_circle)
button_clear_circle.grid(row=4, column=3, padx=5, pady=5)

button_clear_all = ttk.Button(left_frame, text="Удалить всё", command=clear_all)
button_clear_all.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

error_label = ttk.Label(left_frame, text="", foreground="red")
error_label.grid(row=6, column=0, columnspan=4)

scale_label = ttk.Label(left_frame, text=":Масштаб")
scale_label.grid(row=7, column=0, columnspan=4, padx=5, pady=5)
scale_entry = ttk.Entry(left_frame, width=5)
scale_entry.grid(row=7, column=1, padx=5, pady=5)
scale_entry.insert(0, "15")

button_update_scale = ttk.Button(left_frame, text="Изменить масштаб", command=update_scale)
button_update_scale.grid(row=8, column=0, columnspan=4, padx=5, pady=5)

fig = plt.Figure(figsize=(5, 5), dpi=100)
ax = fig.add_subplot(111)
canvas = None

draw_graph()

app.mainloop()

