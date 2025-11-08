"""
Step 1: Participant Information
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from base import BaseStepFrame
from constants import UI_TEXTS


class IntroStep(BaseStepFrame):
    """Step 1: Participant Information"""
    
    def populate(self) -> None:
        # Header
        header = ttk.Label(self, text=UI_TEXTS["app_title"], 
                          font=("TkDefaultFont", 16, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20)
        
        subtitle = ttk.Label(self, text=UI_TEXTS["app_subtitle"])
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 30), padx=20)
        
        # Full Name
        name_label = ttk.Label(self, text="Full Name *")
        name_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=2, column=1, sticky="ew", padx=20, pady=10)
        self.name_entry.bind("<KeyRelease>", self._validate_name)
        
        self.name_error = ttk.Label(self, text="", foreground="red")
        self.name_error.grid(row=3, column=1, sticky="w", padx=20)
        
        # Participant ID
        id_label = ttk.Label(self, text="Participant ID")
        id_label.grid(row=4, column=0, sticky="w", padx=20, pady=10)
        
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(self, textvariable=self.id_var, width=40)
        self.id_entry.grid(row=4, column=1, sticky="ew", padx=20, pady=10)
        
        id_hint = ttk.Label(self, text="(Optional - will be auto-generated if blank)", 
                           font=("TkDefaultFont", 9))
        id_hint.grid(row=5, column=1, sticky="w", padx=20)
        
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)
    
    def bind_events(self) -> None:
        self.name_var.trace_add("write", lambda *args: self._validate_name())
    
    def _validate_name(self, *args) -> None:
        name = self.name_var.get().strip()
        if len(name) < 2:
            self.name_error.config(text="Full name must be at least 2 characters")
            self.complete = False
        else:
            self.name_error.config(text="")
            self.complete = True
        self.app.update_navigation()
    
    def load_state(self) -> None:
        state = self.app.assessment_state
        self.name_var.set(state["participant"].get("full_name", ""))
        self.id_var.set(state["participant"].get("participant_id", ""))
        self._validate_name()
    
    def collect_data(self) -> None:
        state = self.app.assessment_state
        full_name = self.name_var.get().strip()
        participant_id = self.id_var.get().strip()
        
        # Auto-generate ID if blank
        if not participant_id:
            initials = "".join([word[0].upper() for word in full_name.split() if word])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            participant_id = f"{initials}_{timestamp}" if initials else f"PART_{timestamp}"
        
        state["participant"]["full_name"] = full_name
        state["participant"]["participant_id"] = participant_id
    
    def on_enter(self) -> None:
        super().on_enter()
        self.name_entry.focus()

