import csv
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

heights_dropdown = []
spectrums = []
wavelengths = [410,435,460,485,510,535,560,585,610,645,680,705,730,760,810,860,900,940]


def read_csv_file(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                heights_dropdown.append(row[0]) #Definieer in welke kolompositie de hoogte staat in de dataset
                spectrum_strings = row[1:30]
                spectrum_floats = [float(x) for x in spectrum_strings] 
                spectrums.append(spectrum_floats)
                #print(type(spectrums[0][0]))
                #print(row)
    except FileNotFoundError:
        print(f"File {file_path} not found.")


def button_click():
    height = dropdown.get()
    index = heights_dropdown.index(height)
    plot_spectrum(spectrums[index],height)
    #print(index)
    print("Height:", height, "m")
    

def plot_spectrum(spectrums, height):
    plt.plot(wavelengths, spectrums)
    plt.xlabel("wavelength in nm")
    plt.ylabel("counts/intensity")
    plt.title("Spectral Measurements")
    filename="Plot For Height = "+str(height)+"m.png" # Saving the plot as a .png file
    plt.savefig(filename)
    plt.show()
    plt.close()

# Read file
file_path = 'measurements.csv'# Replace with CSV file 
read_csv_file(file_path)

# Create the main window
root = tk.Tk()
root.title("Height")

# Create a dropdown box
options = heights_dropdown
dropdown = ttk.Combobox(root, values=options)
dropdown.pack(side=tk.LEFT, padx=30, pady=30)

# Create a button
button = tk.Button(root, text="Next", command=button_click)
button.pack(side=tk.LEFT, padx=30, pady=30)




# Run the main event loop
root.mainloop()



