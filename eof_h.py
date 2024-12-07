import tkinter as tk
from tkinter import ttk
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

def run_eof_window():
    """Function to create the quantum circuit page."""
    window = tk.Tk()
    window.title("Quantum Circuit Simulator")

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

    # Create the GUI components
    qubits_label = ttk.Label(window, text="Number of Qubits:")
    qubits_label.grid(row=0, column=0, padx=10, pady=10)

    qubits_entry = ttk.Entry(window)
    qubits_entry.grid(row=0, column=1, padx=10, pady=10)

    shots_label = ttk.Label(window, text="Number of Shots:")
    shots_label.grid(row=1, column=0, padx=10, pady=10)

    shots_entry = ttk.Entry(window)
    shots_entry.grid(row=1, column=1, padx=10, pady=10)

    operation_label = ttk.Label(window, text="Quantum Operation:")
    operation_label.grid(row=2, column=0, padx=10, pady=10)

    operation_combobox = ttk.Combobox(window, values=["Hadamard", "Pauli-X"])
    operation_combobox.grid(row=2, column=1, padx=10, pady=10)

    noise_label = ttk.Label(window, text="Noise Level:")
    noise_label.grid(row=3, column=0, padx=10, pady=10)

    # Slider for controlling the noise level (from 0 to 1)
    noise_slider = ttk.Scale(window, from_=0, to_=1, orient='horizontal', length=200)
    noise_slider.set(0.1)  # Set the default noise level to 0.1 (10%)
    noise_slider.grid(row=3, column=1, padx=10, pady=10)

    run_button = ttk.Button(window, text="Run Simulation", command=run_quantum_circuit)
    run_button.grid(row=4, column=0, columnspan=2, pady=10)

    qc_text_label = ttk.Label(window, text="Quantum Circuit:")
    qc_text_label.grid(row=5, column=0, columnspan=2)

    qc_text = tk.Text(window, height=10, width=40)
    qc_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    result_label = ttk.Label(window, text="Measurement Results:")
    result_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # Set up the plot
    fig, ax = plt.subplots(figsize=(5, 4))
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(row=8, column=0, columnspan=2)

    # Run the tkinter main loop
    window.mainloop()
