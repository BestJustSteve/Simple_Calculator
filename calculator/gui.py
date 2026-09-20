import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from calculator.version import __version__

from calculator.calculator_engine import (
    calculate_expression,
    format_number
)

from calculator.storage import (
    load_data,
    save_data
)


class CalculatorApp:
    def __init__(self, root):
        self.root = root

        self.history = []
        self.memory = {}
        self.last_result = None

        self.display_var = tk.StringVar()
        self.previous_var = tk.StringVar()

        self.load_saved_data()

        self.configure_window()
        self.create_menu()
        self.create_widgets()
        self.create_keyboard_shortcuts()


    def load_saved_data(self):
        (
            self.history,
            self.memory,
            self.last_result
        ) = load_data()


    def save(self):
        try:
            save_data(
                self.history,
                self.memory,
                self.last_result
            )

        except OSError:
            messagebox.showerror(
                "Error",
                "Calculator data could not be saved."
            )


    def configure_window(self):
        self.root.title(
            f"Simple Calculator {__version__}"
        )
        self.root.geometry("400x660")
        self.root.resizable(False, False)

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_program
        )


    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(
            menu_bar,
            tearoff=False
        )

        file_menu.add_command(
            label="Clear",
            command=self.clear_display
        )

        file_menu.add_separator()

        file_menu.add_command(
            label="Exit",
            command=self.close_program
        )

        menu_bar.add_cascade(
            label="File",
            menu=file_menu
        )


        history_menu = tk.Menu(
            menu_bar,
            tearoff=False
        )

        history_menu.add_command(
            label="View History",
            command=self.show_history
        )

        history_menu.add_command(
            label="Clear History",
            command=self.clear_history
        )

        menu_bar.add_cascade(
            label="History",
            menu=history_menu
        )


        memory_menu = tk.Menu(
            menu_bar,
            tearoff=False
        )

        memory_menu.add_command(
            label="Save Last Result",
            command=self.save_last_result_to_memory
        )

        memory_menu.add_command(
            label="View Memory",
            command=self.show_memory
        )

        menu_bar.add_cascade(
            label="Memory",
            menu=memory_menu
        )


        help_menu = tk.Menu(
            menu_bar,
            tearoff=False
        )

        help_menu.add_command(
            label="About",
            command=self.show_about
        )

        menu_bar.add_cascade(
            label="Help",
            menu=help_menu
        )

        self.root.config(
            menu=menu_bar
        )


    def create_widgets(self):
        main_frame = ttk.Frame(
            self.root,
            padding=15
        )

        main_frame.pack(
            fill="both",
            expand=True
        )


        previous_label = ttk.Label(
            main_frame,
            textvariable=self.previous_var,
            anchor="e",
            font=("Segoe UI", 11)
        )

        previous_label.pack(
            fill="x",
            pady=(0, 2)
        )


        self.display = ttk.Entry(
            main_frame,
            textvariable=self.display_var,
            justify="right",
            font=("Segoe UI", 24)
        )

        self.display.pack(
            fill="x",
            ipady=10
        )


        tool_frame = ttk.Frame(
            main_frame
        )

        tool_frame.pack(
            fill="x",
            pady=10
        )


        ttk.Button(
            tool_frame,
            text="ANS",
            command=self.use_last_result
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 4)
        )


        ttk.Button(
            tool_frame,
            text="History",
            command=self.show_history
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=4
        )


        ttk.Button(
            tool_frame,
            text="Memory",
            command=self.show_memory
        ).pack(
            side="left",
            expand=True,
            fill="x",
            padx=(4, 0)
        )


        button_frame = ttk.Frame(
            main_frame
        )

        button_frame.pack(
            fill="both",
            expand=True
        )


        buttons = [
            ("C", 0, 0),
            ("⌫", 0, 1),
            ("(", 0, 2),
            (")", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("/", 1, 3),

            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("*", 2, 3),

            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),

            ("0", 4, 0),
            (".", 4, 1),
            ("%", 4, 2),
            ("+", 4, 3),

            ("//", 5, 0),
            ("**", 5, 1),
            ("=", 5, 2, 2)
        ]


        for item in buttons:
            text = item[0]
            row = item[1]
            column = item[2]

            columnspan = 1

            if len(item) == 4:
                columnspan = item[3]

            if text == "C":
                command = self.clear_display

            elif text == "⌫":
                command = self.backspace

            elif text == "=":
                command = self.calculate

            else:
                command = (
                    lambda value=text:
                    self.button_click(value)
                )

            ttk.Button(
                button_frame,
                text=text,
                command=command
            ).grid(
                row=row,
                column=column,
                columnspan=columnspan,
                sticky="nsew",
                padx=4,
                pady=4
            )


        for row in range(6):
            button_frame.rowconfigure(
                row,
                weight=1
            )

        for column in range(4):
            button_frame.columnconfigure(
                column,
                weight=1
            )

        self.display.focus_set()


    def button_click(self, value):
        current = self.display_var.get()

        self.display_var.set(
            current + value
        )


    def clear_display(self):
        self.display_var.set("")
        self.previous_var.set("")


    def backspace(self):
        current = self.display_var.get()

        self.display_var.set(
            current[:-1]
        )


    def calculate(self):
        expression = self.display_var.get().strip()

        if expression == "":
            return

        try:
            result = calculate_expression(
                expression
            )

            formatted_result = format_number(
                result
            )

            self.previous_var.set(
                f"{expression} ="
            )

            self.display_var.set(
                str(formatted_result)
            )

            self.last_result = result

            history_entry = {
                "timestamp": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "expression": expression,
                "result": result
            }

            self.history.append(
                history_entry
            )

            self.save()

        except ZeroDivisionError:
            messagebox.showerror(
                "Error",
                "Cannot divide by zero."
            )

        except OverflowError:
            messagebox.showerror(
                "Error",
                "That number is too large."
            )

        except (ValueError, SyntaxError, TypeError):
            messagebox.showerror(
                "Error",
                "Invalid calculation."
            )


    def use_last_result(self):
        if self.last_result is None:
            messagebox.showinfo(
                "Last Result",
                "No previous result is available."
            )

            return

        self.button_click(
            str(
                format_number(
                    self.last_result
                )
            )
        )


    def show_history(self):
        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Calculation History"
        )

        window.geometry(
            "650x400"
        )


        frame = ttk.Frame(
            window,
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )


        ttk.Label(
            frame,
            text="Calculation History",
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=(0, 10)
        )


        history_box = tk.Text(
            frame,
            font=("Consolas", 11),
            wrap="word"
        )

        history_box.pack(
            fill="both",
            expand=True
        )


        if not self.history:
            history_box.insert(
                tk.END,
                "No calculations in history."
            )

        else:
            for entry in self.history:
                history_box.insert(
                    tk.END,
                    (
                        f'{entry["timestamp"]} | '
                        f'{entry["expression"]} = '
                        f'{format_number(entry["result"])}\n'
                    )
                )


        history_box.config(
            state="disabled"
        )


        ttk.Button(
            frame,
            text="Clear History",
            command=lambda:
                self.clear_history(window)
        ).pack(
            pady=(10, 0)
        )


    def clear_history(self, window=None):
        if not self.history:
            messagebox.showinfo(
                "History",
                "History is already empty."
            )

            return

        confirm = messagebox.askyesno(
            "Clear History",
            "Are you sure you want to clear all history?"
        )

        if confirm:
            self.history.clear()
            self.save()

            if window is not None:
                window.destroy()


    def save_last_result_to_memory(self):
        if self.last_result is None:
            messagebox.showinfo(
                "Memory",
                "There is no result to save."
            )

            return

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Save to Memory"
        )

        window.geometry(
            "320x170"
        )


        frame = ttk.Frame(
            window,
            padding=15
        )

        frame.pack(
            fill="both",
            expand=True
        )


        ttk.Label(
            frame,
            text="Memory name:"
        ).pack(
            anchor="w"
        )


        name_entry = ttk.Entry(
            frame
        )

        name_entry.pack(
            fill="x",
            pady=8
        )

        name_entry.focus_set()


        def save_memory_value():
            name = name_entry.get().strip()

            if name == "":
                messagebox.showerror(
                    "Error",
                    "Memory name cannot be empty."
                )

                return

            self.memory[name] = (
                self.last_result
            )

            self.save()

            window.destroy()


        ttk.Button(
            frame,
            text="Save",
            command=save_memory_value
        ).pack(
            pady=10
        )


    def show_memory(self):
        window = tk.Toplevel(
            self.root
        )

        window.title(
            "Saved Memory"
        )

        window.geometry(
            "450x350"
        )


        frame = ttk.Frame(
            window,
            padding=10
        )

        frame.pack(
            fill="both",
            expand=True
        )


        ttk.Label(
            frame,
            text="Saved Values",
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=(0, 10)
        )


        if not self.memory:
            ttk.Label(
                frame,
                text="No saved values."
            ).pack(
                pady=20
            )

            return


        for name, value in self.memory.items():
            row = ttk.Frame(
                frame
            )

            row.pack(
                fill="x",
                pady=4
            )


            ttk.Label(
                row,
                text=(
                    f"{name} = "
                    f"{format_number(value)}"
                )
            ).pack(
                side="left",
                fill="x",
                expand=True
            )


            ttk.Button(
                row,
                text="Use",
                command=lambda v=value, w=window:
                    self.use_memory_value(v, w)
            ).pack(
                side="left",
                padx=4
            )


            ttk.Button(
                row,
                text="Delete",
                command=lambda n=name, w=window:
                    self.delete_memory_value(n, w)
            ).pack(
                side="left"
            )


    def use_memory_value(
        self,
        value,
        window
    ):
        self.button_click(
            str(
                format_number(value)
            )
        )

        window.destroy()


    def delete_memory_value(
        self,
        name,
        window
    ):
        if name in self.memory:
            del self.memory[name]

            self.save()

            window.destroy()

            self.show_memory()


    def show_about(self):
        messagebox.showinfo(
            "About",
            (
                "Python Calculator\n\n"
                "Built with tkinter, ttk, JSON, and AST."
            )
        )
    def show_about(self):
        messagebox.showinfo(
            "About",
            (
                f"Simple Calculator {__version__}\n\n"
                "Built with Python, tkinter, ttk, JSON, AST, and pytest.\n\n"
                "Features:\n"
                "- Safe expression parsing\n"
                "- Calculation history\n"
                "- Saved memory values\n"
                "- Persistent data storage\n"
                "- Keyboard shortcuts"
            )
        )

    def create_keyboard_shortcuts(self):
        self.root.bind(
            "<Key>",
            self.key_pressed
        )

        self.root.bind(
            "<Control-h>",
            lambda event:
                self.show_history()
        )

        self.root.bind(
            "<Control-m>",
            lambda event:
                self.show_memory()
        )

        self.root.bind(
            "<Control-s>",
            lambda event:
                self.save_last_result_to_memory()
        )

        self.root.bind(
            "<Control-l>",
            lambda event:
                self.clear_display()
        )


    def key_pressed(self, event):
        key = event.keysym
        char = event.char

        if char in "0123456789.+-*/%()":
            self.button_click(char)

        elif key == "Return":
            self.calculate()

        elif key == "BackSpace":
            self.backspace()

        elif key == "Escape":
            self.clear_display()


    def close_program(self):
        self.save()
        self.root.destroy()