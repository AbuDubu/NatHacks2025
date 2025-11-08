"""
Step 4: Balance Assessment (placeholder)
"""

from tkinter import ttk
from base import BaseStepFrame


class BalanceStep(BaseStepFrame):
    """Step 4: Balance Assessment (placeholder)"""
    
    def populate(self) -> None:
        header = ttk.Label(
            self,
            text="Balance Assessment",
            font=("TkDefaultFont", 16, "bold")
        )
        header.grid(row=0, column=0, pady=(40, 20), padx=20)
        
        note = ttk.Label(
            self,
            text="This module will be implemented later. No input required.",
            font=("TkDefaultFont", 10)
        )
        note.grid(row=1, column=0, pady=10, padx=20)
        
        status = ttk.Label(
            self,
            text="Status: Placeholder",
            font=("TkDefaultFont", 10),
            foreground="gray"
        )
        status.grid(row=2, column=0, pady=20, padx=20)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        
        self.complete = True  # Placeholder is always complete
    
    def load_state(self) -> None:
        pass
    
    def collect_data(self) -> None:
        self.app.assessment_state["balance"]["status"] = "placeholder"

