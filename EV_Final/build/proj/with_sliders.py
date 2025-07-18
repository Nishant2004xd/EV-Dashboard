from pathlib import Path
from tkinter import Tk, Canvas, Toplevel, Scale, Label, Button, PhotoImage, BOTTOM, X, IntVar, Checkbutton

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\samyn\Desktop\EV Final\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def on_slider_change(event=None):
    speed_value = slider1.get()
    battery_value = slider2.get()
    soc_value = slider3.get()
    range_value = slider4.get()
    temp_value = slider5.get()

    # Update canvas text elements
    canvas.itemconfig(speed_text, text=f"{speed_value}V")
    canvas.itemconfig(battery_text, text=f"{battery_value}")
    canvas.itemconfig(soc_text, text=f"{soc_value}")
    canvas.itemconfig(range_text, text=f"{range_value}")
    canvas.itemconfig(temp_text, text=f"{temp_value} C")


def toggle_image():
    if show_image.get() == 1:
        canvas.itemconfig(image_8, state="normal")
    else:
        canvas.itemconfig(image_8, state="hidden")


window = Tk()

slider_window = Toplevel(window)
slider_window.geometry("300x600")
slider_window.title("Slider Window")

#Labels
label_speed = Label(slider_window, text="Battery")
label_speed.pack()

slider1 = Scale(slider_window, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider1.pack(expand=True, fill=X)

label_battery = Label(slider_window, text="speed")
label_battery.pack()

slider2 = Scale(slider_window, from_=0, to=120, orient='horizontal', command=on_slider_change)
slider2.pack(expand=True, fill=X)

label_soc = Label(slider_window, text="SOC")
label_soc.pack()

slider3 = Scale(slider_window, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider3.pack(expand=True, fill=X)

label_range = Label(slider_window, text="Range")
label_range.pack()

slider4 = Scale(slider_window, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider4.pack(expand=True, fill=X)

label_temp = Label(slider_window, text="Temp")
label_temp.pack()

slider5 = Scale(slider_window, from_=0, to=100, orient='horizontal', command=on_slider_change)
slider5.pack(expand=True, fill=X)

#Checkbox for HV
show_image = IntVar()
checkbox_show_image = Checkbutton(slider_window, text="Show Image 8", variable=show_image, command=toggle_image)
checkbox_show_image.pack()

show_image.set(0)

# Create canvas in the main window
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

# Load all images
images = []
for i in range(1, 17):
    image_path = relative_to_assets(f"image_{i}.png")
    images.append(PhotoImage(file=image_path))

# Create image objects on canvas
image_objects = []
for index, image in enumerate(images):
    x_pos = 400.0 if index != 9 else 409.0
    y_pos = 240.0 if index != 9 else 242.0
    image_object = canvas.create_image(x_pos, y_pos, image=image)
    image_objects.append(image_object)

# Text objects
speed_text = canvas.create_text(
    495.0,
    352.0,
    anchor="nw",
    text="0V",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 18)
)

battery_text = canvas.create_text(
    548.0,
    196.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 90)
)

soc_text = canvas.create_text(
    723.0,
    352.0,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Inter BoldItalic", 18)
)

range_text = canvas.create_text(
    140.0,
    433.0,
    anchor="nw",
    text="0",
    fill="#38F86E",
    font=("Inter BoldItalic", 18)
)

temp_text = canvas.create_text(
    698.0,
    444.0,
    anchor="nw",
    text="0 C",
    fill="#38F86E",
    font=("Inter BoldItalic", 18)
)

# Initially hide image_8
image_8 = image_objects[7]  # Index 7 corresponds to image_8 in the list
canvas.itemconfig(image_8, state="hidden")

# Run main loop
window.resizable(False, False)
window.mainloop()
