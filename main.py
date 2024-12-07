import tkinter as tk
import sqb_h  # Import sqb_h to use its functions

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Page")
        self.geometry("400x300")

        # Add 4 buttons for different pages
        self.create_buttons()

    def create_buttons(self):
        # Button 1 to open quantum circuit page (sqb_h.py)
        button1 = tk.Button(self, text="Quantum Circuit", command=self.open_quantum_circuit_page)
        button1.pack(pady=10)

        # Button 2 for other functionality (you can modify this)
        button2 = tk.Button(self, text="Page 2", command=self.page2)
        button2.pack(pady=10)

        # Button 3 for another functionality (modify as needed)
        button3 = tk.Button(self, text="Page 3", command=self.page3)
        button3.pack(pady=10)

        # Button 4 for additional functionality (modify as needed)
        button4 = tk.Button(self, text="Page 4", command=self.page4)
        button4.pack(pady=10)

    def open_quantum_circuit_page(self):
        """Function to open the quantum circuit page from sqb_h.py."""
        print("Opening Quantum Circuit page...")
        self.withdraw()  # Hide the main window
        sqb_h.run_quantum_circuit_window()  # Run the quantum circuit window from sqb_h.py

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
