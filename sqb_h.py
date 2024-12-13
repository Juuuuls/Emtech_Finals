# sqb_h.py
import tkinter as tk
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import main

# Initialize the quantum simulator and circuit
sim = AerSimulator()
qc = QuantumCircuit(1, name="kuyajqsi")

# Function to update the visualization
def update_visualization(window, frame_output):
    global qc
    qc.save_statevector()  # Save the statevector after any gate is applied
    result = sim.run(qc).result()  # Run the quantum circuit on the simulator
    state = result.data(qc)["statevector"]  # Retrieve the statevector
    
    # Update Bloch sphere with the current statevector
    fig = plot_bloch_multivector(state)
    canvas = FigureCanvasTkAgg(fig, master=frame_output)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

# Apply Hadamard gate to the current quantum circuit
def apply_hadamard(window, frame_output):
    global qc
    qc = QuantumCircuit(1, name="kuyajqsi")  # Reset circuit to ensure a clean start
    qc.h(0)  # Apply Hadamard gate to qubit 0
    update_visualization(window, frame_output)  # Update the Bloch sphere with the new state

# Reset circuit
def reset_circuit(window, frame_output):
    global qc
    qc = QuantumCircuit(1, name="kuyajqsi")  # Reset the circuit to initial state
    update_visualization(window, frame_output)  # Update the Bloch sphere with the reset state

# Function to create and run the quantum circuit window (called by main.py)
def run_sqb_window():
    window = tk.Toplevel()
    window.title("Quantum Circuit Simulator")
    window.configure(bg="#2b2d42")  # Dark modern background

    # Create frames for input and output
    frame_input = tk.Frame(window, bd=2, relief="sunken", padx=10, pady=10, bg="#8d99ae")
    frame_input.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    frame_output = tk.Frame(window, bd=2, relief="sunken", padx=10, pady=10, bg="#edf2f4")
    frame_output.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Define button style
    button_style = {
        "font": ("Helvetica", 12),
        "bg": "#ef233c",
        "fg": "#edf2f4",
        "activebackground": "#d90429",
        "activeforeground": "#edf2f4",
        "relief": "flat",
        "width": 20
    }

    # Button to apply the Hadamard gate
    button_apply_hadamard = tk.Button(frame_input, text="Apply Hadamard",
                                      command=lambda: apply_hadamard(window, frame_output),
                                      **button_style)
    button_apply_hadamard.grid(row=1, column=0, pady=10)

    # Button to reset the circuit
    button_reset = tk.Button(frame_input, text="Reset Circuit",
                             command=lambda: reset_circuit(window, frame_output),
                             **button_style)
    button_reset.grid(row=2, column=0, pady=10)

    # Button to return to the main menu
    def return_to_main_menu():
        """Returns to the main menu."""
        window.destroy()  # Close the current window
        main.Application().mainloop()  # Reopen the main menu

    button_close = tk.Button(frame_input, text="Return to Main Menu",
                             command=return_to_main_menu,
                             **button_style)
    button_close.grid(row=3, column=0, pady=10)

    # Add a header to the input frame
    label_header = tk.Label(frame_input, text="Quantum Circuit Controls",
                            font=("Helvetica", 14, "bold"), fg="#edf2f4", bg="#8d99ae")
    label_header.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    window.mainloop()