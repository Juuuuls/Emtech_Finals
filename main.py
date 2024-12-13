import tkinter as tk
from tkinter import ttk
from tkinter import font
import sqb_h
import eof_h  
import mqb_h
import interference  # Import the interference simulation module

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Quantum Simulation Main Page")
        self.geometry("450x450")  # Slightly larger to accommodate styling
        
        # Configure a modern style
        self.configure(bg="#2b2d42")  # Dark modern background
        self.create_buttons()

    def create_buttons(self):
        # Header label
        header = tk.Label(self, text="Quantum Simulation Toolkit", 
                          font=("Helvetica", 18, "bold"), fg="#edf2f4", bg="#2b2d42")
        header.pack(pady=20)

        # Button style
        button_style = {
            "font": ("Helvetica", 12),
            "bg": "#8d99ae",  # Muted modern color
            "fg": "#edf2f4",  # Light modern color
            "activebackground": "#ef233c",  # Vibrant highlight
            "activeforeground": "#edf2f4",
            "relief": "flat",
            "width": 25,
            "height": 2
        }

        # Buttons
        button1 = tk.Button(self, text="Single Qubit Superposition", 
                            command=self.open_quantum_circuit_page, **button_style)
        button1.pack(pady=10)

        button2 = tk.Button(self, text="Multi-Qubit Superposition", 
                            command=self.multi_qubit_simulation, **button_style)
        button2.pack(pady=10)

        button3 = tk.Button(self, text="Effects of Measurement", 
                            command=self.open_quantum_simulation, **button_style)
        button3.pack(pady=10)

        button4 = tk.Button(self, text="Interference Simulation", 
                            command=self.open_interference_simulation, **button_style)
        button4.pack(pady=10)

    def open_quantum_circuit_page(self):
        """Function to open the quantum circuit page from sqb_h.py."""
        print("Opening Quantum Circuit page...")
        self.withdraw()  # Hide the main window
        sqb_h.run_sqb_window()  # Correct function name

    def open_quantum_simulation(self):
        """Function to open the quantum simulation page from eof_h.py."""
        print("Opening Quantum Simulation...")
        self.withdraw()  # Hide the main window
        eof_h.run_eof_window()  # Open the simulation window from eof_h.py

    def open_interference_simulation(self):
        """Function to open the interference simulation page from interference_simulation.py."""
        print("Opening Interference Simulation...")
        self.withdraw()  # Hide the main window
        interference.run_interference_circuit()  # Open the interference simulation window

    def multi_qubit_simulation(self):
        print("Opening Multi-Qubit Simulation...")
        self.withdraw()
        mqb_h.run_mqb_window()

# Run the main application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
