import tkinter as tk

from globals import events


class OperationsFrame(tk.Frame):
    def __init__(self, parent: tk.Toplevel):
        super().__init__(parent)

        self.configure(width=parent.winfo_width() * 0.6)
        self.configure(height=parent.winfo_height())
        self.update()

        self._add_buttons()

    def _create_pre_styled_button(self, text: str, command):
        button = tk.Button(self, text=text)
        button.configure(borderwidth=1)
        button.configure(font=("", 13))
        button.configure(command=command)
        return button

    def _add_buttons(self):
        self._train_neural_network_button = self._create_pre_styled_button("Treinar rede neural convolucional", self._train_neural_network)
        self._train_normal_classifier_button = self._create_pre_styled_button("Treinar classificador raso", self._train_normal_classifier)

    def _train_neural_network(self):
        events.train_neural_network_button_clicked.emit()

    def _train_normal_classifier(self):
        events.train_normal_classifier_button_clicked.emit()

    def display_things(self):
        self._train_normal_classifier_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self._train_neural_network_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def hide_things(self):
        self._train_normal_classifier_button.place_forget()
        self._train_neural_network_button.place_forget()
