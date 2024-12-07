import tkinter as tk
from tkinter import ttk
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def run_eof_window():
    # Function to run the quantum circuit simulation
    def run_quantum_circuit():
        try:
            # Get user inputs
            num_qubits = int(qubits_entry.get())
            num_shots = int(shots_entry.get())
            operation = operation_combobox.get()

            # Create the quantum circuit
            qc = QuantumCircuit(num_qubits, num_qubits)

            # Apply the selected operation
            if operation == 'Hadamard':
                qc.h(range(num_qubits))  # Hadamard gate on all qubits
            elif operation == 'Pauli-X':
                qc.x(range(num_qubits))  # Pauli-X gate on all qubits
            else:
                result_label.config(text="Operation not recognized. Proceeding with Hadamard gate.")
                qc.h(range(num_qubits))

            # Measure the qubits
            qc.measure(range(num_qubits), range(num_qubits))

            # Display the quantum circuit
            qc_text.delete(1.0, tk.END)
            qc_text.insert(tk.END, qc.draw())

            # Simulate the quantum circuit
            sim = AerSimulator()
            result = sim.run(qc, shots=num_shots).result()
            counts = result.get_counts()

            # Display the measurement results
            result_label.config(text="Measurement Results (Counts):\n" + str(counts))

            # Plot the histogram of the results
            ax.clear()  # Clear the previous plot
            plot_histogram(counts, ax=ax)  # Plot the new histogram

            # Update the canvas with the new plot
            canvas.draw()

        except ValueError:
            result_label.config(text="Please enter valid numbers for qubits and shots.")

    # Create the main window for the quantum circuit simulator
    window = tk.Tk()
    window.title("Quantum Circuit Simulator")

    # Create the widgets
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

    run_button = ttk.Button(window, text="Run Simulation", command=run_quantum_circuit)
    run_button.grid(row=3, column=0, columnspan=2, pady=10)

    qc_text_label = ttk.Label(window, text="Quantum Circuit:")
    qc_text_label.grid(row=4, column=0, columnspan=2)

    qc_text = tk.Text(window, height=10, width=40)
    qc_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    result_label = ttk.Label(window, text="Measurement Results:")
    result_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    # Create a Matplotlib figure for the histogram
    fig, ax = plt.subplots(figsize=(5, 4))

    # Create a Tkinter canvas to display the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(row=7, column=0, columnspan=2)

    # Start the Tkinter event loop for the quantum circuit window
    window.mainloop()