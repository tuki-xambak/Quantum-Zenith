"""
XAMBAK Main Chat Window
=======================
Chat interface for interacting with assistant.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
from datetime import datetime

class AssistantWindow(tk.Toplevel):
    """Main chat window"""
    
    def __init__(self, parent, assistant, config):
        super().__init__(parent)
        
        self.assistant = assistant
        self.config = config
        self.is_open = True
        
        # Window setup
        self.title("XAMBAK Assistant 🤖")
        self.geometry("700x800")
        self.resizable(True, True)
        self.config(bg='#ecf0f1')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # ===== HEADER =====
        header = tk.Frame(self, bg='#3498db', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 XAMBAK Assistant v2.0",
            font=('Arial', 18, 'bold'),
            bg='#3498db',
            fg='white'
        )
        title.pack(pady=8)
        
        # Status indicator
        self.status = tk.Label(
            header,
            text="🟢 Ready",
            font=('Arial', 10),
            bg='#3498db',
            fg='#2ecc71'
        )
        self.status.pack()
        
        # ===== CHAT DISPLAY =====
        self.chat_display = scrolledtext.ScrolledText(
            self,
            height=25,
            width=80,
            bg='#ffffff',
            fg='#2c3e50',
            font=('Courier', 10),
            state=tk.DISABLED,
            relief=tk.FLAT,
            bd=1
        )
        self.chat_display.pack(padx=12, pady=10, fill=tk.BOTH, expand=True)
        
        # Configure text tags
        self.chat_display.tag_configure("user", foreground="#3498db", font=('Arial', 10, 'bold'))
        self.chat_display.tag_configure("assistant", foreground="#27ae60", font=('Arial', 10))
        self.chat_display.tag_configure("system", foreground="#e74c3c", font=('Arial', 9, 'italic'))
        self.chat_display.tag_configure("timestamp", foreground="#95a5a6", font=('Arial', 8))
        
        # Initial message
        self._add_message("system", "✨ XAMBAK Assistant ready! Type your message below.")
        
        # ===== INPUT AREA =====
        input_frame = tk.Frame(self, bg='#ecf0f1')
        input_frame.pack(fill=tk.X, padx=12, pady=10)
        
        self.input_field = tk.Entry(
            input_frame,
            font=('Arial', 11),
            bg='#ffffff',
            fg='#2c3e50',
            relief=tk.FLAT,
            bd=1
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.input_field.bind('<Return>', self._send_message)
        self.input_field.focus()
        
        send_btn = tk.Button(
            input_frame,
            text="Send ➤",
            command=self._send_message,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            cursor='hand2',
            activebackground='#2980b9'
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        settings_btn = tk.Button(
            input_frame,
            text="⚙️",
            command=self._open_settings,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10),
            relief=tk.FLAT,
            padx=10,
            cursor='hand2',
            activebackground='#7f8c8d'
        )
        settings_btn.pack(side=tk.LEFT)
        
        # ===== FOOTER =====
        footer = tk.Frame(self, bg='#34495e', height=30)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        footer_label = tk.Label(
            footer,
            text="💡 Tip: Type 'help' to see all commands",
            font=('Arial', 8),
            bg='#34495e',
            fg='#ecf0f1'
        )
        footer_label.pack(pady=5)
        
        # Window events
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.focus()
    
    def _send_message(self, event=None):
        """Send message to assistant"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        # Display user message
        self._add_message("user", f"You: {message}")
        self.input_field.delete(0, tk.END)
        
        # Set status to processing
        self.status.config(text="⏳ Processing...", fg='#f39c12')
        self.update()
        
        # Process in background
        thread = threading.Thread(target=self._process_async, args=(message,))
        thread.daemon = True
        thread.start()
    
    def _process_async(self, message: str):
        """Process message asynchronously"""
        try:
            response = self.assistant.process_message(message)
            self.root.after(0, self._add_message, "assistant", f"Assistant: {response}")
        except Exception as e:
            error_msg = f"Error: {str(e)[:100]}"
            self.root.after(0, self._add_message, "system", f"⚠️ {error_msg}")
        finally:
            self.root.after(0, self._update_status_ready)
    
    def _update_status_ready(self):
        """Update status to ready"""
        self.status.config(text="🟢 Ready", fg='#2ecc71')
    
    def _add_message(self, tag: str, message: str):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def _open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings window coming soon!\n\n"
            "Current settings:\n"
            f"• Button position: {self.config.get('button_position')}\n"
            f"• Theme: {self.config.get('theme')}\n"
            f"• Voice enabled: {self.config.get('voice_enabled')}"
        )
    
    def _on_close(self):
        """Handle window close"""
        self.is_open = False
        self.destroy()
