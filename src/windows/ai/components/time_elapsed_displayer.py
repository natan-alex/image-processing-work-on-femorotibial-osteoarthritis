import time
import datetime
import tkinter as tk
import multiprocessing as mp


class TimeElapsedDisplayer:
    def __init__(self, parent: tk.Frame):
        self._parent = parent
        self._label = None
        self._process = None
        self._stop_event = None

    def _update_time(self):
        """ Measure time elapsed from the begining and display it formatted """

        elapsed_time = int(time.time() - self._start_time)

        h, m, s = str(datetime.timedelta(seconds=elapsed_time)).split(':')

        label_text = f"Tempo gasto: {h} horas {m} minutos e {s} segundos"

        self._label.configure(text=label_text)
        self._label.update()

    def _keep_updating(self):
        while not self._stop_event.is_set():
            self._update_time()
            time.sleep(1)

    def start(self):
        self._label = tk.Label(self._parent)
        self._label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        self._label.update()

        self._stop_event = mp.Event()
        self._start_time = time.time()

        self._process = mp.Process(target=self._keep_updating)
        self._process.start()

    def stop(self):
        print("deactivating")

        if self._stop_event is not None:
            self._stop_event.set()

        if self._process is not None:
            self._process.join()
