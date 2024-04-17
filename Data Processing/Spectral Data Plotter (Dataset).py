import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

heights_dropdown = []
spectrums = []
wavelengths = [410, 435, 460, 485, 510, 535, 560, 585, 610, 645, 680, 705, 730, 760, 810, 860, 900, 940]

def read_csv_file(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                height = row[0]
                heights_dropdown.append(height)
                spectrum_strings = row[1:30]
                spectrum_floats = [float(x) for x in spectrum_strings]
                spectrums.append(spectrum_floats)
                plot_spectrum(spectrum_floats, height)
                print("Generating for:", height, "m")
    except FileNotFoundError:
        print(f"File {file_path} not found.")

def plot_spectrum(spectrums, height):
    plt.plot(wavelengths, spectrums)
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Counts/Intensity")
    plt.title(f"Spectral Measurements For Height: {height} m")
    filename = f"Plot For Height "+str(height)+"m.png"
    plt.savefig(filename)
    plt.close()

# Read and define file(name)
file_path = 'measurements.csv'
read_csv_file(file_path)

# Create window with message "all done!"
root = tk.Tk()
root.title("Height")
label = tk.Label(root, text="All done!")
label.pack(padx=100, pady=100)
root.mainloop()