import sys
import tkinter as tk

from dataclasses import dataclass

from typing import TextIO, Union, Callable


@dataclass
class BeforeWriteCallbackParams:
    content_to_write: str

@dataclass
class AfterWriteCallbackParams:
    wrote: Union[str, None]


BeforeWriteCallback = Union[Callable[[BeforeWriteCallbackParams], Union[str, None]], None]
AfterWriteCallback = Union[Callable[[AfterWriteCallbackParams], None], None]


class StdoutRedirector(TextIO):
    """
    The class used to write stdout to a tkinter frame.
    Replace stdout and print content on frame by creating
    label frames inside it
    """

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
        """
        Call before_callback to allow entry manipulation.
        Add label widgets to destination to print stdout content
        """

        to_write = None

        if self._before_write_callback is not None:
            params = BeforeWriteCallbackParams(content_to_write=string)
            to_write = self._before_write_callback(params)

        if to_write is not None:
            self._last_inserted_widget = tk.Label(self._destination, text=to_write)
            self._last_inserted_widget.pack()

            self._old_stdout.write(to_write)

        if self._after_write_callback is not None:
            params = AfterWriteCallbackParams(wrote=string)
            self._after_write_callback(params)

    def flush(self):
        self._destination.update()

    @property
    def last_inserted_widget(self) -> Union[tk.Label, None]:
        return self._last_inserted_widget

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
        """ Assign stdout to StdoutRedirector """

        self._old_stdout = sys.stdout
        self._redirector = StdoutRedirector(
            widget,
            old_stdout=self._old_stdout,
            before_write_callback=before_write_callback,
            after_write_callback=after_write_callback)
        sys.stdout = self._redirector

    def undo_stdout_redirection(self):
        sys.stdout = self._old_stdout

    def undo_last_insertion(self):
        if self._redirector is None:
            return

        widget = self._redirector.last_inserted_widget

        if widget is not None:
            widget.destroy()
