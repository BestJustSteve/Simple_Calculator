import tkinter as tk

from calculator.gui import CalculatorApp


def main():
    root = tk.Tk()

    CalculatorApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
