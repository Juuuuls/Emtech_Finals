import tkinter as tk
from tkinter import messagebox
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, pauli_error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_circuit():
    try:
        # Get user inputs
        num_qubits = int(entry_qubits.get())
        if num_qubits < 1:
            raise ValueError("Number of qubits must be at least 1.")

        apply_h = h_var.get()
        apply_cx = cx_var.get()
        apply_x = x_var.get()
        pauli_x_qubit = int(entry_pauli_x.get()) if apply_x else -1
        noise_level = noise_slider.get()  # Get the noise level from the slider

        if apply_x and (pauli_x_qubit < 0 or pauli_x_qubit >= num_qubits):
            raise ValueError("Pauli-X qubit index is out of range.")

        # Create quantum circuit
        qc = QuantumCircuit(num_qubits)
        if apply_h:
            qc.h(0)  # Apply Hadamard gate to the first qubit
        if apply_cx:
            if num_qubits < 2:
                raise ValueError("CNOT requires at least 2 qubits.")
            qc.cx(0, 1)  # Apply CNOT between qubit 0 and qubit 1
        if apply_x:
            qc.x(pauli_x_qubit)  # Apply Pauli-X gate to the selected qubit
        qc.measure_all()  # Add measurement gates to all qubits

        # Incorporate noise if the noise level is greater than 0
        if noise_level > 0:
            noise_model = NoiseModel()
            error = pauli_error([('X', noise_level), ('I', 1 - noise_level)])  # Pauli-X noise
            for qubit in range(num_qubits):
                noise_model.add_all_qubit_quantum_error(error, ['x'])  # Apply noise to X gates

            # Simulate the circuit with noise
            sim = AerSimulator(noise_model=noise_model)
        else:
            sim = AerSimulator()  # Simulate without noise

        result = sim.run(qc).result()
        counts = result.get_counts()

        # Display the quantum circuit
        circuit_text.set(qc.draw())

        # Display results
        result_text.set(f"Measurement Counts:\n{counts}")
        
        # Clear any previous plots
        for widget in frame_plot.winfo_children():
            widget.destroy()
        
        # Plot histogram
        fig = plot_histogram(counts, title="Measurement Results")
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the GUI
root = tk.Tk()
root.title("Quantum Circuit GUI")
root.geometry("1800x1800")  # Set window size to 1800x1800 pixels

# Input section
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Number of Qubits:").grid(row=0, column=0, padx=5, pady=5)
entry_qubits = tk.Entry(frame_input)
entry_qubits.grid(row=0, column=1, padx=5, pady=5)

h_var = tk.BooleanVar()
tk.Checkbutton(frame_input, text="Apply Hadamard (H) to Qubit 0", variable=h_var).grid(row=1, columnspan=2, pady=5)

cx_var = tk.BooleanVar()
tk.Checkbutton(frame_input, text="Apply CNOT (CX) between Qubit 0 and Qubit 1", variable=cx_var).grid(row=2, columnspan=2, pady=5)

x_var = tk.BooleanVar()
tk.Checkbutton(frame_input, text="Apply Pauli-X", variable=x_var).grid(row=3, column=0, pady=5)
tk.Label(frame_input, text="Pauli-X Qubit Index:").grid(row=3, column=1, padx=5)
entry_pauli_x = tk.Entry(frame_input)
entry_pauli_x.grid(row=3, column=2, padx=5)

# Noise slider
tk.Label(frame_input, text="Noise Level (0.0 - 1.0):").grid(row=4, column=0, padx=5, pady=5)
noise_slider = tk.Scale(frame_input, from_=0.0, to_=1.0, orient=tk.HORIZONTAL, resolution=0.01)
noise_slider.set(0.0)  # Default value
noise_slider.grid(row=4, column=1, padx=5, pady=5)

tk.Button(frame_input, text="Generate Circuit", command=create_circuit).grid(row=5, columnspan=3, pady=10)

# Output section
frame_output = tk.Frame(root)
frame_output.pack(pady=10)

tk.Label(frame_output, text="Quantum Circuit:").pack(anchor="w")
circuit_text = tk.StringVar()
tk.Label(frame_output, textvariable=circuit_text, justify="left").pack(anchor="w")

tk.Label(frame_output, text="Results:").pack(anchor="w")
result_text = tk.StringVar()
tk.Label(frame_output, textvariable=result_text, justify="left").pack(anchor="w")

# Plot section
frame_plot = tk.Frame(root)
frame_plot.pack(pady=10)

# Run the GUI
root.mainloop()