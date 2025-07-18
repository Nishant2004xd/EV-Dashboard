from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
import random
import csv
from datetime import datetime, timedelta

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\samyn\Desktop\EV Final\build\assets\frame0")
SPEED_ASSETS_PATH = ASSETS_PATH / Path("speed")
CSV_FILE_PATH = OUTPUT_PATH / "data_log.csv"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def relative_to_speed_assets(path: str) -> Path:
    return SPEED_ASSETS_PATH / Path(path)


# Initialize CSV file with session time as a header
start_time = datetime.now()


def init_csv():
    elapsed_time = str(timedelta(seconds=0))
    session_time_column = f"Session {elapsed_time}"

    # Add BMS cells 1-14 as additional columns
    bms_cell_columns = [f"Cell {i + 1} Voltage" for i in range(14)]

    if not CSV_FILE_PATH.exists():
        with open(CSV_FILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                                "Timestamp", "Speed", "Temperature (C)", "SOC (%)",
                                "Current (A)", "Odometer (Km)", "Battery (V)", session_time_column
                            ] + bms_cell_columns)


def append_to_csv(speed, temp, soc, current, odometer, battery, session_time, bms_cell_values):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Placeholder for BMS cell values (14 cells)
    if not bms_cell_values:
        bms_cell_values = [random.uniform(3.0, 4.2) for _ in range(14)]  # Simulate random BMS values

    with open(CSV_FILE_PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
                            current_time, speed, temp, soc, current, odometer, battery, session_time
                        ] + bms_cell_values)


def update_values():
    speed_value = random.randint(0, 120)
    temp_value = random.randint(0, 100)
    soc_value = random.randint(0, 100)
    current_value = round(random.uniform(0, 100))
    odometer_value = random.randint(0, 100)  # Simulated odometer value
    battery_value = random.randint(0, 100)

    # Adjust positions for SOC based on number of digits
    if soc_value < 10:
        canvas.coords(soc_text, 729.0, 352.0)
    elif soc_value < 100:
        canvas.coords(soc_text, 723.0, 352.0)
    else:
        canvas.coords(soc_text, 715.0, 352.0)

    # Adjust positions for temperature based on number of digits
    if temp_value < 10:
        canvas.coords(temp_text, 705.0, 444.0)
    else:
        canvas.coords(temp_text, 700.0, 444.0)

    # Adjust positions for current based on number of digits
    if current_value < 100:
        canvas.coords(current_text_object, 197.0, 348.0)
    else:
        canvas.coords(current_text_object, 191.0, 348.0)

    # Update GUI text
    canvas.itemconfig(battery_text, text=f"{battery_value}V")
    canvas.itemconfig(speed_text, text=f"{speed_value}")
    canvas.itemconfig(soc_text, text=f"{soc_value}%")
    canvas.itemconfig(range_text, text=f"{odometer_value} Km")
    canvas.itemconfig(temp_text, text=f"{temp_value} C")
    canvas.itemconfig(current_text_object, text=f"{current_value} A")

    # Update speed image
    rounded_speed = round(speed_value / 10) * 10
    speed_image_path = relative_to_speed_assets(f"speed_{rounded_speed}.png")
    speed_image = PhotoImage(file=speed_image_path)
    canvas.itemconfig(speed_image_object, image=speed_image)
    canvas.images['speed'] = speed_image  # Keep a reference to avoid garbage collection

    # Update session time
    elapsed_time = datetime.now() - start_time
    formatted_time = str(timedelta(seconds=round(elapsed_time.total_seconds())))
    canvas.itemconfig(session_time, text=formatted_time)

    # Simulate fetching 14 BMS cell values
    bms_cell_values = [random.uniform(3.0, 4.2) for _ in range(14)]

    # Append data to CSV
    append_to_csv(speed_value, temp_value, soc_value, current_value, odometer_value, battery_value, formatted_time,
                  bms_cell_values)

    window.after(1000, update_values)  # Update every second


window = Tk()
window.geometry("800x480")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=480,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Load all images except image_11.png
images = []

image_path = relative_to_assets(f"design-ev-new.png")
images.append(PhotoImage(file=image_path))

# Create image objects on canvas
image_objects = []
for index, image in enumerate(images):
    x_pos = 400.0 if index != 9 else 409.0
    y_pos = 240.0 if index != 9 else 242.0
    image_object = canvas.create_image(x_pos, y_pos, image=image)
    image_objects.append(image_object)

# Create a placeholder for speed image
speed_image_path = relative_to_speed_assets("speed_0.png")
speed_image = PhotoImage(file=speed_image_path)
speed_image_object = canvas.create_image(400.0, 190.0, image=speed_image)
canvas.images = {'speed': speed_image}  # Dictionary to store images

# Text objects
battery_text = canvas.create_text(
    495.0,
    352.0,
    anchor="nw",
    text="0V",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 18, "bold italic")
)

speed_text = canvas.create_text(
    548.0,
    196.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 90, "bold italic")
)

soc_text = canvas.create_text(
    723.0,
    352.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 18, "bold italic")
)

range_text = canvas.create_text(
    190.0,
    425.0,
    anchor="nw",
    text="0 Km",
    fill="#38F86E",
    font=("Inter BoldItalic", 18, "bold italic")
)

session_time = canvas.create_text(
    483.0,
    421.0,
    anchor="nw",
    text="0:00:00",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 20, "bold italic")
)

temp_text = canvas.create_text(
    700.0,
    444.0,
    anchor="nw",
    text="0 C",
    fill="#38F86E",
    font=("Inter BoldItalic", 18, "bold italic")
)

# Current text object
current_text_object = canvas.create_text(
    191.0,
    348.0,
    anchor="nw",
    text="0 A",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 20, "bold italic")
)

# Initialize the CSV file
init_csv()

# Start updating values
update_values()

# Handle closing the window (stop the session timer)
window.protocol("WM_DELETE_WINDOW", window.quit)

# Run main loop
window.overrideredirect(True)
window.resizable(False, False)
window.mainloop()
