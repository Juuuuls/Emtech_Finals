import tkinter as tk
import sqb_h
import eof_h  # Import eof_h to use its functions

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Page")
        self.geometry("400x300")

        # Add 4 buttons for different pages
        self.create_buttons()

    def create_buttons(self):
        # Button 1 to open quantum circuit page (eof_h.py)
        button1 = tk.Button(self, text="Quantum Circuit", command=self.open_quantum_circuit_page)
        button1.pack(pady=10)

        # Button 2 for other functionality (you can modify this)
        button2 = tk.Button(self, text="Page 2", command=self.page2)
        button2.pack(pady=10)

        # Button 3 for opening quantum circuit page from eof_h.py
        button3 = tk.Button(self, text="Quantum Simulation", command=self.open_quantum_simulation)
        button3.pack(pady=10)

        # Button 4 for additional functionality (modify as needed)
        button4 = tk.Button(self, text="Page 4", command=self.page4)
        button4.pack(pady=10)

    def open_quantum_circuit_page(self):
        """Function to open the quantum circuit page from eof_h.py."""
        print("Opening Quantum Circuit page...")
        self.withdraw()  # Hide the main window
        sqb_h.run_sqb_window()  # Correct function name


    def open_quantum_simulation(self):
        """Function to open the quantum simulation page from eof_h.py."""
        print("Opening Quantum Simulation...")
        self.withdraw()  # Hide the main window
        eof_h.run_eof_window()  # Open the simulation window from eof_h.py

    def page2(self):
        print("Page 2 functionality")  # Placeholder for your second page

    def page3(self):
        print("Page 3 functionality")  # Placeholder for your third page

    def page4(self):
        print("Page 4 functionality")  # Placeholder for your fourth page

# Run the main application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
