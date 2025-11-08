"""
Base class for all step frames.
"""

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from main import App


class BaseStepFrame(ttk.Frame):
    """Base class for all step frames with common interface."""
    
    def __init__(self, parent: tk.Widget, app: Any):
        super().__init__(parent)
        self.app = app
        self.complete = False
        
    def populate(self) -> None:
        """Build widgets for this step. Override in subclasses."""
        pass
    
    def bind_events(self) -> None:
        """Wire callbacks and validation. Override in subclasses."""
        pass
    
    def load_state(self) -> None:
        """Pre-fill fields from assessment_state. Override in subclasses."""
        pass
    
    def collect_data(self) -> None:
        """Push page data to assessment_state. Override in subclasses."""
        pass
    
    def is_complete(self) -> bool:
        """Return True if step is complete and Next can be enabled."""
        return self.complete
    
    def on_enter(self) -> None:
        """Called when step becomes active. Override if needed."""
        self.load_state()
        self.app.update_navigation()
    
    def on_leave(self) -> None:
        """Called when leaving this step. Override if needed."""
        pass

