import sys
import tkinter as tk

from dataclasses import dataclass

from typing import TextIO, Union, Callable


@dataclass
class BeforeWriteCallbackParams:
    content_to_write: str

@dataclass
class AfterWriteCallbackParams:
    wrote: str
    inserted_widget: tk.Label


BeforeWriteCallback = Union[Callable[[BeforeWriteCallbackParams], str], None]
AfterWriteCallback = Union[Callable[[AfterWriteCallbackParams], None], None]


class StdoutRedirector(TextIO):
    def __init__(
        self,
        destination: tk.Frame,
        old_stdout: TextIO,
        before_write_callback: BeforeWriteCallback = None,
        after_write_callback: AfterWriteCallback = None
    ):
        self._destination = destination
        self._old_stdout = old_stdout
        self._before_write_callback = before_write_callback
        self._after_write_callback = after_write_callback

    def write(self, string: str):
        if self._before_write_callback is not None:
            string = self._before_write_callback(
                BeforeWriteCallbackParams(content_to_write=string))

        label = tk.Label(self._destination, text=string)
        label.pack()

        self._old_stdout.write(f"{string}\n")

        if self._after_write_callback is not None:
            self._after_write_callback(
                AfterWriteCallbackParams(wrote=string, inserted_widget=label))

    def flush(self):
        self._destination.update()

class OutputService:
    def __init__(self) -> None:
        self._old_stdout: Union[TextIO, None] = None
        self._redirector: Union[StdoutRedirector, None] = None

    def redirect_stdout_to(
        self,
        widget: tk.Frame,
        before_write_callback: BeforeWriteCallback = None,
        after_write_callback: AfterWriteCallback = None
    ):
        self._old_stdout = sys.stdout
        self._redirector = StdoutRedirector(
            widget, 
            old_stdout=self._old_stdout,
            before_write_callback=before_write_callback,
            after_write_callback=after_write_callback)
        sys.stdout = self._redirector

    def undo_stdout_redirection(self):
        sys.stdout = self._old_stdout
