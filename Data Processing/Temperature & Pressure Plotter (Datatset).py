import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

time = []
pressure = []
temp1 = []
temp2 = []

def read_csv_file(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                pressure_data= row[1]  #kolompositie van de luchtdruk
                temp1_data = row[2] #kolompositie van de temperatuur 1
                temp2_data = row[3] #kolompositie van de temperatuur 2
                time_data = row[4] #kolompositie van de tijd
                pressure.append(pressure_data)
                temp1.append(temp1_data)
                temp2.append(temp2_data)
                time.append(time_data)

    except FileNotFoundError:
        print(f"File {file_path} not found.")
        
# Read and define file(name)
file_path = 'measurements.csv'
read_csv_file(file_path)

#Define plot
plt.figure(figsize=(12, 10))
plt.subplot(2, 2, 1)
plt.plot(time, temp1, marker='o', color='blue')
plt.title('Temperature 1 over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')

plt.subplot(2, 2, 2)
plt.plot(time, temp2, marker='o', color='green')
plt.title('Temperature 2 over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Temperature (°C)')

plt.subplot(2, 2, 3)
plt.plot(time, pressure, marker='o', color='red')
plt.title('Pressure over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Pressure (Pa)')

#naming and saving the file
filename = "Temp+Press over time.png"
plt.savefig(filename)
plt.close()

# Create window with message "all done!"
root = tk.Tk()
root.title("Height")
label = tk.Label(root, text="All done!")
label.pack(padx=100, pady=100)
root.mainloop()
