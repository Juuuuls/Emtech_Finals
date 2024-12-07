# sqb_h.py
import tkinter as tk
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Initialize the quantum simulator and circuit
sim = AerSimulator()
qc = QuantumCircuit(1, name="kuyajqsi")

# Function to update the visualization
def update_visualization(window):
    global qc
    qc.save_statevector()  # Save the statevector after any gate is applied
    result = sim.run(qc).result()  # Run the quantum circuit on the simulator
    state = result.data(qc)["statevector"]  # Retrieve the statevector
    
    # Update Bloch sphere with the current statevector
    fig = plot_bloch_multivector(state)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=5)

# Button functions
def apply_h(window):
    global qc
    qc = QuantumCircuit(1, name="kuyajqsi")  # Reset circuit to ensure a clean start
    qc.h(0)  # Apply Hadamard gate to qubit 0
    update_visualization(window)  # Update the Bloch sphere with the new state

def reset_circuit(window):
    global qc
    qc = QuantumCircuit(1, name="kuyajqsi")  # Reset the circuit to initial state
    update_visualization(window)  # Update the Bloch sphere with the reset state

# Function to create and run the quantum circuit window (called by main.py)
def run_sqb_window():
    window = tk.Toplevel()  # Create a new window (like a new page)
    window.title("Quantum Circuit Simulator")
    window.geometry("800x600")

    # Create buttons for the interface
    tk.Button(window, text="Apply Hadamard", command=lambda: apply_h(window), width=15).grid(row=0, column=0)
    tk.Button(window, text="Reset Circuit", command=lambda: reset_circuit(window), width=15).grid(row=0, column=1)

    # Initial visualization to show the starting state (|0⟩)
    update_visualization(window)

    # Run the application for this window
    window.mainloop()
