"""
Step 3: Immediate Memory (3 trials)
"""

import tkinter as tk
from tkinter import ttk
from base import BaseStepFrame
from utils import normalize_text, score_recall


class ImmediateMemoryStep(BaseStepFrame):
    """Step 3: Immediate Memory (3 trials)"""
    
    def populate(self) -> None:
        self.current_trial = 0
        self.trials_data = []
        
        # Instructions
        instructions = ttk.Label(
            self,
            text="You will see 5 words for 30 seconds. After they disappear, recall as many as you can.",
            font=("TkDefaultFont", 10),
            wraplength=600
        )
        instructions.grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=20)
        
        # Word display area
        self.word_frame = ttk.Frame(self, relief="sunken", borderwidth=2)
        self.word_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")
        self.word_frame.configure(height=200)  # Minimum height
        
        self.word_display = ttk.Label(
            self.word_frame,
            text="",
            font=("TkDefaultFont", 18, "bold"),
            justify="center"
        )
        self.word_display.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Timer label
        self.timer_label = ttk.Label(
            self.word_frame,
            text="",
            font=("TkDefaultFont", 14),
            foreground="red"
        )
        self.timer_label.pack(pady=10)
        
        # Control buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.show_button = ttk.Button(
            self.button_frame,
            text="Show Words",
            command=self._start_trial
        )
        self.show_button.pack(side="left", padx=10)
        
        self.submit_button = ttk.Button(
            self.button_frame,
            text="Submit Trial",
            command=self._submit_trial,
            state="disabled"
        )
        self.submit_button.pack(side="left", padx=10)
        
        self.next_trial_button = ttk.Button(
            self.button_frame,
            text="Next Trial",
            command=self._next_trial,
            state="disabled"
        )
        self.next_trial_button.pack(side="left", padx=10)
        
        # Recall input
        recall_label = ttk.Label(self, text="Enter recalled words (separated by spaces or commas):")
        recall_label.grid(row=3, column=0, columnspan=2, pady=(20, 5), padx=20, sticky="w")
        
        self.recall_text = tk.Text(self, height=6, width=60, wrap="word")
        self.recall_text.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        self.recall_text.config(state="disabled")
        
        # Feedback label
        self.feedback_label = ttk.Label(self, text="", font=("TkDefaultFont", 10, "bold"))
        self.feedback_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Trial progress
        self.progress_label = ttk.Label(self, text="Trial 0 of 3", font=("TkDefaultFont", 10))
        self.progress_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        
        self.timer_id = None
        self.time_remaining = 0
    
    def bind_events(self) -> None:
        pass
    
    def _start_trial(self) -> None:
        """Start a trial: show words and start 30s countdown."""
        self.current_trial += 1
        self.progress_label.config(text=f"Trial {self.current_trial} of 3")
        
        # Show words
        words = self.app.assessment_state["cognitive"]["immediate_memory"]["word_list"]
        self.word_display.config(text="\n".join(words))
        
        # Disable inputs
        self.show_button.config(state="disabled")
        self.recall_text.config(state="disabled")
        self.recall_text.delete("1.0", tk.END)
        self.submit_button.config(state="disabled")
        
        # Start countdown
        self.time_remaining = 30
        self._update_timer()
    
    def _update_timer(self) -> None:
        """Update countdown timer."""
        if self.time_remaining > 0:
            self.timer_label.config(text=f"Time remaining: {self.time_remaining} seconds")
            self.time_remaining -= 1
            self.timer_id = self.after(1000, self._update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            self.word_display.config(text="")
            self.recall_text.config(state="normal")
            self.submit_button.config(state="normal")
            self.recall_text.focus()
    
    def _submit_trial(self) -> None:
        """Submit current trial and score it."""
        recall_text = self.recall_text.get("1.0", tk.END).strip()
        recalled = normalize_text(recall_text)
        word_list = self.app.assessment_state["cognitive"]["immediate_memory"]["word_list"]
        score = score_recall(recalled, word_list)
        
        trial_data = {
            "recalled": recalled,
            "score": score
        }
        self.trials_data.append(trial_data)
        
        # Show feedback
        self.feedback_label.config(
            text=f"Trial {self.current_trial} score: {score}/5",
            foreground="green" if score == 5 else "black"
        )
        
        # Disable submit
        self.submit_button.config(state="disabled")
        self.recall_text.config(state="disabled")
        
        # Enable next trial or mark complete
        if self.current_trial < 3:
            self.next_trial_button.config(state="normal")
        else:
            # All trials complete
            self.complete = True
            self.app.update_navigation()
            self.feedback_label.config(
                text=f"All trials complete! Total score: {sum(t['score'] for t in self.trials_data)}/15"
            )
    
    def _next_trial(self) -> None:
        """Move to next trial."""
        self.next_trial_button.config(state="disabled")
        self.feedback_label.config(text="")
        self.show_button.config(state="normal")
    
    def load_state(self) -> None:
        state = self.app.assessment_state
        trials = state["cognitive"]["immediate_memory"].get("trials", [])
        if trials:
            self.trials_data = trials.copy()
            self.current_trial = len(trials)
            if self.current_trial >= 3:
                self.complete = True
                # Show final state
                self.progress_label.config(text="All 3 trials completed")
                self.feedback_label.config(
                    text=f"Total score: {sum(t['score'] for t in self.trials_data)}/15"
                )
                self.show_button.config(state="disabled")
                self.recall_text.config(state="disabled")
            else:
                self.progress_label.config(text=f"Trial {self.current_trial} of 3")
                self.show_button.config(state="normal")
        else:
            self.current_trial = 0
            self.trials_data = []
            self.show_button.config(state="normal")
    
    def collect_data(self) -> None:
        state = self.app.assessment_state
        total_score = sum(t["score"] for t in self.trials_data)
        state["cognitive"]["immediate_memory"]["trials"] = self.trials_data
        state["cognitive"]["immediate_memory"]["total_score"] = total_score
        state["cognitive"]["immediate_memory"]["max_score"] = 15
    
    def on_enter(self) -> None:
        super().on_enter()
        # Cancel any running timer
        if hasattr(self, 'timer_id') and self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None
    
    def on_leave(self) -> None:
        """Called when leaving this step."""
        # Cancel timer if running
        if hasattr(self, 'timer_id') and self.timer_id:
            self.after_cancel(self.timer_id)
            self.timer_id = None

