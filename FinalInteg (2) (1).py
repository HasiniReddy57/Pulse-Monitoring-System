import socket
import tkinter as tk
from tkinter import PhotoImage, simpledialog
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

hostMACAddress = 'D8:3A:DD:3C:E0:7B'  # The MAC address of a Bluetooth adapter on the server.
port = 4  # Port used by the client.
backlog = 1
size = 1024
data_bpm = 0
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("Starting")

client, address = s.accept()
print("Outside while loop")


class UserInputPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("User Information")
        self.geometry("500x400")
        
        tk.Label(self, text="Let's get to know you better!!").pack(pady=10)
        
        tk.Label(self, text="Enter your name and age to start..").pack(pady=10)

        tk.Label(self, text="Enter Your Name:").pack(pady=10)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        tk.Label(self, text="Enter Your Age:").pack(pady=10)
        self.age_entry = tk.Entry(self)
        self.age_entry.pack(pady=5)
        
        tk.Label(self, text="Get in contact with the sensor").pack(pady=10)
        
        tk.Label(self, text="Click on submit, and push the button once you are ready").pack(pady=10)

        submit_button = tk.Button(self, text="Submit", command=self.submit_user_info)
        submit_button.pack(pady=10)

    def submit_user_info(self):
        user_name = self.name_entry.get()
        user_age = self.age_entry.get()

        if user_name and user_age:
            self.destroy()  # Close the user input page
            app = PulseMonitoringApp(user_name, user_age)
            flag = False
            cnt = 0
            while 1:
                data = client.recv(size)
                heart_rate = data.decode()
                print(heart_rate)
                if heart_rate.startswith('B'):
                    flag = True
                    # display/update heart rate in bpm
                    if cnt < 2:
                        cnt = cnt + 1
                        flag = False
                    heart_rate = heart_rate[4:]
                else:
                    flag = False
                    heart_rate = int(heart_rate)
                app.update_bargraph(heart_rate, flag,user_name,user_age)
                app.update_idletasks()
                app.update()

                if data:
                    print("Received data:", heart_rate)


class PulseMonitoringApp(tk.Tk):
    def __init__(self, user_name, user_age):
        super().__init__()
        self.title("Pulse Monitoring System")

        # Configure resizing behavior
        self.grid_columnconfigure(0, weight=28)
        self.grid_columnconfigure(1, weight=32)
        self.rowconfigure(0, weight=3)
        
        # Gradient background
        self.create_gradient_background()

#         # Create a Canvas for the gradient background
#         canvas = tk.Canvas(self, width=800, height=600, highlightthickness=0)
#         canvas.grid(row=0, column=0, columnspan=2, rowspan=5, sticky="nsew")

#         # Create a gradient background
#         gradient = tk.PhotoImage(width=1, height=1)
#         gradient.put("#ff0000", (0, 0))
#         gradient.put("#ff7f7f", (0, 1))
#         gradient.put("#ffffff", (0, 2))
#         canvas.create_image(0, 0, anchor=tk.NW, image=gradient)

        # Load and resize the logo
        original_logo = Image.open("/home/pi/Downloads/heartRateLogo.png")
        resized_logo = original_logo.resize((40, 40), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(resized_logo)

        # Display the resized logo
        self.logo_label = tk.Label(self, image=self.logo)
        self.logo_label.grid(row=0, column=0, pady=10, sticky="e")

        # Display the title label
        title_label = tk.Label(self, text="Pulse Monitoring System", font=("Helvetica", 16),fg='white')
        title_label.grid(row=0, column=1, pady=10, padx=20, sticky="w")
        title_label.configure(bg=self.get_gradient_color(0))  # Set background color


        # Matplotlib graph (compressed to 75%)
        self.fig, self.ax = plt.subplots(figsize=(6, 4), dpi=75)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=1, column=0, pady=10, padx=30, sticky="nsew", columnspan=2)
        self.canvas_widget.configure(bg=self.get_gradient_color(1))  # Set background color

        # Heart rate data (initialize with zeros)
        self.heart_rate_data = np.zeros(60)
        self.line, = self.ax.plot(np.arange(60), self.heart_rate_data, label="Heart Rate", color='white')
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Heart Rate")
        self.ax.patch.set_facecolor(self.get_gradient_color(2))  # Set background color

#         # Add reference lines for normal resting heart rate range
#         self.ax.axhline(y=60, color='r', linestyle='--', label='Lower Limit (60 bpm)')
#         self.ax.axhline(y=100, color='g', linestyle='--', label='Upper Limit (100 bpm)')

        # Move legend to top-right and decrease its size by 30%
        self.ax.legend(loc='upper right', fontsize='xx-small', edgecolor='black')

        # Set y-axis limits to accommodate values above 120
        self.ax.set_ylim(0, 250)  # Adjust the upper limit as needed

        # Heart rate value label with increased font size and font weight
        self.bpm_label = tk.Label(self, text="", font=("Helvetica", 20, "bold"),fg='white')
        self.bpm_label.grid(row=2, column=0, pady=5, columnspan=2, sticky="nsew")
        self.bpm_label.configure(bg=self.get_gradient_color(3))  # Set background color


        # Toggleable text section
        self.show_text = False
        self.button = tk.Button(self, text="Standard Info", command=self.toggle_text)
        self.button.grid(row=4, column=0, pady=10, columnspan=2, sticky="w")

        self.text_label = tk.Label(self, text="", anchor=tk.W, justify=tk.LEFT,fg='white')
        self.text_label.grid(row=5, column=0, pady=10, columnspan=2, sticky="w")
        self.text_label.configure(bg=self.get_gradient_color(4))  # Set background color

        self.res_label = tk.Label(self, text="", anchor=tk.W, justify=tk.LEFT, font=("Helvetica", 15), fg='white')
        self.res_label.grid(row=3, column=0, pady=10, columnspan=2, sticky="w")
        self.res_label.configure(bg=self.get_gradient_color(3))  # Set background color
        
        # Update graph with user information
        self.update_bargraph(0, False, user_name, user_age)

    def create_gradient_background(self):
        canvas = tk.Canvas(self, width=1200, height=400)
        canvas.grid(row=0, column=0, rowspan=7, columnspan=3, sticky="nsew")

        for i in range(self.winfo_screenwidth()):
            r = int(i / self.winfo_screenwidth() * 127) + 128
            hex_color = "#{:02x}{:02x}{:02x}".format(r, int(0.5 * r), int(0.5 * r))
            canvas.create_line(i, 0, i, self.winfo_screenheight(), fill=hex_color)
 
    def get_gradient_color(self, segment):
        r = int(segment / 5 * 127) + 128  # Adjust multiplier and constant to control brightness
        return "#{:02x}{:02x}{:02x}".format(r, int(0.5 * r), int(0.5 * r))           

    def toggle_text(self):
        self.show_text = not self.show_text

        if self.show_text:
            info_text = (
                "Your pulse rate, also known as your heart rate, is the number of times your heart beats per minute.\n"
                "A normal resting heart rate should be between 60 to 100 beats per minute, but it can vary from minute to minute.\n"
                "Your age and general health can also affect your pulse rate, so itÃ¢â‚¬â„¢s important to remember that a Ã¢â‚¬ËœnormalÃ¢â‚¬â„¢ pulse can vary from person to person."
            )
            self.text_label.config(text=info_text)
        else:
            self.text_label.config(text="")

    def update_bargraph(self, new_data, flag, user_name, user_age):
        # Update the heart rate data
        self.heart_rate_data = np.roll(self.heart_rate_data, -1)
        self.heart_rate_data[-1] = new_data

        # Update the line plot data
        self.line.set_ydata(self.heart_rate_data)

        if flag:
            data_bpm = new_data
            # Update the heart rate value label
            self.bpm_label.config(text=f"Heart Rate: {int(data_bpm)} bpm")
            # Update the status label based on age and heart rate
            if int(user_age) >= 10 and 60 <= int(data_bpm) <= 100:
                status_text = f"Your heart rate is normal for age {user_age}."
                       # Add reference lines for normal resting heart rate range
                self.ax.axhline(y=60, color='r', linestyle='--', label='Lower Limit (60 bpm)')
                self.ax.axhline(y=100, color='g', linestyle='--', label='Upper Limit (100 bpm)')
            elif int(user_age) < 10 and 70 <= int(data_bpm) <= 110:
                status_text = f"Your heart rate is normal for age {user_age}."
            elif user_age is not None:
                status_text = f"Your heart rate is not within the normal range for age {user_age}."
#                 for line in self.ax.axhline:
#                     if line.get_ydata()[0] == 60 or line.get_ydata()[0] == 100:
#                         line.remove()
               # self.ax.axhline.remove()
            else:
                status_text = "Your heart rate status is unknown."
            self.res_label.config(text=status_text)
        # Redraw the canvas
        self.canvas.draw()

        # Update the title with user information
        self.title(f"Pulse Monitoring System - {user_name}, {user_age} years old")


if __name__ == "__main__":
    user_input_page = UserInputPage()
    user_input_page.mainloop()
