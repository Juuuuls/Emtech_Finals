import tkinter as tk
from tkinter import ttk
from tkinter import font
import sqb_h 
import mqb_h
import interference 

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window title
        self.title("Quantum Simulation Main Page")
        
        # Enable fullscreen mode on startup
        self.attributes("-fullscreen", True)
        
        # Configure a modern style
        self.configure(bg="#2b2d42")  # Dark modern background
        self.create_buttons()

        # Bind the Escape key to exit fullscreen
        self.bind("<Escape>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode when Escape key is pressed."""
        current_state = self.attributes("-fullscreen")
        self.attributes("-fullscreen", not current_state)

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
            "width": 45,
            "height": 2
        }

        # Buttons
        button1 = tk.Button(self, text="Single Qubit Superposition", 
                            command=self.open_quantum_circuit_page, **button_style)
        button1.pack(pady=20)

        button2 = tk.Button(self, text="Multi-Qubit Superposition", 
                            command=self.multi_qubit_simulation, **button_style)
        button2.pack(pady=20)

        button3 = tk.Button(self, text="Effects of Measurement and Interference Simulation",
                            command=self.open_interference_simulation, **button_style)
        button3.pack(pady=20)

        # Exit button
        button4 = tk.Button(self, text="Exit", command=self.exit_application, **button_style)
        button4.pack(pady=20)

    def open_quantum_circuit_page(self):
        """Function to open the quantum circuit page from sqb_h.py."""
        print("Opening Quantum Circuit page...")
        self.withdraw()  # Hide the main window
        sqb_h.run_sqb_window()  # Correct function name

    def open_interference_simulation(self):
        """Function to open the interference simulation page from interference_simulation.py."""
        print("Opening Interference Simulation...")
        self.withdraw()  # Hide the main window
        interference.run_interference_circuit()  # Open the interference simulation window

    def multi_qubit_simulation(self):
        print("Opening Multi-Qubit Simulation...")
        self.withdraw()
        mqb_h.run_mqb_window()

    def exit_application(self):
        """Function to exit the application."""
        print("Exiting the application...")
        self.quit()

# Run the main application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
