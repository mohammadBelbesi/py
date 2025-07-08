import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import math
import time

# Constants
RED_TRIANGLE_AREA = 1
WHITE_TRIANGLE_AREA = 0.5
BASE_LENGTH = 400

# Geometry logic
def count_red(n):
    if n == 1:
        return 1  # 1 red triangle drawn
    elif n == 2:
        return 3
    else:
        return 3 * count_red(n - 1)

def count_white(n):
    if n == 1:
        return 0  # no inner white triangle at stage 1
    elif n == 2:
        return 1
    else:
        return count_white(n - 1) + count_red(n - 1)

def total_area(n):
    red = count_red(n)
    white = count_white(n)
    return red * RED_TRIANGLE_AREA + white * WHITE_TRIANGLE_AREA

def draw_triangle(canvas, x, y, size, color):
    h = math.sqrt(3)/2 * size
    points = [x, y,
              x + size, y,
              x + size / 2, y - h]
    canvas.create_polygon(points, fill=color, outline="black")
    canvas.update()
    time.sleep(0.02)

def draw_recursive(canvas, x, y, size, stage):
    if stage == 0:
        draw_triangle(canvas, x, y, size, "red")
    else:
        half = size / 2
        h = math.sqrt(3)/2 * half
        draw_recursive(canvas, x, y, half, stage-1)
        draw_recursive(canvas, x + half, y, half, stage-1)
        draw_recursive(canvas, x + half/2, y - h, half, stage-1)

def generate_csv():
    try:
        n = int(entry.get())
        if n < 1:
            raise ValueError
    except:
        messagebox.showerror("Invalid Input", "Please enter a valid stage number before exporting.")
        return

    with open('zelda_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stage", "Red Triangles", "White Triangles", "Total Area"])
        writer.writerow([n, count_red(n), count_white(n), total_area(n)])

    messagebox.showinfo("Export", f"CSV for stage {n} created successfully!")

def on_calculate():
    try:
        n = int(entry.get())
        if n < 1:
            raise ValueError
        red = count_red(n)
        white = count_white(n)
        area = total_area(n)
        result_text.set(f"Stage {n}:\nRed Triangles: {red}\nWhite Triangles: {white}\nTotal Area: {area}")
        draw_on_canvas(n)
        show_graphs(n)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a positive integer.")

def show_graphs(n):
    for widget in graph_left_frame.winfo_children():
        widget.destroy()
    for widget in graph_right_frame.winfo_children():
        widget.destroy()

    stages = list(range(1, n + 1))
    reds = [count_red(i) for i in stages]
    whites = [count_white(i) for i in stages]
    areas = [total_area(i) for i in stages]

    fig1, ax1 = plt.subplots(figsize=(4, 4))
    ax1.plot(stages, reds, color='red', marker='o', label='Red')
    ax1.plot(stages, whites, color='black', marker='s', label='White')
    ax1.set_title("Triangles Count")
    ax1.set_xlabel("Stage")
    ax1.set_ylabel("Number of Triangles")
    ax1.legend()
    
    canvas1 = FigureCanvasTkAgg(fig1, master=graph_left_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack()

    fig2, ax2 = plt.subplots(figsize=(4, 4))
    ax2.plot(stages, areas, label="Total Area", color='green', marker='^')
    ax2.set_title("Total Area")
    ax2.set_xlabel("Stage")
    ax2.set_ylabel("Area")
    ax2.legend()
    canvas2 = FigureCanvasTkAgg(fig2, master=graph_right_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

def draw_on_canvas(n):
    canvas.delete("all")
    
    start_x = 100
    start_y = 450
    draw_triangle(canvas, start_x, start_y, BASE_LENGTH, "white")
    draw_recursive(canvas, start_x, start_y, BASE_LENGTH, n - 1)

# GUI Setup
import sys

root = tk.Tk()
root.title("Zelda Triangle Series Explorer")

frame = tk.Frame(root)
frame.pack(padx=10, pady=5)

entry_label = tk.Label(frame, text="Enter stage number (n):")
entry_label.grid(row=0, column=0, sticky='e')

entry = tk.Entry(frame)
entry.grid(row=0, column=1)

tk.Button(frame, text="Calculate", command=on_calculate).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(frame, text="Export CSV", command=generate_csv).grid(row=2, column=0, columnspan=2, pady=5)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify='left', font=('Courier', 12)).pack()

# Layout Frame
main_frame = tk.Frame(root)
main_frame.pack(pady=10, fill='both', expand=True)

# Left graph
graph_left_frame = tk.Frame(main_frame)
graph_left_frame.pack(side='left', fill='both', expand=True)

# Drawing Canvas
canvas = tk.Canvas(main_frame, width=600, height=500, bg="white")
canvas.pack(side='left', padx=10)

# Right graph
graph_right_frame = tk.Frame(main_frame)
graph_right_frame.pack(side='left', fill='both', expand=True)


def on_exit():
    try:
        root.quit()
        root.destroy()
        sys.exit(0)
    except:
        pass  # Just in case something is already being destroyed


root.protocol("WM_DELETE_WINDOW", on_exit)


exit_button = tk.Button(
    root,
    text="Exit",
    bg="red",
    fg="white",
    font=("Helvetica", 14, "bold"),  # larger and bold text
    padx=20,  # horizontal padding
    pady=10   # vertical padding
)
exit_button.config(command=on_exit)
exit_button.pack(pady=10)



root.mainloop()