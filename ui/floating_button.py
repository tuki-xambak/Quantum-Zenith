"""
XAMBAK Floating Button UI
==========================
Non-intrusive overlay button.
"""

import tkinter as tk
from tkinter import font
from typing import Callable

class FloatingButton(tk.Toplevel):
    """Floating button overlay"""
    
    def __init__(self, parent, callback: Callable, position: str = "top-right", icon: str = "🤖"):
        super().__init__(parent)
        
        self.callback = callback
        self.position = position
        self.icon = icon
        self.drag_data = {'x': 0, 'y': 0}
        
        # Configure window
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.9)
        self.overrideredirect(True)  # Remove window decorations
        
        self.config(bg='#2c3e50', relief=tk.RAISED, bd=2)
        
        # Button
        btn_font = font.Font(size=16)
        self.btn = tk.Button(
            self,
            text=icon,
            font=btn_font,
            command=self._on_click,
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            relief=tk.FLAT,
            padx=12,
            pady=12,
            cursor='hand2',
            bd=0
        )
        self.btn.pack()
        
        # Tooltip
        self.tooltip = None
        self.btn.bind('<Enter>', self._show_tooltip)
        self.btn.bind('<Leave>', self._hide_tooltip)
        
        # Position
        self._position_button()
        
        # Dragging
        self.btn.bind('<B1-Motion>', self._drag)
        self.btn.bind('<Button-1>', self._drag_start)
    
    def _position_button(self):
        """Position button on screen"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        positions = {
            "top-right": (screen_width - 80, 20),
            "top-left": (20, 20),
            "bottom-right": (screen_width - 80, screen_height - 80),
            "bottom-left": (20, screen_height - 80),
        }
        
        x, y = positions.get(self.position, (screen_width - 80, 20))
        self.geometry(f"+{x}+{y}")
    
    def _on_click(self):
        """Handle button click"""
        try:
            self.callback()
        except Exception as e:
            print(f"❌ Button click error: {e}")
    
    def _drag_start(self, event):
        """Start drag operation"""
        self.drag_data['x'] = event.x_root - self.winfo_x()
        self.drag_data['y'] = event.y_root - self.winfo_y()
    
    def _drag(self, event):
        """Handle drag"""
        x = event.x_root - self.drag_data['x']
        y = event.y_root - self.drag_data['y']
        self.geometry(f"+{x}+{y}")
    
    def _show_tooltip(self, event):
        """Show tooltip on hover"""
        if self.tooltip:
            return
        
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.attributes('-alpha', 0.95)
        
        label = tk.Label(
            self.tooltip,
            text="Click to open XAMBAK Assistant 🤖",
            bg='#34495e',
            fg='#ecf0f1',
            padx=10,
            pady=5,
            font=('Arial', 9)
        )
        label.pack()
        
        x = self.winfo_x() + self.winfo_width() + 10
        y = self.winfo_y()
        self.tooltip.geometry(f"+{x}+{y}")
    
    def _hide_tooltip(self, event):
        """Hide tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
