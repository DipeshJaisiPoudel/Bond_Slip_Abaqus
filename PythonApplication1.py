import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import simpledialog

def tau_b(s2, tau_max, s_peak, sR):
    if 0 <= s2 < 0.1 * s_peak:
        return 3.0 * tau_max / s_peak * s2
    elif 0.1 * s_peak <= s2 < s_peak:
        return tau_max * (0.75 - 0.45 * ((s2 - s_peak) / (0.9 * s_peak)) ** 4)
    elif s_peak <= s2 < 1.1 * s_peak:
        return 0.75 * tau_max
    elif 1.1 * s_peak <= s2 < sR:
        return 0.75 * tau_max * (1 - (s2 - 1.1 * s_peak) / (sR - 1.1 * s_peak))
    else:
        return 0

def tau_f(s2, tau_max, s_peak):
    if 0 <= s2 < 0.1 * s_peak:
        return tau_max * s2 / s_peak
    elif 0.1 * s_peak <= s2 < s_peak:
        return tau_max * (0.25 - 0.15 * ((s2 - s_peak) / (0.9 * s_peak)) ** 4)
    else:
        return 0.25 * tau_max

# Create a simple Tkinter dialog to get input values
root = tk.Tk()
root.withdraw()  # Hide the root window

try:
    db = float(simpledialog.askstring("Input", "Enter the diameter of rebar (in millimeters):"))
    f_c = float(simpledialog.askstring("Input", "Enter the concrete strength (in N/mm²):"))
except ValueError:
    print("Invalid input. Please enter numerical values.")
    sys.exit(1)

# Calculate example parameters
s_peak = 0.07 * db  # Example value based on rebar diameter
tau_max = 1.163 * (f_c ** (3/4))  # For concrete with f'c = f_c N/mm²
sR = 0.5 * db  # Example value (usually 40% to 60% of bar diameter)

# Generate slip values
s2_values = np.linspace(0, sR + 1, 50)  # Reduced to 50 data points

# Calculate tau_b, tau_f and combined values
tau_b_values = [tau_b(s2, tau_max, s_peak, sR) for s2 in s2_values]
tau_f_values = [tau_f(s2, tau_max, s_peak) for s2 in s2_values]
tau_combined_values = [tau_b_val + tau_f_val for tau_b_val, tau_f_val in zip(tau_b_values, tau_f_values)]

# Create a DataFrame to store the data
data = {
    'Slip (s2) [mm]': s2_values,
    'τ_b(s2) [N/mm²]': tau_b_values,
    'τ_f(s2) [N/mm²]': tau_f_values,
    'τ_combined(s2) [N/mm²]': tau_combined_values
}

df = pd.DataFrame(data)

# Create directory if it doesn't exist
output_dir = r'E:\Bond Slip'
os.makedirs(output_dir, exist_ok=True)

# Save the DataFrame to a CSV file
csv_file_path = os.path.join(output_dir, 'bond_friction_resistance.csv')
df.to_csv(csv_file_path, index=False)

print(f"CSV file saved as '{csv_file_path}'")

# Plotting the graphs
plt.figure(figsize=(10, 6))
plt.plot(s2_values, tau_b_values, label='τ_b(s2)', color='blue')
plt.plot(s2_values, tau_f_values, label='τ_f(s2)', color='red', linestyle='--')
plt.plot(s2_values, tau_combined_values, label='τ_combined(s2)', color='green', linestyle=':')

# Add labels and title
plt.xlabel('Slip (s2) [mm]')
plt.ylabel('Stress (τ) [N/mm²]')
plt.title('Bond and Friction Resistance as a Function of Slip')
plt.legend()

# Show grid
plt.grid(True)

# Display the plot
plt.show()

