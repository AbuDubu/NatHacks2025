"""
Step 7: Review & Finish
"""

import tkinter as tk
from tkinter import ttk
from base import BaseStepFrame


class ReviewStep(BaseStepFrame):
    """Step 7: Review & Finish"""
    
    def populate(self) -> None:
        # Summary header
        header = ttk.Label(
            self,
            text="Review & Finish",
            font=("TkDefaultFont", 16, "bold")
        )
        header.grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=20)
        
        # Create scrollable summary
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        summary_frame = ttk.Frame(canvas)
        
        summary_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=summary_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.summary_text = tk.Text(
            summary_frame,
            height=15,
            width=70,
            wrap="word",
            state="disabled",
            font=("TkDefaultFont", 10)
        )
        self.summary_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        scrollbar.grid(row=1, column=2, sticky="ns", pady=10)
        
        # Assessor notes
        notes_label = ttk.Label(self, text="Assessor Notes (optional):")
        notes_label.grid(row=2, column=0, columnspan=2, pady=(20, 5), padx=20, sticky="w")
        
        self.notes_text = tk.Text(self, height=4, width=70, wrap="word")
        self.notes_text.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.complete = True  # Review is always complete
    
    def _generate_summary(self) -> str:
        """Generate summary text from assessment state."""
        state = self.app.assessment_state
        lines = []
        
        # Participant info
        lines.append("=== PARTICIPANT INFORMATION ===")
        lines.append(f"Full Name: {state['participant'].get('full_name', 'N/A')}")
        lines.append(f"Participant ID: {state['participant'].get('participant_id', 'N/A')}")
        lines.append("")
        
        # Symptoms
        lines.append("=== SYMPTOMS ===")
        symptom_count = state['symptoms'].get('symptom_count', 0)
        symptom_severity = state['symptoms'].get('symptom_severity_total', 0)
        lines.append(f"Symptom Count: {symptom_count}")
        lines.append(f"Symptom Severity Sum: {symptom_severity}")
        lines.append("")
        
        # Immediate Memory
        lines.append("=== IMMEDIATE MEMORY ===")
        imm = state['cognitive']['immediate_memory']
        trials = imm.get('trials', [])
        if trials:
            for i, trial in enumerate(trials, 1):
                lines.append(f"Trial {i}: {trial['score']}/5")
            lines.append(f"Total Score: {imm.get('total_score', 0)}/15")
        else:
            lines.append("Not completed")
        lines.append("")
        
        # Delayed Recall
        lines.append("=== DELAYED RECALL ===")
        dr = state['cognitive']['delayed_recall']
        lines.append(f"Score: {dr.get('score', 0)}/5")
        lines.append("")
        
        # Placeholders
        lines.append("=== OTHER ASSESSMENTS ===")
        lines.append("Balance Assessment: Not yet implemented")
        lines.append("Eye-Tracking Assessment: Not yet implemented")
        
        return "\n".join(lines)
    
    def load_state(self) -> None:
        # Update summary
        summary = self._generate_summary()
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", summary)
        self.summary_text.config(state="disabled")
        
        # Load notes
        notes = self.app.assessment_state["meta"].get("assessor_notes", "")
        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", notes)
    
    def collect_data(self) -> None:
        notes = self.notes_text.get("1.0", tk.END).strip()
        self.app.assessment_state["meta"]["assessor_notes"] = notes
    
    def on_enter(self) -> None:
        super().on_enter()
        self.notes_text.focus()

