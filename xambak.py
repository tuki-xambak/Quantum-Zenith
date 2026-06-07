"""
XAMBAK Enhanced Main Application
With all features integrated
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time
from datetime import datetime
import os
from pathlib import Path

# Import features
from music_feature import play_music, play_spotify
from notes_feature import add_note, list_notes, search_notes
from reminders_feature import add_reminder, list_reminders, check_reminders
from search_feature import search_wikipedia, search_duckduckgo

# Create data directory
DATA_DIR = Path.home() / ".xambak"
DATA_DIR.mkdir(exist_ok=True)

class AdvancedAssistant:
    """AI Assistant with all features"""
    
    def __init__(self):
        self.commands = {
            "müzik": self.handle_music,
            "music": self.handle_music,
            "youtube": self.handle_music,
            "spotify": self.handle_spotify,
            "not": self.handle_note,
            "note": self.handle_note,
            "ara": self.handle_search,
            "search": self.handle_search,
            "wikipedia": self.handle_wikipedia,
            "hatırlat": self.handle_reminder,
            "reminder": self.handle_reminder,
            "hatırlatıcı": self.handle_reminder,
            "listele": self.handle_list,
            "list": self.handle_list,
            "help": self.handle_help,
            "yardım": self.handle_help,
            "saat": self.handle_time,
            "time": self.handle_time,
            "espri": self.handle_joke,
            "joke": self.handle_joke,
        }
    
    def get_response(self, user_input):
        """Get response for user input"""
        user_input_lower = user_input.lower().strip()
        
        # Check for commands
        for cmd, handler in self.commands.items():
            if cmd in user_input_lower:
                try:
                    return handler(user_input)
                except Exception as e:
                    return f"❌ Hata: {str(e)[:100]}"
        
        # Default responses
        if any(w in user_input_lower for w in ["merhaba", "hello", "hi", "hey", "selam"]):
            return "Merhaba! 👋 Sana nasıl yardımcı olabilirim?"
        
        if any(w in user_input_lower for w in ["nasılsın", "how are you", "naber"]):
            return "Harika, teşekkür edersin! 😊 Sen nasılsın?"
        
        return "Anlıyorum! 🤔 Lütfen daha açık açıkla veya 'help' yazarak komutları görebilirsiniz."
    
    def handle_music(self, text):
        """Handle music command"""
        query = text.replace("müzik", "").replace("music", "").replace("youtube", "").strip()
        if not query:
            query = "random music"
        return play_music(query)
    
    def handle_spotify(self, text):
        """Handle Spotify command"""
        query = text.replace("spotify", "").strip()
        if not query:
            query = "random music"
        return play_spotify(query)
    
    def handle_note(self, text):
        """Handle note command"""
        content = text.replace("not", "").replace("note", "").replace("kaydet", "").strip()
        if not content:
            return list_notes()
        title = content[:30] if len(content) > 30 else content
        return add_note(title, content)
    
    def handle_search(self, text):
        """Handle search command"""
        query = text.replace("ara", "").replace("search", "").strip()
        if not query:
            return "❌ Lütfen arama terimi girin"
        return search_wikipedia(query)
    
    def handle_wikipedia(self, text):
        """Handle Wikipedia command"""
        query = text.replace("wikipedia", "").strip()
        if not query:
            return "❌ Lütfen arama terimi girin"
        return search_wikipedia(query)
    
    def handle_reminder(self, text):
        """Handle reminder command"""
        text_clean = text.replace("hatırlat", "").replace("reminder", "").replace("hatırlatıcı", "").strip()
        
        # Parse: "saat 30 dakika sonra" or "30 dakika sonra"
        if "30 dakika" in text_clean or "otuz dakika" in text_clean:
            return add_reminder("Hatırlatıcı", "30 dakika sonra")
        elif "1 saat" in text_clean or "bir saat" in text_clean:
            return add_reminder("Hatırlatıcı", "1 saat sonra")
        else:
            return add_reminder("Hatırlatıcı", text_clean or "1 saat sonra")
    
    def handle_list(self, text):
        """Handle list command"""
        if "not" in text.lower():
            return list_notes()
        else:
            return list_reminders()
    
    def handle_help(self, text):
        """Handle help command"""
        return """📚 Komutlar:

🎵 Müzik:
  • 'müzik çal [şarkı]' - YouTube'da müzik aç
  • 'spotify [şarkı]' - Spotify'da müzik aç

📝 Notlar:
  • 'not kaydet [içerik]' - Not ekle
  • 'notları listele' - Tüm notları göster

🔍 Arama:
  • 'ara [konu]' - Wikipedia'da ara
  • 'wikipedia [konu]' - Wikipedia'da ara

⏰ Hatırlatıcılar:
  • 'hatırlat [metin]' - Hatırlatıcı kur
  • 'hatırlatıcıları listele' - Tüm hatırlatıcıları göster

🎤 Genel:
  • 'saat' - Saati söyle
  • 'espri' - Şaka yap
  • 'help' - Yardım"""
    
    def handle_time(self, text):
        """Handle time command"""
        return f"🕐 Şu an: {datetime.now().strftime('%H:%M:%S')}"
    
    def handle_joke(self, text):
        """Handle joke command"""
        jokes = [
            "Neden programcılar hep ışığı sönerler? Çünkü bugs karanlıktan çıkar! 🐛",
            "Bir programcı uyurken rüyasında kaç loop var? ∞ (sonsuz)! 🔄",
            "Neden Java programcıları gözlük takar? C# yapamadıkları için! 👓",
            "Git merge conflict'i nereden bulunur? Sorun yaşadığında! 😅",
            "Stack overflow'da hangi balık yaşar? Recursive fish! 🐠",
        ]
        import random
        return "😄 " + random.choice(jokes)


class XambakUI:
    """Enhanced GUI for XAMBAK"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("XAMBAK Assistant 🤖 v2.0")
        self.root.geometry("800x700")
        self.root.config(bg="#2c3e50")
        
        self.assistant = AdvancedAssistant()
        
        # Create UI
        self.create_header()
        self.create_chat_area()
        self.create_input_area()
        self.create_footer()
        
        # Add welcome message
        self.add_message("system", "✨ XAMBAK Assistant v2.0 başlatıldı!\n'help' yazarak tüm komutları görebilirsiniz.")
        
        # Start reminder checker
        self.start_reminder_checker()
    
    def create_header(self):
        """Create header"""
        header = tk.Frame(self.root, bg="#3498db", height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="🤖 XAMBAK Assistant v2.0",
            font=("Arial", 22, "bold"),
            bg="#3498db",
            fg="white"
        )
        title.pack(pady=10)
        
        subtitle = tk.Label(
            header,
            text="Müzik • Not • Arama • Hatırlatıcı • Ve Daha Fazlası!",
            font=("Arial", 10),
            bg="#3498db",
            fg="#ecf0f1"
        )
        subtitle.pack()
        
        status = tk.Label(
            header,
            text="🟢 Hazır",
            font=("Arial", 10),
            bg="#3498db",
            fg="#2ecc71"
        )
        status.pack(pady=5)
        self.status = status
    
    def create_chat_area(self):
        """Create chat display"""
        chat_frame = tk.Frame(self.root, bg="#ecf0f1")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            bg="white",
            fg="#2c3e50",
            font=("Courier", 10),
            state=tk.DISABLED,
            relief=tk.FLAT,
            bd=1
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure text styles
        self.chat_display.tag_configure("user", foreground="#3498db", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("assistant", foreground="#27ae60", font=("Arial", 10))
        self.chat_display.tag_configure("system", foreground="#e74c3c", font=("Arial", 9, "italic"))
    
    def create_input_area(self):
        """Create input area"""
        input_frame = tk.Frame(self.root, bg="#2c3e50")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="white",
            fg="#2c3e50",
            relief=tk.FLAT,
            bd=1
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message)
        self.input_field.focus()
        
        send_btn = tk.Button(
            input_frame,
            text="Gönder ➤",
            command=self.send_message,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            padx=20,
            cursor="hand2",
            activebackground="#2980b9"
        )
        send_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        help_btn = tk.Button(
            input_frame,
            text="❓",
            command=self.show_help,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 12),
            relief=tk.FLAT,
            padx=12,
            cursor="hand2",
            activebackground="#7f8c8d"
        )
        help_btn.pack(side=tk.LEFT)
    
    def create_footer(self):
        """Create footer"""
        footer = tk.Frame(self.root, bg="#34495e", height=50)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        footer_label = tk.Label(
            footer,
            text="💡 'help' yazarak komutları görebilirsiniz | Tüm veriler yerel olarak saklanır",
            font=("Arial", 9),
            bg="#34495e",
            fg="#ecf0f1"
        )
        footer_label.pack(pady=8)
    
    def add_message(self, tag, message):
        """Add message to chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "system")
        self.chat_display.insert(tk.END, f"{message}\n\n", tag)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Send message to assistant"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        # Show user message
        self.add_message("user", f"Siz: {message}")
        self.input_field.delete(0, tk.END)
        
        # Update status
        self.status.config(text="⏳ Düşünüyor...", fg="#f39c12")
        self.root.update()
        
        # Get response in background
        thread = threading.Thread(target=self.get_response_async, args=(message,))
        thread.daemon = True
        thread.start()
    
    def get_response_async(self, message):
        """Get response asynchronously"""
        time.sleep(0.3)  # Simulate thinking
        response = self.assistant.get_response(message)
        self.root.after(0, self.add_message, "assistant", f"Assistant: {response}")
        self.root.after(0, self.update_status_ready)
    
    def update_status_ready(self):
        """Update status to ready"""
        self.status.config(text="🟢 Hazır", fg="#2ecc71")
    
    def show_help(self):
        """Show help dialog"""
        help_text = self.assistant.handle_help("")
        messagebox.showinfo("Yardım", help_text)
    
    def start_reminder_checker(self):
        """Start reminder checker"""
        def check_loop():
            while True:
                try:
                    triggered = check_reminders()
                    for title in triggered:
                        messagebox.showinfo("⏰ Hatırlatıcı", f"{title}")
                        self.add_message("system", f"⏰ Hatırlatıcı: {title}")
                except:
                    pass
                time.sleep(10)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("🚀 XAMBAK Assistant v2.0 Başlatılıyor...")
    print("="*60)
    print("✅ Uygulama açıldı!")
    print("💡 Pencereyi kontrol edin\n")
    
    root = tk.Tk()
    app = XambakUI(root)
    app.run()


if __name__ == "__main__":
    main()
