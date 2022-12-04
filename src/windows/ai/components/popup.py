import tkinter as tk


class Popup(tk.Toplevel):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent, padx=30, pady=30)

        width = int(parent.winfo_width() * 0.5)
        height = int(parent.winfo_height() * 0.4)

        self.geometry(f"{width}x{height}")
            
        self.update()

        self._add_components()

    def _add_components(self):
        self._label = tk.Label(self, text="Número de épocas: ")
        self._label.pack()
        self._entry = tk.Entry(self)
        self._entry.pack()
        self._button = tk.Button(self, text="Prosseguir", command=self._ok_button_clicked)
        self._button.pack(pady=10)

    def _show_invalid_input_message(self):
        labels = [
            tk.Label(self, text="Número de épocas inválido"),
            tk.Label(self, text="Deve ser um número maior que 0.")
        ]

        for label in labels:
            label.pack()
            label.after(2000, label.destroy)

    def _ok_button_clicked(self):
        epochs = 0

        try:
            epochs = int(self._entry.get())
        except Exception:
            self._show_invalid_input_message()
            return

        if epochs <= 0:
            self._show_invalid_input_message()
            return
        
        if self._input_entered is not None:
            self._input_entered.set(True)

    def wait_input(self):
        self._input_entered = tk.BooleanVar(value=False)

        self.wait_variable(self._input_entered)

        epochs = int(self._entry.get())

        return epochs
