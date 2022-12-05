import tkinter as tk

from typing import Union

from services.output_service import (
    AfterWriteCallbackParams, BeforeWriteCallbackParams, OutputService
)

from helpers.tensorflow_output_helper import TensorflowOutputHelper

from windows.ai.components.scrollable_frame import ScrollableFrame


class TensorflowOutputDisplayer:
    def __init__(self, parent: tk.Frame):
        self._parent = parent
        self._output_service = OutputService()
        self._last_wrote_text: Union[str, None] = None

    def _before_write_callback(self, params: BeforeWriteCallbackParams):
        """
        Called before something is written to screen.
        Just allow content that is interesting to be displayed.
        Manipulate tensorflow output to be displayed on screen
        """

        if (not TensorflowOutputHelper.is_epoch_indicator(params.content_to_write) and
            not TensorflowOutputHelper.is_progress_output(params.content_to_write)):
            return None

        if (self._last_wrote_text is not None and 
            TensorflowOutputHelper.is_progress_output(self._last_wrote_text)):
            self._output_service.undo_last_insertion()

        return TensorflowOutputHelper.manipulate_to_show(params.content_to_write)

    def _after_write_callback(self, params: AfterWriteCallbackParams):
        """
        Called after something is written to screen.
        Store the previous wrote text to delete it on next write
        """

        self._last_wrote_text = params.wrote

    def enable(self):
        """
        Redirect stdout to a frame
        """

        self._frame = ScrollableFrame(self._parent)
        self._frame.configure(width=int(self._parent.winfo_width() * 0.7))
        self._frame.configure(height=int(self._parent.winfo_height() * 0.6))
        self._frame.configure(highlightthickness=1, highlightbackground="gray")
        self._frame.pack(pady=20)
        self._frame.pack_propagate(False)

        self._output_service.redirect_stdout_to(
            self._frame,
            before_write_callback=self._before_write_callback,
            after_write_callback=self._after_write_callback)

    def disable(self):
        self._output_service.undo_stdout_redirection()

        if self._frame is not None:
            self._frame.destroy()
