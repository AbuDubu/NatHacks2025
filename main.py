#!/usr/bin/env python3
"""
Neuro Assessment GUI (SCAT-6 Inspired)
A multi-step wizard-style desktop application for conducting neuro assessments.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
import json
from datetime import datetime
from typing import List

from base import BaseStepFrame
from utils import initialize_assessment_state
from constants import UI_TEXTS
from steps import (
    IntroStep,
    SymptomsStep,
    ImmediateMemoryStep,
    BalanceStep,
    EyeTrackingStep,
    DelayedRecallStep,
    ReviewStep
)


class App(tk.Tk):
    """Main application controller."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize state
        self.assessment_state = initialize_assessment_state()
        self.assessment_state["meta"]["start_timestamp"] = datetime.now().isoformat()
        
        # Window setup
        self.title("Neuro Assessment (SCAT-6 Inspired)")
        self.geometry("800x700")
        
        # Try to use clam theme, fallback to default
        try:
            style = ttk.Style()
            style.theme_use("clam")
        except:
            pass
        
        # Configure grid weights for responsiveness
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Current step index
        self.current_step = 0
        
        # Create frames
        self.frames: List[BaseStepFrame] = [
            IntroStep(self, self),
            SymptomsStep(self, self),
            ImmediateMemoryStep(self, self),
            BalanceStep(self, self),
            EyeTrackingStep(self, self),
            DelayedRecallStep(self, self),
            ReviewStep(self, self)
        ]
        
        # Populate all frames
        for frame in self.frames:
            frame.populate()
            frame.bind_events()
        
        # Create UI components
        self._create_header()
        self._create_footer()
        self._create_menu()
        
        # Show first step
        self.go_to(0)
        
        # Keyboard shortcuts
        self.bind("<Alt-Left>", lambda e: self.back())
        self.bind("<Alt-Right>", lambda e: self.next())
        self.bind("<Return>", lambda e: self._handle_enter())
    
    def _create_header(self) -> None:
        """Create header with step title."""
        self.header_frame = ttk.Frame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.header_frame.columnconfigure(0, weight=1)
        
        self.step_title_label = ttk.Label(
            self.header_frame,
            text="",
            font=("TkDefaultFont", 12, "bold")
        )
        self.step_title_label.grid(row=0, column=0, sticky="w", padx=10)
    
    def _create_footer(self) -> None:
        """Create footer with navigation buttons and progress."""
        self.footer_frame = ttk.Frame(self)
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.footer_frame.columnconfigure(1, weight=1)
        
        # Progress indicator
        self.progress_label = ttk.Label(self.footer_frame, text="Step 1 of 7")
        self.progress_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            self.footer_frame,
            mode="determinate",
            length=200
        )
        self.progress_bar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Navigation buttons
        button_frame = ttk.Frame(self.footer_frame)
        button_frame.grid(row=0, column=2, padx=10, pady=5)
        
        self.back_button = ttk.Button(
            button_frame,
            text="Back",
            command=self.back
        )
        self.back_button.pack(side="left", padx=5)
        
        self.next_button = ttk.Button(
            button_frame,
            text="Next",
            command=self.next
        )
        self.next_button.pack(side="left", padx=5)
        
        self.save_exit_button = ttk.Button(
            button_frame,
            text="Save & Exit",
            command=self.save_and_exit
        )
        self.save_exit_button.pack(side="left", padx=5)
        
        self.finish_button = ttk.Button(
            button_frame,
            text="Finish",
            command=self.finish
        )
        # Initially hide finish button (it will be shown on last step)
        self.finish_button.pack_forget()
        self.finish_button_visible = False  # Track visibility
    
    def _create_menu(self) -> None:
        """Create menu bar."""
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        view_menu.add_command(label="Font Size: Small", command=lambda: self._set_font_size(8))
        view_menu.add_command(label="Font Size: Normal", command=lambda: self._set_font_size(10))
        view_menu.add_command(label="Font Size: Large", command=lambda: self._set_font_size(12))
    
    def _set_font_size(self, size: int) -> None:
        """Set font size for default font."""
        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=size)
        # Force refresh by updating all widgets
        self.update_idletasks()
    
    def _handle_enter(self) -> None:
        """Handle Enter key press."""
        if self.finish_button_visible and self.finish_button["state"] != "disabled":
            self.finish()
        elif self.next_button["state"] != "disabled":
            self.next()
    
    def go_to(self, index: int) -> None:
        """Navigate to a specific step."""
        if 0 <= index < len(self.frames):
            # Call on_leave on current frame if it exists
            if hasattr(self.frames[self.current_step], 'on_leave'):
                self.frames[self.current_step].on_leave()
            
            # Hide current frame
            if self.frames[self.current_step].winfo_viewable():
                self.frames[self.current_step].grid_remove()
            
            # Show new frame
            self.current_step = index
            self.frames[index].grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            self.frames[index].on_enter()
            
            # Update header
            step_titles = [
                UI_TEXTS["step_intro"],
                UI_TEXTS["step_symptoms"],
                UI_TEXTS["step_immediate_memory"],
                UI_TEXTS["step_balance"],
                UI_TEXTS["step_eye_tracking"],
                UI_TEXTS["step_delayed_recall"],
                UI_TEXTS["step_review"]
            ]
            self.step_title_label.config(text=step_titles[index])
            
            # Update progress
            progress = ((index + 1) / len(self.frames)) * 100
            self.progress_bar["value"] = progress
            self.progress_label.config(text=f"Step {index + 1} of {len(self.frames)}")
            
            # Update navigation
            self.update_navigation()
    
    def next(self) -> None:
        """Move to next step."""
        if self.current_step < len(self.frames) - 1:
            # Collect data from current step
            self.frames[self.current_step].collect_data()
            # Move to next
            self.go_to(self.current_step + 1)
    
    def back(self) -> None:
        """Move to previous step."""
        if self.current_step > 0:
            # Collect data from current step
            self.frames[self.current_step].collect_data()
            # Move to previous
            self.go_to(self.current_step - 1)
    
    def update_navigation(self) -> None:
        """Update button states based on current step."""
        # Back button
        self.back_button.config(state="normal" if self.current_step > 0 else "disabled")
        
        # Next button
        is_complete = self.frames[self.current_step].is_complete()
        is_last = self.current_step == len(self.frames) - 1
        
        # Finish button (only on last step)
        if is_last:
            # Hide Next button, show Finish button
            self.next_button.pack_forget()
            self.finish_button.pack(side="left", padx=5)
            self.finish_button.config(state="normal" if is_complete else "disabled")
            self.finish_button_visible = True
        else:
            # Hide Finish button, show Next button
            self.finish_button.pack_forget()
            self.next_button.pack(side="left", padx=5)
            self.next_button.config(
                state="normal" if is_complete else "disabled"
            )
            self.finish_button_visible = False
    
    def save_to_json(self, filepath: str) -> bool:
        """Save assessment state to JSON file."""
        try:
            # Update timestamps
            end_time = datetime.now()
            start_time = datetime.fromisoformat(self.assessment_state["meta"]["start_timestamp"])
            duration = (end_time - start_time).total_seconds()
            
            self.assessment_state["meta"]["end_timestamp"] = end_time.isoformat()
            self.assessment_state["meta"]["duration_seconds"] = duration
            
            # Ensure all steps have collected their data
            self.frames[self.current_step].collect_data()
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.assessment_state, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
            return False
    
    def save_and_exit(self) -> None:
        """Save current progress and exit."""
        if messagebox.askyesno("Save & Exit", "Are you sure you want to save and exit?"):
            # Collect current step data
            self.frames[self.current_step].collect_data()
            
            # Generate filename
            full_name = self.assessment_state["participant"].get("full_name", "Unknown")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"NeuroAssessment_{full_name}_{timestamp}.json"
            
            # Open save dialog
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=default_filename
            )
            
            if filepath:
                if self.save_to_json(filepath):
                    messagebox.showinfo("Success", "Assessment saved successfully!")
                    self.quit()
    
    def finish(self) -> None:
        """Finish assessment and save."""
        # Collect current step data
        self.frames[self.current_step].collect_data()
        
        # Generate filename
        full_name = self.assessment_state["participant"].get("full_name", "Unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"NeuroAssessment_{full_name}_{timestamp}.json"
        
        # Open save dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filepath:
            if self.save_to_json(filepath):
                messagebox.showinfo("Success", "Assessment completed and saved successfully!")
                if messagebox.askyesno("Exit", "Would you like to exit the application?"):
                    self.quit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
