from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
import random
import csv
from datetime import datetime
import subprocess
import json


def get_bms_data():
    try:
        # Run the bash command and capture the output
        command = ['daly-bms-cli', '-d', '/dev/ttyUSB0', '--all']
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Parse the JSON output
        data = json.loads(result.stdout)
        return data

    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")
        return None

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\samyn\Desktop\EV Final\build\assets\frame0")
SPEED_ASSETS_PATH = ASSETS_PATH / Path("speed")
CSV_FILE_PATH = OUTPUT_PATH / "data_log.csv"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_speed_assets(path: str) -> Path:
    return SPEED_ASSETS_PATH / Path(path)

# Initialize CSV file with headers if it does not exist
if not CSV_FILE_PATH.exists():
    with open(CSV_FILE_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Battery (V)", "Speed", "SOC", "Range", "Temperature (C)", "Laptime"])


def update_values():
    # Get data from the BMS
    bms_data = get_bms_data()

    if bms_data is not None:
        battery_value = bms_data['soc']['total_voltage']
        speed_value = random.randint(0, 120)  # Assuming no speed in BMS data
        soc_value = bms_data['soc']['soc_percent']
        range_value = random.randint(0, 100)  # Assuming range is not available in BMS data
        temp_value = bms_data['temperature_range']['highest_temperature']

        # Update GUI text
        canvas.itemconfig(battery_text, text=f"{battery_value}V")
        canvas.itemconfig(speed_text, text=f"{speed_value}")
        canvas.itemconfig(soc_text, text=f"{soc_value}")
        canvas.itemconfig(range_text, text=f"{range_value}")
        canvas.itemconfig(temp_text, text=f"{temp_value} C")

        # Update speed image
        rounded_speed = round(speed_value / 10) * 10
        speed_image_path = relative_to_speed_assets(f"speed_{rounded_speed}.png")
        speed_image = PhotoImage(file=speed_image_path)
        canvas.itemconfig(speed_image_object, image=speed_image)
        canvas.images['speed'] = speed_image  # Keep a reference to avoid garbage collection

        # Append data to CSV file with timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILE_PATH, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                current_time, battery_value, speed_value, soc_value, range_value, temp_value,
                canvas.itemcget(timer_text_object, 'text')
            ])

    # Schedule the next update
    window.after(1000, update_values)
def update_timer(seconds):
    # Format seconds into hh:mm:ss
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    timer_text = f"{hours:0>1}:{minutes:0>2}:{secs:0>2}"
    canvas.itemconfig(timer_text_object, text=timer_text, fill="#FFFFFF")

    if seconds >= 10:
        seconds = 0  # Reset timer every 10 seconds
    else:
        seconds += 1

    window.after(1000, update_timer, seconds)  # Update every second

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
for i in range(1, 17):
    if i != 11:  # Skip image_11.png
        image_path = relative_to_assets(f"image_{i}.png")
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
    140.0,
    433.0,
    anchor="nw",
    text="0",
    fill="#38F86E",
    font=("Inter BoldItalic", 18, "bold italic")
)

temp_text = canvas.create_text(
    698.0,
    444.0,
    anchor="nw",
    text="0 C",
    fill="#38F86E",
    font=("Inter BoldItalic", 18, "bold italic")
)

# Timer text object
timer_text_object = canvas.create_text(
    182.0,
    348.0,
    anchor="nw",
    text="0:00:00",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 20, "bold italic")
)

# Start updating values
update_values()
update_timer(0)  # Start the timer

# Run main loop
window.overrideredirect(True)
window.resizable(False, False)
window.mainloop()
