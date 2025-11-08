"""
Step 2: Symptoms Checklist
"""

import tkinter as tk
from tkinter import ttk
from base import BaseStepFrame
from constants import SYMPTOMS, SYMPTOM_LABELS


class SymptomsStep(BaseStepFrame):
    """Step 2: Symptoms Checklist"""
    
    def populate(self) -> None:
        # Instructions
        instructions = ttk.Label(
            self,
            text="Rate each symptom 0–6 (0 = none, 6 = severe) over the last 24 hours.",
            font=("TkDefaultFont", 10)
        )
        instructions.grid(row=0, column=0, columnspan=3, pady=(20, 20), padx=20, sticky="w")
        
        # Create scrollable frame
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.symptom_vars = {}
        row = 0
        
        for symptom in SYMPTOMS:
            label = ttk.Label(scrollable_frame, text=SYMPTOM_LABELS[symptom])
            label.grid(row=row, column=0, sticky="w", padx=20, pady=5)
            
            var = tk.IntVar(value=0)
            self.symptom_vars[symptom] = var
            
            # Scale widget
            scale = ttk.Scale(
                scrollable_frame,
                from_=0,
                to=6,
                variable=var,
                orient="horizontal",
                length=200,
                command=lambda v, s=symptom: self._update_metrics()
            )
            scale.grid(row=row, column=1, padx=10, pady=5)
            
            # Value label
            value_label = ttk.Label(scrollable_frame, text="0", width=3)
            value_label.grid(row=row, column=2, padx=5, pady=5)
            self.symptom_vars[f"{symptom}_label"] = value_label
            
            # Update label when scale changes (capture var in closure)
            def update_label(*args, v=var, vl=value_label):
                vl.config(text=str(v.get()))
            var.trace_add("write", update_label)
            
            row += 1
        
        canvas.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        scrollbar.grid(row=1, column=2, sticky="ns", pady=10)
        
        # Metrics
        metrics_frame = ttk.Frame(self)
        metrics_frame.grid(row=2, column=0, columnspan=3, pady=20, padx=20, sticky="ew")
        
        self.count_label = ttk.Label(metrics_frame, text="Symptom Count: 0", 
                                     font=("TkDefaultFont", 10, "bold"))
        self.count_label.grid(row=0, column=0, padx=20)
        
        self.severity_label = ttk.Label(metrics_frame, text="Symptom Severity Sum: 0",
                                     font=("TkDefaultFont", 10, "bold"))
        self.severity_label.grid(row=0, column=1, padx=20)
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        self.complete = True  # All symptoms default to 0, so complete by default
    
    def _update_metrics(self) -> None:
        """Update symptom count and severity sum display."""
        count = sum(1 for var in self.symptom_vars.values() 
                   if isinstance(var, tk.IntVar) and var.get() > 0)
        severity_sum = sum(var.get() for var in self.symptom_vars.values() 
                          if isinstance(var, tk.IntVar))
        
        self.count_label.config(text=f"Symptom Count: {count}")
        self.severity_label.config(text=f"Symptom Severity Sum: {severity_sum}")
    
    def load_state(self) -> None:
        state = self.app.assessment_state
        symptoms = state.get("symptoms", {})
        for symptom in SYMPTOMS:
            value = symptoms.get(symptom, 0)
            if symptom in self.symptom_vars:
                self.symptom_vars[symptom].set(value)
        self._update_metrics()
    
    def collect_data(self) -> None:
        state = self.app.assessment_state
        symptoms = {}
        for symptom in SYMPTOMS:
            symptoms[symptom] = self.symptom_vars[symptom].get()
        
        # Calculate metrics
        symptom_count = sum(1 for v in symptoms.values() if v > 0)
        symptom_severity_total = sum(symptoms.values())
        
        state["symptoms"] = {
            **symptoms,
            "symptom_count": symptom_count,
            "symptom_severity_total": symptom_severity_total
        }
    
    def on_enter(self) -> None:
        super().on_enter()
        # Focus first scale if available
        for widget in self.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.focus_set()
                break

