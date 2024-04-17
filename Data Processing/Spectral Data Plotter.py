import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt



#import numpy as np

heights = []
spectrums = []
wavelengths = [410,435,460,485,510,535,560,585,610,645,680,705,730,760,810,860,900,940]


def read_csv_file(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                heights.append(row[0])
                spectrum_strings = row[1:30]
                spectrum_floats = [float(x) for x in spectrum_strings] 
                spectrums.append(spectrum_floats)
                print(type(spectrums[0][0]))
                #print(row)
    except FileNotFoundError:
        print(f"File {file_path} not found.")


def button_click():
    selected_item = dropdown.get()
    index = heights.index(selected_item)
    plot_spectrum(spectrums[index],selected_item)
    print(index)
    print("Selected item:", selected_item)
    

def plot_spectrum(s, h):
    plt.plot(wavelengths, s)
    plt.xlabel("wavelength in nm")
    plt.ylabel("counts")
    plt.title("Spectral Measurements")
    filename="Plot Results Height = "+str(h)+".png"
    # Saving the plot as a .png file
    plt.savefig(filename)
    plt.show()
    
    
    
# Read file
file_path = 'measurements.csv'  # Replace 'example.csv' with your CSV file path
read_csv_file(file_path)

# Create the main window
root = tk.Tk()
root.title("Height")

# Create a dropdown box
options = heights
dropdown = ttk.Combobox(root, values=options)
dropdown.pack(side=tk.LEFT, padx=5, pady=5)

# Create a button
button = tk.Button(root, text="Next", command=button_click)
button.pack(side=tk.LEFT, padx=5, pady=5)




# Run the main event loop
root.mainloop()



