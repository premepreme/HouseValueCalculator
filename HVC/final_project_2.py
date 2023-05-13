import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

matplotlib.use('TkAgg')


class App(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="news")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.bedroom = tk.StringVar()
        self.bathroom = tk.StringVar()
        self.parent.title("House Value Calculator")

        self.init_components()

    def init_components(self):
        self.bedroom_input = tk.Entry(self, textvariable=self.bedroom)
        self.bathroom_input = tk.Entry(self, textvariable=self.bathroom)
        self.text_bedroom = tk.Label(self, text="Number of Bedroom")
        self.text_bathroom = tk.Label(self, text="Number of Bathroom")
        self.quit_bt = tk.Button(self, text="QUIT", command=self.quit_handle)

        self.text_bedroom.grid(row=1, column=1, padx=5, pady=5)
        self.bedroom_input.grid(row=1, column=2, padx=5, pady=5)
        self.text_bathroom.grid(row=1, column=3, padx=5, pady=5)
        self.bathroom_input.grid(row=1, column=4, padx=5, pady=5)
        self.quit_bt.grid(row=2, column=4)

    def quit_handle(self):
        time.sleep(2)
        self.parent.destroy()


class Data(ttk.Frame):

    def __init__(self, parent, filename, input_data: App):
        super().__init__(parent)
        self.data = pd.read_csv(f'{filename}')
        self.app = input_data
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self.error_text = tk.Label(self.app, text="The house you are looking for does not exist.Please try again"
                                   , fg='red', font=("Arial", 16))
        self.init_components()
        self.plot_components()

    def init_components(self):
        self.enter_bt = tk.Button(self.app, text="Enter", command=self.check_plot)
        self.clear_bt = tk.Button(self.app, text="Clear", command=self.clear)


        self.enter_bt.grid(row=2, column=2, padx=5, pady=5)
        self.clear_bt.grid(row=2, column=3, padx=5, pady=5)


    def plot_components(self):
        self.fig1 = Figure()
        self.axes1 = self.fig1.add_subplot()
        self.fig_canvas1 = FigureCanvasTkAgg(self.fig1, master=self.app)
        self.fig_canvas1.get_tk_widget().grid(row=4, column=1,
                                              sticky="news", padx=10, pady=10, columnspan=4)
        self.axes1.set_xlabel("PRICE")
        self.axes1.set_ylabel("HOUSE NUMBER")
        self.axes1.set_title("Price of the house")

        self.fig2 = Figure()
        self.axes2 = self.fig2.add_subplot()
        self.fig_canvas2 = FigureCanvasTkAgg(self.fig2, master=self.app)
        self.fig_canvas2.get_tk_widget().grid(row=4, column=5,
                                              sticky="news", padx=10, pady=10, columnspan=6)
        self.fig2.patch.set_visible(False)
        self.axes2.axis('off')
        self.axes2.axis('tight')

    def plot(self):
        self.axes1.clear()
        self.axes1.set_xlabel("PRICE(Dollar)")
        self.axes1.set_ylabel("HOUSE NUMBER")

        self.axes2.clear()
        self.axes2.axis('off')
        df = pd.DataFrame(self.data)
        self.fig1.subplots_adjust(bottom=0.1)
        num_bathroom = float(self.app.bathroom.get())
        num_bedroom = float(self.app.bedroom.get())

        condition_1 = df['bedrooms'] == num_bedroom
        condition_2 = df['bathrooms'] == num_bathroom
        result = df[(condition_1) & (condition_2)]
        name = result['Num']
        price = result['price']
        colums = ["Num", "Storey", "driveway","recroom","Gas and Hot water systems ", "airco", "garage"]
        data_table = result[colums]
        a = pd.DataFrame(data_table.values.tolist(), columns=["Num", "Storey", "Driveway", "Rec room",
                                                              "Heater", "Airco", "Garage"])
        try:  # Check Data
            self.table = self.axes2.table(cellText=a.values, colLabels=a.columns, loc='center')
        except IndexError:  # no data case
            self.error_text.grid(row=3, column=1, columnspan=5)
        else:
            self.error_text.grid_remove()
            if num_bedroom == 1 and num_bathroom > 1:
                self.axes1.set_title(f"Price of {int(num_bedroom)} Bedroom and {int(num_bathroom)} Bathrooms")
            elif num_bedroom > 1 and num_bathroom == 1:
                self.axes1.set_title(f"Price of {int(num_bedroom)} Bedrooms and {int(num_bathroom)} Bathroom")
            elif num_bedroom > 1 and num_bathroom > 1:
                self.axes1.set_title(f"Price of {int(num_bedroom)} Bedrooms and {int(num_bathroom)} Bathrooms")
            elif num_bedroom == 1 and num_bathroom ==1:
                self.axes1.set_title(f"Price of {int(num_bedroom)} Bedroom and {int(num_bathroom)} Bathroom")
            self.axes1.barh(name, price)
            self.axes1.xaxis.set_ticks_position('none')
            self.axes1.yaxis.set_ticks_position('none')
            self.axes1.xaxis.set_tick_params(pad=5)
            self.axes1.yaxis.set_tick_params(pad=10)
            self.axes1.invert_yaxis()
            for bars in self.axes1.containers:
                self.axes1.bar_label(bars)
            self.fig_canvas1.draw()
            self.table = self.axes2.table(cellText=a.values, colLabels=a.columns, loc='center')
            self.table.auto_set_font_size(False)
            self.fig2.tight_layout()
            self.fig_canvas2.draw()

    def clear(self):
        self.axes1.clear()
        self.app.bedroom.set('')
        self.app.bathroom.set('')
        self.app.bedroom_input.config(fg='black')
        self.app.bathroom_input.config(fg='black')

    def check_plot(self):
        if self.app.bedroom.get() != '':
            try:
                float(self.app.bedroom.get())
            except ValueError:
                self.app.bedroom_input.config(fg='red')
                if self.app.bathroom.get() != '':
                    try:
                        float(self.app.bathroom.get())
                    except ValueError:
                        self.app.bathroom_input.config(fg='red')
                    else:
                        self.app.bathroom_input.config(fg='green')
            else:
                if self.app.bedroom.get() != '':
                    try:
                        float(self.app.bathroom.get())
                    except ValueError:
                        self.app.bathroom_input.config(fg='red')
                        if self.app.bedroom.get() != '':
                            try:
                                float(self.app.bedroom.get())
                            except ValueError:
                                self.app.bedroom_input.config(fg='red')
                            else:
                                self.app.bedroom_input.config(fg='green')
                    else:
                        self.app.bedroom_input.config(fg='black')
                        self.app.bathroom_input.config(fg='black')
                        self.plot()

