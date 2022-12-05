import tkinter as tk


class ScrollableFrame(tk.Frame):
    """ A frame that have a scrollbar """

    def __init__(self, parent: tk.Frame):
        super().__init__(parent)

        self._canvas = tk.Canvas(self)
        self._frame = tk.Frame(self._canvas)
        self._scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self._canvas.yview)
        
        self._frame.bind("<Configure>", self._on_configure)
        self._canvas.bind("<Configure>", self._on_configure)

        self._canvas.create_window((0, 0), window=self._frame, anchor=tk.NW)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._canvas.pack(fill=tk.BOTH)
        self._frame.pack(fill=tk.BOTH)
        self._scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
    
    def _on_configure(self, _):
        self._canvas.configure(scrollregion=self._canvas.bbox(tk.ALL))
