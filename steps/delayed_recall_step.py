"""
Step 6: Delayed Recall
"""

import tkinter as tk
from tkinter import ttk
from base import BaseStepFrame
from utils import normalize_text, score_recall


class DelayedRecallStep(BaseStepFrame):
    """Step 6: Delayed Recall"""
    
    def populate(self) -> None:
        instructions = ttk.Label(
            self,
            text="Please recall the words you saw earlier. Enter as many as you can (order doesn't matter).",
            font=("TkDefaultFont", 10),
            wraplength=600
        )
        instructions.grid(row=0, column=0, pady=(20, 20), padx=20, sticky="w")
        
        # Recall input
        recall_label = ttk.Label(self, text="Enter recalled words (separated by spaces or commas):")
        recall_label.grid(row=1, column=0, pady=(10, 5), padx=20, sticky="w")
        
        self.recall_text = tk.Text(self, height=8, width=60, wrap="word")
        self.recall_text.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        
        # Submit button
        self.submit_button = ttk.Button(
            self,
            text="Submit Delayed Recall",
            command=self._submit_recall
        )
        self.submit_button.grid(row=3, column=0, pady=20)
        
        # Feedback label
        self.feedback_label = ttk.Label(self, text="", font=("TkDefaultFont", 10, "bold"))
        self.feedback_label.grid(row=4, column=0, pady=10)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
    
    def _submit_recall(self) -> None:
        """Submit and score delayed recall."""
        recall_text = self.recall_text.get("1.0", tk.END).strip()
        recalled = normalize_text(recall_text)
        word_list = self.app.assessment_state["cognitive"]["immediate_memory"]["word_list"]
        score = score_recall(recalled, word_list)
        
        # Store data
        state = self.app.assessment_state
        state["cognitive"]["delayed_recall"]["recalled"] = recalled
        state["cognitive"]["delayed_recall"]["score"] = score
        state["cognitive"]["delayed_recall"]["max_score"] = 5
        
        # Show feedback
        self.feedback_label.config(
            text=f"Delayed recall score: {score}/5",
            foreground="green" if score == 5 else "black"
        )
        
        # Disable input
        self.recall_text.config(state="disabled")
        self.submit_button.config(state="disabled")
        
        # Mark complete
        self.complete = True
        self.app.update_navigation()
    
    def load_state(self) -> None:
        state = self.app.assessment_state
        recalled = state["cognitive"]["delayed_recall"].get("recalled", [])
        if recalled:
            self.recall_text.insert("1.0", " ".join(recalled))
            self.recall_text.config(state="disabled")
            self.submit_button.config(state="disabled")
            score = state["cognitive"]["delayed_recall"].get("score", 0)
            self.feedback_label.config(text=f"Delayed recall score: {score}/5")
            self.complete = True
        else:
            self.recall_text.config(state="normal")
            self.submit_button.config(state="normal")
    
    def collect_data(self) -> None:
        # Already collected in _submit_recall, but ensure it's called
        pass
    
    def on_enter(self) -> None:
        super().on_enter()
        if not self.complete:
            self.recall_text.focus()

