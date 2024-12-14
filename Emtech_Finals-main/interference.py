import tkinter as tk
from tkinter import ttk, messagebox
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import main

def run_interference_circuit(): 
    # Function to run the simulation
    def run_simulation():
        try:
            num_qubits = int(qubits_entry.get())
            num_shots = int(shots_entry.get())
            apply_pauli_x = pauli_x_var.get() 
            apply_hadamard = hadamard_var.get()  # Get the state of the Hadamard checkbox
            apply_cnot = cnot_var.get()  # Get the state of the CNOT checkbox
            noise_level = noise_slider.get()  # Get the noise level from the slider

            # Create the quantum circuit
            qc = QuantumCircuit(num_qubits, num_qubits)

            # Apply Hadamard gate to all qubits if selected
            if apply_hadamard:
                qc.h(range(num_qubits))

            if apply_pauli_x:
                qc.x(range(num_qubits))

            # Apply the CNOT gates if selected
            if apply_cnot:
                for i in range(num_qubits - 1):
                    qc.cx(i, i + 1)

            # Simulate noise by randomly flipping qubits based on noise level
            if noise_level > 0:
                for qubit in range(num_qubits):
                    if random.random() < noise_level:
                        qc.x(qubit)  # Apply X gate (flip) as noise

            # Measure the qubits
            qc.measure(range(num_qubits), range(num_qubits))

            # Display the quantum circuit in text form
            qc_text.delete(1.0, tk.END)
            qc_text.insert(tk.END, qc.draw())

            # Set up the simulator
            sim = AerSimulator()
            result = sim.run(qc, shots=num_shots).result()
            counts = result.get_counts()

            # Update the result with counts
            result_label.config(text="Measurement Results (Counts):\n" + str(counts))

            # Plot the results
            ax.clear()
            plot_histogram(counts, ax=ax)
            canvas.draw()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for qubits and shots.")

    # Function to update the noise level label
    def update_noise_label(val):
        try:
            # Convert the string value to a float before formatting
            float_val = float(val)
            noise_label.config(text=f"Noise Level: {float_val:.2f}")
        except ValueError:
            noise_label.config(text="Noise Level: Invalid")

    # Create a new Tkinter window for the interference simulation
    root = tk.Toplevel()
    root.title("Quantum Interference Simulation")
    root.configure(bg="#2b2d42")  # Dark modern background

    # Full screen window setup
    root.attributes("-fullscreen", True)  # Set the window to fullscreen
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))  # Escape to exit fullscreen

    # Frame for the controls and simulation results
    content_frame = tk.Frame(root, bd=2, relief="sunken", padx=10, pady=10, bg="#edf2f4")
    content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    controls_frame = tk.Frame(root, bd=2, relief="sunken", padx=10, pady=10, bg="#8d99ae")
    controls_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    label_style = {"font": ("Helvetica", 12), "fg": "#edf2f4", "bg": "#8d99ae"}

    qubits_label = tk.Label(controls_frame, text="Number of Qubits:", **label_style)
    qubits_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    qubits_entry = tk.Entry(controls_frame, font=("Helvetica", 12))
    qubits_entry.grid(row=0, column=1, padx=10, pady=10)

    shots_label = tk.Label(controls_frame, text="Number of Shots:", **label_style)
    shots_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    shots_entry = tk.Entry(controls_frame, font=("Helvetica", 12))
    shots_entry.grid(row=1, column=1, padx=10, pady=10)

    # Checkboxes with color customization
    checkbox_style = {"font": ("Helvetica", 12), "fg": "#edf2f4", "bg": "#8d99ae", "selectcolor": "#2b2d42"}

    hadamard_var = tk.BooleanVar(value=True)  # Default to True (Hadamard applied)
    hadamard_check = tk.Checkbutton(controls_frame, text="Apply Hadamard Gate", variable=hadamard_var, **checkbox_style)
    hadamard_check.grid(row=2, column=0, columnspan=2, pady=10)

    cnot_var = tk.BooleanVar(value=True)  # Default to True (CNOT applied)
    cnot_check = tk.Checkbutton(controls_frame, text="Apply CNOT Gates", variable=cnot_var, **checkbox_style)
    cnot_check.grid(row=3, column=0, columnspan=2, pady=10)
      # Add Pauli-X Gate Checkbox
    pauli_x_var = tk.BooleanVar(value=False)  # Default to False (Pauli-X not applied)
    pauli_x_check = tk.Checkbutton(controls_frame, text="Apply Pauli-X Gate", variable=pauli_x_var, **checkbox_style)
    pauli_x_check.grid(row=4, column=0, columnspan=2, pady=10)

    # Noise Level Slider
    noise_label = tk.Label(controls_frame, text="Noise Level: 0.00", **label_style)
    noise_label.grid(row=5,column=0, padx=10, pady=10, sticky="e")

    noise_slider = ttk.Scale(controls_frame, from_=0, to=1, orient="horizontal", command=update_noise_label)
    noise_slider.set(0)  # Default noise level is 0
    noise_slider.grid(row=5,column=1, padx=10, pady=10)

    button_style = {
        "font": ("Helvetica", 12),
        "bg": "#ef233c",
        "fg": "#edf2f4",
        "activebackground": "#d90429",
        "activeforeground": "#edf2f4",
        "relief": "flat",
        "width": 20
    }

    run_button = tk.Button(controls_frame, text="Run Simulation", command=run_simulation, **button_style)
    run_button.grid(row=6,column=0, columnspan=2, pady=10)

    def return_to_main_menu():
        """Returns to the main menu."""
        root.destroy()  # Close the current window
        main.Application().mainloop()  # Reopen the main menu

    button_close = tk.Button(controls_frame, text="Return to Main Menu", command=return_to_main_menu, **button_style)
    button_close.grid(row=7,column=0, columnspan=2, pady=10)

    # Frame for the visualizations (Quantum Circuit, Results, Histogram)
    visualization_frame = tk.Frame(content_frame, bd=2, relief="sunken", padx=10, pady=10, bg="#edf2f4")
    visualization_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

    # Quantum Circuit Display
    qc_text_label = tk.Label(visualization_frame, text="Quantum Circuit:", font=("Helvetica", 12, "bold"), fg="#2b2d42", bg="#edf2f4")
    qc_text_label.grid(row=0, column=0, columnspan=2)

    qc_text = tk.Text(visualization_frame, height=10, width=40, font=("Courier", 12), bg="#f8f9fa", fg="#2b2d42")
    qc_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    result_label = tk.Label(visualization_frame, text="Measurement Results:", font=("Helvetica", 12, "bold"), fg="#2b2d42", bg="#edf2f4")
    result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Set up the plot for the histogram (smaller size)
    fig, ax = plt.subplots(figsize=(4, 3))  # Reduced the figure size
    canvas = FigureCanvasTkAgg(fig, visualization_frame)
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

    # Run the tkinter main loop
    root.mainloop()
