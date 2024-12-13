import tkinter as tk
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector, plot_histogram, plot_state_city
from qiskit_aer import AerSimulator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import main  # Import main.py to reopen the main menu

# Quantum simulator
simulator = AerSimulator()

# Function to create and visualize the quantum circuit
def create_circuit_and_visualize(num_qubits, gate_type, target_qubit, text_output, frame_output):
    """Handles the creation of the quantum circuit and visualizes it."""
    try:
        num_qubits = int(num_qubits)
        target_qubit = int(target_qubit)
        
        if target_qubit >= num_qubits or target_qubit < 0:
            text_output.insert(tk.END, "Error: Target qubit must be within the range of available qubits.\n")
            return

        # Create the quantum circuit
        qc = QuantumCircuit(num_qubits)
        if gate_type.upper() == "H":
            qc.h(target_qubit)
        elif gate_type.upper() == "X":
            qc.x(target_qubit)
        elif gate_type.upper() == "Y":
            qc.y(target_qubit)
        elif gate_type.upper() == "Z":
            qc.z(target_qubit)
        else:
            text_output.insert(tk.END, f"Error: Unsupported gate type '{gate_type}'.\n")
            return

        # Save the circuit statevector and run the simulation
        qc.save_statevector()
        result = simulator.run(qc).result()
        statevector = result.get_statevector()

        # Clear previous visualizations
        for widget in frame_output.winfo_children():
            widget.destroy()

        # Visualize the quantum circuit
        circuit_fig = qc.draw(output='mpl')
        circuit_canvas = FigureCanvasTkAgg(circuit_fig, master=frame_output)
        circuit_canvas.draw()
        circuit_canvas.get_tk_widget().pack()

        # Visualizations based on qubit count
        if num_qubits <= 2:
            # Bloch sphere for single or two-qubit systems
            bloch_fig = plot_bloch_multivector(statevector)
            bloch_canvas = FigureCanvasTkAgg(bloch_fig, master=frame_output)
            bloch_canvas.draw()
            bloch_canvas.get_tk_widget().pack()
        
        # Probability histogram for all qubit counts
        probabilities = result.get_counts(qc)
        histogram_fig = plot_histogram(probabilities)
        histogram_canvas = FigureCanvasTkAgg(histogram_fig, master=frame_output)
        histogram_canvas.draw()
        histogram_canvas.get_tk_widget().pack()

        # For 3 or more qubits, add state vector visualization
        if num_qubits > 2:
            state_city_fig = plot_state_city(statevector)
            state_city_canvas = FigureCanvasTkAgg(state_city_fig, master=frame_output)
            state_city_canvas.draw()
            state_city_canvas.get_tk_widget().pack()

        # Show success message
        text_output.insert(tk.END, "Quantum circuit created and visualized successfully!\n")

    except Exception as e:
        text_output.insert(tk.END, f"Error: {str(e)}\n")

# Function to initialize the multi-qubit superposition window
def run_mqb_window():
    """Launches the Multi-Qubit Superposition window with modern styling."""
    root = tk.Toplevel()  # Use Toplevel to create a new window
    root.title("Multi-Qubit Superposition")
    root.configure(bg="#2b2d42")  # Dark modern background

    # Create frames for organizing the GUI
    frame_input = tk.Frame(root, bd=2, relief="sunken", padx=10, pady=10, bg="#8d99ae")
    frame_input.pack(side="left", fill="both", expand=True, padx=20, pady=20)

    frame_output = tk.Frame(root, bd=2, relief="sunken", padx=10, pady=10, bg="#edf2f4")
    frame_output.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Input fields in frame_input with modern styling
    label_qubits = tk.Label(frame_input, text="Number of Qubits:", 
                            font=("Helvetica", 12), fg="#edf2f4", bg="#8d99ae")
    label_qubits.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    entry_qubits = tk.Entry(frame_input, font=("Helvetica", 12))
    entry_qubits.grid(row=0, column=1, padx=10, pady=5)

    label_gate = tk.Label(frame_input, text="Gate Type (H, X, Y, Z, etc.):",
                          font=("Helvetica", 12), fg="#edf2f4", bg="#8d99ae")
    label_gate.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    entry_gate = tk.Entry(frame_input, font=("Helvetica", 12))
    entry_gate.grid(row=1, column=1, padx=10, pady=5)

    label_target = tk.Label(frame_input, text="Target Qubit:", 
                            font=("Helvetica", 12), fg="#edf2f4", bg="#8d99ae")
    label_target.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    entry_target = tk.Entry(frame_input, font=("Helvetica", 12))
    entry_target.grid(row=2, column=1, padx=10, pady=5)

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

    # Generate Circuit Button
    button_generate = tk.Button(frame_input, text="Generate Circuit", 
                                 command=lambda: create_circuit_and_visualize(
                                     entry_qubits.get(), entry_gate.get(), entry_target.get(), text_output, frame_output
                                 ), 
                                 **button_style)
    button_generate.grid(row=3, column=0, columnspan=2, pady=10)

    # Button to return to the main menu
    def return_to_main_menu():
        """Returns to the main menu."""
        root.destroy()  # Close the current window
        main.Application().mainloop()  # Reopen the main menu

    button_close = tk.Button(frame_input, text="Return to Main Menu", command=return_to_main_menu, **button_style)
    button_close.grid(row=4, column=0, columnspan=2, pady=10)

    # Output fields in frame_output
    label_output = tk.Label(frame_output, text="Simulation Output:", 
                            font=("Helvetica", 12, "bold"), fg="#2b2d42", bg="#edf2f4")
    label_output.grid(row=0, column=0, padx=10, pady=5)

    text_output = tk.Text(frame_output, width=60, height=20, font=("Courier", 12), bg="#f8f9fa", fg="#2b2d42")
    text_output.grid(row=1, column=0, padx=10, pady=5)

    root.mainloop()