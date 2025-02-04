from customtkinter import *
from PIL import Image
import json
import utils
import time

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from backend import plotter


# Load in the styles
with open('./static/styles.json', 'r') as f:
    styling = json.load(f)
fonts = styling['fonts']
colours = styling['colours']


class MyTabView(CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=0)

        # Change font size of tab buttons
        self._segmented_button.configure(font=(fonts['primary'], 16))

        # Create tabs
        self.dashboard = self.add("Dashboard")
        self.toolkit = self.add("Toolkit")
        self.help = self.add("Help")

        # self.tab('Dashboard').grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        # self.tab('Toolkit').grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        # self.tab('Help').grid(row=0, column=0, padx=0, pady=0, sticky="ew")


class Dashboard(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame, for example:
        self.radio = CTkRadioButton(self, text="Radio Button")
        self.radio.grid(row=0, column=0, padx=20, pady=20)
        
        # add widgets onto the frame, for example:
        self.radio = CTkRadioButton(self, text="Radio Button")
        self.radio.grid(row=0, column=1, padx=20, pady=20)

        # add widgets onto the frame, for example:
        self.radio = CTkRadioButton(self, text="Radio Button")
        self.radio.grid(row=0, column=2, padx=20, pady=20)


class Toolkit(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # self.plot_btn = CTkButton(self, text="Plot Sine Wave", command=plotter.plot_sine_wave(50, 50, 0, 5))
        # self.plot_btn.grid(row=0, column=0, padx=20, pady=20)

        self.intro = CTkLabel(self, text="Select a tool to begin", font=(fonts['primary'], 24, "bold"))
        self.intro.grid(row=0, column=2, padx=0, pady=20)

        # Free vibration testing
        self.free_btn = ToolBtn(self, tool_name="Free Vibration")
        self.free_btn.grid(row=1, column=0, padx=20, pady=20)

        # Hammer testing
        self.hammer_btn = ToolBtn(self, tool_name="Hammer")
        self.hammer_btn.grid(row=1, column=1, padx=20, pady=20)

        # Sine-sweep testing
        self.random = ToolBtn(self, tool_name="Random")
        self.random.grid(row=1, column=2, padx=20, pady=20)

        # Stepped-sweep testing
        self.sine_sweep = ToolBtn(self, tool_name="Sine Sweep")
        self.sine_sweep.grid(row=1, column=3, padx=20, pady=20)
        
        # Forced vibration testing
        self.stepped_sweep = ToolBtn(self, tool_name="Stepped Sweep")
        self.stepped_sweep.grid(row=1, column=4, padx=20, pady=20)

        # Discrete Fourier Transform
        self.dft = ToolBtn(self, tool_name="DFT")
        self.dft.grid(row=1, column=5, padx=20, pady=20)


class ToolBtn(CTkButton):
    def __init__(self, master, tool_name: str, **kwargs):
        super().__init__(master, **kwargs)

        self.tool_window = None
        self.configure(
            text=tool_name,
            command=self.open_new_window,
            state=utils.get_tool_state(tool_name),
            fg_color=colours['button'],
            font=(fonts['tertiary'], 16)
        )
    
    def open_new_window(self):
        if self.tool_window is None or not self.tool_window.winfo_exists():
            tool_name = self.cget("text")
            if tool_name == "Free Vibration":
                ToolWindow = FreeVibration
            elif tool_name == "Hammer":
                ToolWindow = Hammer
            elif tool_name == "Random":
                ToolWindow = Random
            elif tool_name == "Sine Sweep":
                ToolWindow = SineSweep
            elif tool_name == "Stepped Sweep":
                ToolWindow = SteppedSweep
            elif tool_name == "DFT":
                ToolWindow = DFT
            self.tool_window = ToolWindow(self)  # create window if its None or destroyed
            self.tool_window.configure(width=810, height=1000)
            self.tool_window.focus()
        else:
            self.tool_window.focus()  # if window exists focus it


class FreeVibration(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Free Vibration")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


class Hammer(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Hammer")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


class SineSweep(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Sine Sweep")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


class Random(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Random")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


class SteppedSweep(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Stepped Sweep")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


class DFT(CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title("DFT")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)


class Help(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)

        self.welcome = CTkLabel(self, text="Welcome to PartCZ!", font=(fonts['primary'], 24, "bold"))
        self.welcome.grid(row=0, column=0, padx=0, pady=20, sticky="ew")

        with open('./static/help.txt', 'r') as f:
            help_text = f.read()

        self.help = CTkLabel(self, text=help_text)
        self.help.grid(row=1, column=0, padx=0)


class ProgressBar(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)

        self.label = CTkLabel(self, text=f"Progress: {utils.read_progress()*100:.0f}%", font=(fonts['primary'], 16, "bold"))
        self.label.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

        self.bar = CTkProgressBar(self, orientation="horizontal", fg_color=colours['foreground'], progress_color=colours['button'])
        self.bar.set(utils.read_progress())
        self.bar.grid(row=0, column=1, padx=0, pady=0, sticky="ew")


    def progress(self):

        self.label.configure(text=f"Progress: {utils.read_progress()*100:.0f}%")
        self.bar.set(utils.read_progress())


class App(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("810x1000")
        self.title("PartCZ!")

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        banner_image = CTkImage(light_image=Image.open("./static/AnthonyStappan.png"), size=(200, 60))
        self.banner_image = CTkLabel(self, image=banner_image, text="")
        self.banner_image.grid(row=0, column=0, padx=0, pady=20, sticky="nsew")

        self.tab_view = MyTabView(
            master=self, 
            width=1500, 
            height=825, 
            segmented_button_fg_color=colours['button'],
            segmented_button_selected_color=colours['button_active'], 
            # segmented_button_selected_hover_color=colours['button_hover'],
            segmented_button_unselected_color=colours['button'],
            # segmented_button_unselected_hover_color=colours['button_hover'],
            bg_color=colours['background'],
            fg_color=colours['foreground'],
            corner_radius=10
        )
        self.tab_view.grid(row=1, column=0, padx=20, pady=10)

        self.dashboard = Dashboard(
            master=self.tab_view.tab("Dashboard"),
            bg_color=colours['background'],
            fg_color=colours['foreground']
        )
        self.dashboard.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.toolkit = Toolkit(
            master=self.tab_view.tab("Toolkit"),
            bg_color=colours['background'],
            fg_color=colours['foreground']
        )
        self.toolkit.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.help = Help(
            master=self.tab_view.tab("Help"),
            bg_color=colours['background'],
            fg_color=colours['foreground']
        )
        self.help.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        self.progress_bar = ProgressBar(
            master=self,
            fg_color='gray92'
        )
        self.progress_bar.grid(row=2, column=0, padx=100, pady=10, sticky="nsew")
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
