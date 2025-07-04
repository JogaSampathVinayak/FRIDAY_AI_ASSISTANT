import customtkinter as ctk
import threading
from listener import take_command
from brain import get_response
from speech import speak
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FridayApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FRIDAY AI Assistant")
        self.geometry("600x400")
        self.resizable(False, False)

        # Add a frame for layout (fixes blank screen issue)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Label
        self.label = ctk.CTkLabel(self.main_frame, text="Ask me anything", font=("Arial", 18))
        self.label.pack(pady=(0, 10))

        # Chat display
        self.chat_display = ctk.CTkTextbox(self.main_frame, width=520, height=220)
        self.chat_display.pack(pady=(0, 10))

        # Speak button
        self.ask_button = ctk.CTkButton(self.main_frame, text="🎤 Speak to FRIDAY", command=self.listen_to_user)
        self.ask_button.pack(pady=(0, 10))

        # Clear button
        self.clear_button = ctk.CTkButton(self.main_frame, text="🧹 Clear", command=self.clear_chat)
        self.clear_button.pack()

        self.update()

    def listen_to_user(self):
        def task():
            self.ask_button.configure(state="disabled", text="🎙 Listening...")
            query = take_command()
            if query:
                self.chat_display.insert("end", f"👤 You: {query}\n")
                response = get_response(query)
                self.chat_display.insert("end", f"🤖 FRIDAY: {response}\n\n")
                speak(response)
            else:
                self.chat_display.insert("end", "⚠️ Could not hear you.\n")
            self.ask_button.configure(state="normal", text="🎤 Speak to FRIDAY")
        threading.Thread(target=task).start()

    def clear_chat(self):
        self.chat_display.delete("1.0", "end")

if __name__ == "__main__":
    app = FridayApp()
    app.mainloop()
