import tkinter as tk
from tkinter import filedialog
import pandas as pd
from PIL import ImageGrab

root = tk.Tk()
root.title("학생 시간표 통합")
root.geometry('1920x1080')

names_hidden = False
max_col_widths = []
MAX_STUDENTS_DISPLAY = 16  # 최대 16명까지만 표시

def get_color(count):
    green_shades = [
        "#FFFFFF", "#F0FFF0", "#E0FFE0", "#D0FFD0", "#C0FFC0",
        "#B0FFB0", "#A0FFA0", "#90FF90", "#80FF80", "#70FF70", "#60FF60",
        "#50FF50", "#40FF40", "#30FF30", "#20FF20", "#10FF10", "#00EE00"
    ]
    return green_shades[min(count, len(green_shades) - 1)]

def load_schedule():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            df = pd.read_csv(f)
        process_schedule(df)

def process_schedule(df):
    global current_schedule, max_col_widths
    current_schedule = df
    max_col_widths = [max(len(str(cell)) for cell in df[col]) for col in df.columns]
    refresh_schedule(df)

def toggle_names():
    global names_hidden
    names_hidden = not names_hidden
    refresh_schedule(current_schedule)

def refresh_schedule(df):
    for widget in frame.winfo_children():
        widget.destroy()
    
    time_slots = df['시간대']
    days = df.columns[1:]
    overlaps = {}
    
    for i, time_slot in enumerate(time_slots):
        for day in days:
            cell_data = df.at[i, day]
            students = cell_data.split(",") if isinstance(cell_data, str) else []
            overlaps[(time_slot, day)] = len(students)
    
    for i, time_slot in enumerate(time_slots):
        for j, day in enumerate(days):
            count = overlaps[(time_slot, day)]
            color = get_color(count)
            
            cell_data = df.at[i, day]
            students = cell_data.split(",") if isinstance(cell_data, str) else []
            
            if names_hidden:
                label_text = f"({count}명)"
            else:
                displayed_students = students[:MAX_STUDENTS_DISPLAY]
                label_text = ", ".join(displayed_students) + ("..." if len(students) > MAX_STUDENTS_DISPLAY else "")
                label_text += f" ({count}명)"
            
            label = tk.Label(frame, text=label_text, bg=color, padx=5, pady=5, 
                             borderwidth=1, relief="solid", width=20, height=3, 
                             wraplength=250, justify="center")
            label.grid(row=i+1, column=j+1, sticky="nsew")
    
    for j, day in enumerate(days):
        label = tk.Label(frame, text=day, bg="lightgrey", padx=10, pady=5, 
                         borderwidth=1, relief="solid", width=20, height=2)
        label.grid(row=0, column=j+1, sticky="nsew")
    
    for i, time_slot in enumerate(time_slots):
        label = tk.Label(frame, text=time_slot, bg="lightgrey", padx=10, pady=5, 
                         borderwidth=1, relief="solid", width=20, height=2)
        label.grid(row=i+1, column=0, sticky="nsew")
    
    for j in range(len(df.columns)):
        frame.grid_columnconfigure(j, weight=1)
    
    for i in range(len(time_slots)):
        frame.grid_rowconfigure(i, weight=1)

def save_as_image():
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()
    image = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        image.save(save_path)

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

load_button = tk.Button(root, text="시간표 불러오기", command=load_schedule)
load_button.pack(pady=10)

toggle_button = tk.Button(root, text="이름 숨기기/보이기", command=toggle_names)
toggle_button.pack(pady=10)

save_button = tk.Button(root, text="이미지로 저장", command=save_as_image)
save_button.pack(pady=10)

root.mainloop()
