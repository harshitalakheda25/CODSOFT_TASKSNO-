"""
===== CALCULATOR (GUI) =====

"""

import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------------------
# BACKEND — pure calculation logic, no UI code here.
# ---------------------------------------------------------------------------

def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "Addition (+)": add,
    "Subtraction (-)": subtract,
    "Multiplication (*)": multiply,
    "Division (/)": divide,
}


def calculate(num1_text, num2_text, operation_label):
    """
    Takes raw string inputs + the chosen operation label,
    returns (result, error_message). Exactly one will be None.
    """
    if not num1_text.strip() or not num2_text.strip():
        return None, "Enter both numbers first"

    try:
        num1 = float(num1_text)
        num2 = float(num2_text)
    except ValueError:
        return None, "Numbers must be valid (e.g. 12 or 3.5)"

    func = OPERATIONS.get(operation_label)
    if func is None:
        return None, "Invalid choice"

    try:
        result = func(num1, num2)
    except ZeroDivisionError as e:
        return None, str(e)

    # Show whole numbers without a trailing .0
    if result == int(result):
        result = int(result)

    return result, None


# ---------------------------------------------------------------------------
# FRONTEND — Tkinter GUI. Calls into the backend functions above.
# ---------------------------------------------------------------------------

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("320x320")
        self.resizable(False, False)
        self.configure(padx=20, pady=20)

        ttk.Label(self, text="CALCULATOR", font=("Segoe UI", 16, "bold")).pack(pady=(0, 15))

        # First number
        ttk.Label(self, text="First number:").pack(anchor="w")
        self.num1_entry = ttk.Entry(self)
        self.num1_entry.pack(fill="x", pady=(0, 10))

        # Second number
        ttk.Label(self, text="Second number:").pack(anchor="w")
        self.num2_entry = ttk.Entry(self)
        self.num2_entry.pack(fill="x", pady=(0, 10))

        # Operation dropdown
        ttk.Label(self, text="Operation:").pack(anchor="w")
        self.operation_var = tk.StringVar(value=list(OPERATIONS.keys())[0])
        self.operation_menu = ttk.Combobox(
            self,
            textvariable=self.operation_var,
            values=list(OPERATIONS.keys()),
            state="readonly",
        )
        self.operation_menu.pack(fill="x", pady=(0, 15))

        # Calculate button
        ttk.Button(self, text="Calculate", command=self.on_calculate).pack(fill="x")

        # Result / error display
        self.result_var = tk.StringVar(value="Result = ")
        self.result_label = ttk.Label(
            self, textvariable=self.result_var, font=("Segoe UI", 12, "bold")
        )
        self.result_label.pack(pady=(20, 0))

        # Let Enter key trigger calculation too
        self.bind("<Return>", lambda event: self.on_calculate())

    def on_calculate(self):
        num1_text = self.num1_entry.get()
        num2_text = self.num2_entry.get()
        operation_label = self.operation_var.get()

        result, error = calculate(num1_text, num2_text, operation_label)

        if error:
            self.result_var.set(error)
            self.result_label.configure(foreground="red")
        else:
            self.result_var.set(f"Result = {result}")
            self.result_label.configure(foreground="black")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
