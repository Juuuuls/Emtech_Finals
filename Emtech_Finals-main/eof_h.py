import tkinter as tk
from tkinter import ttk
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random
import main

def run_eof_window():
    """Function to create the quantum circuit page with modern styling."""
    window = tk.Toplevel()
    window.title("Quantum Circuit Simulator")
    window.configure(bg="#2b2d42")  # Dark modern background

    def run_quantum_circuit():
        try:
            num_qubits = int(qubits_entry.get())
            num_shots = int(shots_entry.get())
            operation = operation_combobox.get()
            noise_level = noise_slider.get()  # Get the noise level from the slider

            # Create the quantum circuit
            qc = QuantumCircuit(num_qubits, num_qubits)

            # Apply the selected quantum operation
            if operation == 'Hadamard':
                qc.h(range(num_qubits))
            elif operation == 'Pauli-X':
                qc.x(range(num_qubits))
            else:
                result_label.config(text="Operation not recognized. Proceeding with Hadamard gate.")
                qc.h(range(num_qubits))

            # Measure the qubits
            qc.measure(range(num_qubits), range(num_qubits))

            # Display the quantum circuit in text form
            qc_text.delete(1.0, tk.END)
            qc_text.insert(tk.END, qc.draw())

            # Set up the simulator
            sim = AerSimulator()
            result = sim.run(qc, shots=num_shots).result()
            counts = result.get_counts()

            # Simulate noise: Introduce bit-flip noise based on the slider value
            noisy_counts = simulate_noise(counts, noise_level=noise_level)

            # Update the result with noisy counts
            result_label.config(text="Measurement Results (Counts):\n" + str(noisy_counts))

            # Plot the noisy result
            ax.clear()
            plot_histogram(noisy_counts, ax=ax)
            canvas.draw()

        except ValueError:
            result_label.config(text="Please enter valid numbers for qubits and shots.")

    def simulate_noise(counts, noise_level=0.1):
        """Simulate bit-flip noise by randomly flipping the bits in the counts dictionary."""
        noisy_counts = {}
        for key, value in counts.items():
            # Introduce noise by flipping each bit in the string with a probability of `noise_level`
            noisy_key = ''.join(
                [bit if random.random() > noise_level else str(1 - int(bit)) for bit in key]
            )
            if noisy_key in noisy_counts:
                noisy_counts[noisy_key] += value
            else:
                noisy_counts[noisy_key] = value
        return noisy_counts

    # Frame with modern styling
    controls_frame = tk.Frame(window, bd=2, relief="sunken", padx=10, pady=10, bg="#8d99ae")
    controls_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    visualization_frame = tk.Frame(window, bd=2, relief="sunken", padx=10, pady=10, bg="#edf2f4")
    visualization_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Add input components to controls_frame
    label_style = {"font": ("Helvetica", 12), "fg": "#edf2f4", "bg": "#8d99ae"}
    qubits_label = tk.Label(controls_frame, text="Number of Qubits:", **label_style)
    qubits_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    qubits_entry = tk.Entry(controls_frame, font=("Helvetica", 12))
    qubits_entry.grid(row=0, column=1, padx=10, pady=10)

    shots_label = tk.Label(controls_frame, text="Number of Shots:", **label_style)
    shots_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    shots_entry = tk.Entry(controls_frame, font=("Helvetica", 12))
    shots_entry.grid(row=1, column=1, padx=10, pady=10)

    operation_label = tk.Label(controls_frame, text="Quantum Operation:", **label_style)
    operation_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    operation_combobox = ttk.Combobox(controls_frame, values=["Hadamard", "Pauli-X"], font=("Helvetica", 12))
    operation_combobox.grid(row=2, column=1, padx=10, pady=10)

    noise_label = tk.Label(controls_frame, text="Noise Level: 0.0", **label_style)
    noise_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

    def update_noise_label(val):
        noise_label.config(text=f"Noise Level: {float(val):.2f}")

    noise_slider = ttk.Scale(controls_frame, from_=0, to=1, orient="horizontal", command=update_noise_label)
    noise_slider.set(0.1)
    noise_slider.grid(row=3, column=1, padx=10, pady=10)

    button_style = {
        "font": ("Helvetica", 12),
        "bg": "#ef233c",
        "fg": "#edf2f4",
        "activebackground": "#d90429",
        "activeforeground": "#edf2f4",
        "relief": "flat",
        "width": 20
    }

    run_button = tk.Button(controls_frame, text="Run Simulation", command=run_quantum_circuit, **button_style)
    run_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Add visualization components to visualization_frame
    qc_text_label = tk.Label(visualization_frame, text="Quantum Circuit:", font=("Helvetica", 12, "bold"), fg="#2b2d42", bg="#edf2f4")
    qc_text_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    qc_text = tk.Text(visualization_frame, height=10, width=60, font=("Courier", 12), bg="#f8f9fa", fg="#2b2d42")
    qc_text.grid(row=1, column=0, padx=10, pady=10)

    result_label = tk.Label(visualization_frame, text="Measurement Results:", font=("Helvetica", 12, "bold"), fg="#2b2d42", bg="#edf2f4")
    result_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    fig, ax = plt.subplots(figsize=(4, 3))
    canvas = FigureCanvasTkAgg(fig, visualization_frame)
    canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)

    def return_to_main_menu():
        """Returns to the main menu."""
        window.destroy()
        main.Application().mainloop()

    button_close = tk.Button(controls_frame, text="Return to Main Menu", command=return_to_main_menu, **button_style)
    button_close.grid(row=5, column=0, columnspan=2, pady=10)

    window.mainloop()