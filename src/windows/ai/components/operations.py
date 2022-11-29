import tkinter as tk

from globals import events


class Operations(tk.Frame):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self.configure(width=parent.winfo_width() * 0.6)
        self.configure(height=parent.winfo_height())
        self.update()

        self._add_train_with_neural_network_button()

    def _add_train_with_neural_network_button(self):
        self._train_neural_network_button = tk.Button(self, text="Treinar rede neural")
        self._train_neural_network_button.configure(borderwidth=1)
        self._train_neural_network_button.configure(font=("", 15))
        self._train_neural_network_button.configure(command=self._train_neural_network)

    def _train_neural_network(self):
        events.train_neural_network_button_clicked.emit()

    def display_things(self):
        self._train_neural_network_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def hide_things(self):
        self._train_neural_network_button.place_forget()
