import tkinter as tk

import time
import datetime


class TimeElapsedLabel(tk.Label):
    def __init__(self, parent: tk.Toplevel, interval_in_seconds: int = 2):
        super().__init__(parent)

        self._interval_in_seconds = interval_in_seconds if interval_in_seconds >= 1 else 2
        self._is_activated = False

    def _format_elapsed_time(self, seconds: int) -> str:
        h, m, s = str(datetime.timedelta(seconds=seconds)).split(':')
        return f"{h} horas {m} minutos e {s} segundos"

    def _update_label(self):
        if not self._is_activated:
            return

        elapsed_time = time.time() - self._start_time
        formatted = self._format_elapsed_time(int(elapsed_time))
        self.configure(text=f"Tempo gasto: {formatted}")
        self.after(self._interval_in_seconds * 1000, self._update_label)

    def start_showing_and_updating_time(self):
        self._start_time = time.time()
        self._is_activated = True

        self.pack(pady=20)

        self._update_label()

    def stop_updating_time(self):
        self._is_activated = False
