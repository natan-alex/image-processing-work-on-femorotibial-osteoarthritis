import tkinter as tk

import time
import datetime


class TimeElapsedDisplayer:
    def __init__(self, parent: tk.Frame, interval_in_seconds: int = 2):
        self._parent = parent
        self._interval_in_seconds = interval_in_seconds if interval_in_seconds >= 1 else 2
        self._is_activated = False

    def _format_elapsed_time(self, seconds: int) -> str:
        h, m, s = str(datetime.timedelta(seconds=seconds)).split(':')
        return f"{h} horas {m} minutos e {s} segundos"

    def _update_label(self):
        """ Measure time elapsed from the begining and show it formatted """

        if not self._is_activated or self._label is None:
            return

        elapsed_time = time.time() - self._start_time
        formatted = self._format_elapsed_time(int(elapsed_time))
        self._label.configure(text=f"Tempo gasto: {formatted}")
        self._label.after(self._interval_in_seconds * 1000, self._update_label)

    def enable(self):
        """ Create label that recursively self update after in an interval """

        self._start_time = time.time()
        self._is_activated = True
        self._label = tk.Label(self._parent)
        self._label.pack(pady=20)

        self._update_label()

    def disable(self):
        """ Stop interval """

        self._is_activated = False

        if self._label is not None:
            self._label.destroy()
