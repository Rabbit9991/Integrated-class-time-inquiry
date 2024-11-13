import tkinter as tk
from tkinter import filedialog
import pandas as pd
from PIL import ImageGrab  # 이미지 캡처를 위한 라이브러리

# Tkinter 초기 설정
root = tk.Tk()
root.title("학생 시간표 통합")

# 창 크기 설정
root.geometry('1200x800')

# 상태 변수를 사용하여 이름을 숨길지 여부를 저장
names_hidden = False  # 초기 상태는 이름이 표시됨

# 가장 긴 텍스트 길이를 저장하는 변수
max_col_widths = []

# 색상 설정 (겹치는 학생 수에 따라 색상 변경, 하양 -> 초록 10단계)
def get_color(count):
    green_shades = [
        "#FFFFFF", "#E6FFE6", "#CCFFCC", "#B3FFB3", "#99FF99",
        "#80FF80", "#66FF66", "#4DFF4D", "#33FF33", "#1AFF1A", "#00FF00"
    ]
    return green_shades[min(count, len(green_shades) - 1)]

# CSV 파일에서 시간표 데이터를 불러오는 함수
def load_schedule():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        # UTF-8 인코딩으로 파일을 열고 문제를 대체하여 처리
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            df = pd.read_csv(f)
        process_schedule(df)

# 시간표 데이터를 처리하고 시각화하는 함수
def process_schedule(df):
    global current_schedule, max_col_widths
    current_schedule = df
    
    # 각 열에서 가장 긴 텍스트의 길이를 계산
    max_col_widths = [max(len(str(cell)) for cell in df[col]) for col in df.columns]
    
    refresh_schedule(df)

# 이름을 숨기거나 표시하는 버튼 동작
def toggle_names():
    global names_hidden
    names_hidden = not names_hidden
    refresh_schedule(current_schedule)

# 시간표를 갱신하는 함수 (이름 숨기기/표시 상태에 따라 변경)
def refresh_schedule(df):
    # 기존 표시된 내용 삭제
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
            if names_hidden:
                # 이름 숨기기 모드에서는 학생 이름을 표시하지 않음
                label_text = f"({count}명)"
            else:
                # 이름 표시 모드에서는 학생 이름과 인원 표시
                label_text = f"{df.at[i, day]} ({count}명)" if isinstance(df.at[i, day], str) else f"({count}명)"
            label = tk.Label(frame, text=label_text, bg=color, padx=5, pady=3, borderwidth=1, relief="solid", width=max_col_widths[j+1])
            label.grid(row=i+1, column=j+1, sticky="nsew")

    for j, day in enumerate(days):
        label = tk.Label(frame, text=day, bg="lightgrey", padx=10, pady=5, borderwidth=1, relief="solid", width=max_col_widths[j+1])
        label.grid(row=0, column=j+1, sticky="nsew")

    for i, time_slot in enumerate(time_slots):
        label = tk.Label(frame, text=time_slot, bg="lightgrey", padx=10, pady=5, borderwidth=1, relief="solid", width=max_col_widths[0])
        label.grid(row=i+1, column=0, sticky="nsew")

    # 열 너비를 고정 (각 열의 최소 너비를 설정)
    for j in range(len(df.columns)):
        frame.grid_columnconfigure(j, weight=1)

    for i in range(len(time_slots)):
        frame.grid_rowconfigure(i, weight=1)

# 화면을 이미지로 저장하는 함수
def save_as_image():
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()

    # Tkinter 창을 캡처
    image = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # 파일로 저장
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        image.save(save_path)

# 프레임 생성 (테이블을 표시할 곳)
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# CSV 파일 불러오기 버튼
load_button = tk.Button(root, text="시간표 불러오기", command=load_schedule)
load_button.pack(pady=10)

# 이름 숨기기/보이기 버튼 추가
toggle_button = tk.Button(root, text="이름 숨기기/보이기", command=toggle_names)
toggle_button.pack(pady=10)

# 이미지로 저장하는 버튼 추가
save_button = tk.Button(root, text="이미지로 저장", command=save_as_image)
save_button.pack(pady=10)

# GUI 실행
root.mainloop()
