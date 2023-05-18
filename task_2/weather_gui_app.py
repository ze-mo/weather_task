import tkinter as tk
import weather

# Window size
ROW_SIZE = [x for x in range(10)]
COLUMN_SIZE = [x for x in range(3)]

# Color scheme
BG_COLOR = "#d5f4e6"
ENT_COLOR = "#fefbd8"
BTN_COLOR = "#618685"

# Initialize window
window = tk.Tk()
window.title("Weather app")
window.rowconfigure(ROW_SIZE, minsize=50)
window.columnconfigure(COLUMN_SIZE, minsize=200)
window.resizable(width=False, height=False)
window.configure(background=BG_COLOR)


def set_api_key():
    # Initialize second window
    secondary_window = tk.Tk()
    secondary_window.title("Set API key")
    secondary_window.resizable(width=False, height=False)
    secondary_window.configure(background=BG_COLOR)

    def submit_key():
        """
        Takes API key from input, assigns it to a constant in the weather module and closes the second window.
        """
        key = ent_key.get()
        weather.WEATHER_API_KEY = key
        secondary_window.destroy()

    lbl_key = tk.Label(master=secondary_window, text="API key: ", background=BG_COLOR)
    ent_key = tk.Entry(master=secondary_window, relief=tk.SUNKEN, background=ENT_COLOR)
    btn_submit = tk.Button(
        master=secondary_window, 
        text="Submit", 
        relief=tk.RAISED, command=submit_key, background=BTN_COLOR
        )

    lbl_key.pack(side=tk.LEFT, padx=5, pady=5)
    ent_key.pack(side=tk.LEFT, padx=5, pady=5)
    btn_submit.pack(side=tk.LEFT, padx=5, pady=5)

def load_temp():
    city = ent_city.get()
    try:
        weather_info = weather.load_data(city)
        lbl_output["text"] = weather.format_output(weather_info)
    except Exception:
        lbl_output["text"] = "Invalid input! Check if you are spelling the city correctly or if you've set a correct API key!"

def load_random_cities():
    try:
        random_cities, weather_info, coldest_city, avg_temp = weather.gather_initial_output()
        lbl_inital_stats["text"] = f"{' | '.join(random_cities)}\n\n{weather.format_output(weather_info)}\n\nColdest city: {coldest_city} | Average temperature: {avg_temp} C"
    except Exception:
        lbl_inital_stats["text"] = "Invalid request! Have you set your API key correctly?"

def clear():
    ent_city.delete(first=0, last=len(ent_city.get()))


class AppButton(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, *args, **kwargs)
        self.config(relief=tk.RAISED)
        self.config(font="Helvetica 10 bold")
        self.config(background=BTN_COLOR)

class AppLabel(tk.Label):
    def __init__(self, *args, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        self.config(background=BG_COLOR)

# Instanciate main widgets
btn_load = AppButton(text="Check weather", command=load_temp)
btn_key = AppButton(text="API key", command=set_api_key)
btn_clear = AppButton(text="Clear", command=clear)
btn_initial_stats = AppButton(text="Generate stats for 5 random cities", command=load_random_cities)

ent_city = tk.Entry(
    master=window, 
    relief=tk.SUNKEN, 
    background=ENT_COLOR
    )

lbl_output= AppLabel(text="")
lbl_inital_stats = AppLabel(text="")
lbl_check_weather = AppLabel(text="Enter city name:")
lbl_app_title = AppLabel(text="Simple Weather Application", font="Helvetica 20 bold")


# Layout
btn_load.grid(column=1, row=6, sticky='nw', padx=3, pady=3, ipadx=50, ipady=5)
btn_key.grid(column=2, row=8, ipadx=50, ipady=5)
btn_clear.grid(column=1, row=6, sticky='ne', padx=3, pady=3, ipadx=50, ipady=5)
btn_initial_stats.grid(column=1, row=1, sticky='wne')

ent_city.grid(column=1, row=5, sticky='wse')

lbl_output.grid(column=1, row=7, sticky='wsen')
lbl_inital_stats.grid(column=1, row=2)
lbl_check_weather.grid(column=1, row=5, sticky='wn')
lbl_app_title.grid(column=1, row=0, sticky='we')

# Event loop
window.mainloop()
