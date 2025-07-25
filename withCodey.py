import customtkinter as ctk
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
import threading
import random
import time

# Initialize app
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Codey Chatbot ✨")
app.geometry("480x720")
app.configure(fg_color="#2D1B3C")

# Sparkling Canvas Background
canvas = ctk.CTkCanvas(app, bg="#2D1B3C", highlightthickness=0)
canvas.place(relwidth=1, relheight=1)

def create_sparkles():
    colors = ["#FFD1DC", "#FFB6C1", "#FFE4E1", "#FFCCF9"]
    for _ in range(100):
        x = random.randint(0, 480)
        y = random.randint(0, 720)
        r = random.randint(1, 3)
        canvas.create_oval(x, y, x+r, y+r, fill=random.choice(colors), outline="")

create_sparkles()

# Header Banner
header = ctk.CTkLabel(app, text="💖 Code like a girl boss! 💖", font=("Comic Sans MS", 18, "bold"), text_color="white")
header.place(x=100, y=20)

# Daily Quote
quotes = [
    "“Dream big, code bigger.”",
    "“You are capable of amazing things.”",
    "“Every bug you fix is a level up.”",
    "“She who codes, rules the world.”",
    "“One line of code at a time!”"
]
quote_label = ctk.CTkLabel(app, text=random.choice(quotes), font=("Comic Sans MS", 12), text_color="white")
quote_label.place(x=50, y=60)

# Emoji Avatar
avatar_label = ctk.CTkLabel(app, text="👩‍💻", font=("Arial", 60), fg_color="#FF69B4", corner_radius=50, width=100, height=100)
avatar_label.place(x=190, y=90)

# Chat Frame
chat_frame = ctk.CTkScrollableFrame(app, fg_color="white", corner_radius=20, width=440, height=250)
chat_frame.place(x=20, y=200)

# Input Entry
user_entry = ctk.CTkEntry(app, width=440, height=40, font=("Comic Sans MS", 14), corner_radius=20)
user_entry.place(x=20, y=470)

# Language Buttons
selected_lang = ctk.StringVar(value="English")
lang_options = ["English", "Tshivenda", "Tsonga", "Sepedi", "isiZulu"]
x_pos = 20
for lang in lang_options:
    btn = ctk.CTkButton(app, text=lang, fg_color="white", text_color="#5A2A54", corner_radius=20, width=80, command=lambda l=lang: selected_lang.set(l))
    btn.place(x=x_pos, y=520)
    x_pos += 90

# Buttons
send_btn = ctk.CTkButton(app, text="Send", fg_color="#FF69B4", corner_radius=20, width=100, command=lambda: handle_input())
send_btn.place(x=20, y=580)

mic_btn = ctk.CTkButton(app, text="Speak", fg_color="#FF69B4", corner_radius=20, width=100, command=lambda: listen_mic())
mic_btn.place(x=140, y=580)

reset_btn = ctk.CTkButton(app, text="Reset", fg_color="#FF69B4", corner_radius=20, width=100, command=lambda: reset_chat())
reset_btn.place(x=260, y=580)

# Chatbot Logic
translator = Translator()
engine = pyttsx3.init()
engine.setProperty('rate', 160)
typing_animation_running = False

def create_bubble(text, sender="user"):
    bubble_color = "#2C0C14" if sender == "user" else "#D1C4E9"
    bubble = ctk.CTkFrame(chat_frame, fg_color=bubble_color, corner_radius=15)
    message = ctk.CTkLabel(bubble, text=text, text_color="#5A2A54", font=("Comic Sans MS", 14), wraplength=300, justify="left")
    message.pack(padx=10, pady=5)
    bubble.pack(pady=8, padx=10, anchor="w" if sender=="user" else "e")
    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1)

def handle_input():
    user_input = user_entry.get().strip()
    if user_input == "":
        return
    create_bubble(user_input, sender="user")
    user_entry.delete(0, "end")
    threading.Thread(target=process_bot_response, args=(user_input,)).start()

def process_bot_response(user_input):
    typing_label = ctk.CTkLabel(chat_frame, text="", text_color="#888888", font=("Comic Sans MS", 12))
    typing_label.pack(pady=2, anchor="e")
    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1)

    global typing_animation_running
    typing_animation_running = True
    animate_typing_dots(typing_label)

    time.sleep(2)

    responses = {
        "what is javascript": "📚 JavaScript is a scripting language used to make web pages interactive.",
        "what is a variable": "🔑 A variable stores data values in programming.",
        "what is an array": "📦 An array stores multiple values in a single variable.",
    }

    response = responses.get(user_input.lower(), "🤖 I'm still learning! Ask me JavaScript questions.")
    lang_codes = {"Tshivenda": "ven", "Tsonga": "ts", "Sepedi": "nso", "isiZulu": "zu", "English": "en"}
    translated = translator.translate(response, dest=lang_codes.get(selected_lang.get(), "en")).text

    typing_animation_running = False
    typing_label.destroy()
    create_bubble(translated, sender="bot")
    threading.Thread(target=speak, args=(translated,)).start()

def animate_typing_dots(label):
    dots = ["", ".", "..", "..."]
    i = 0
    def loop():
        nonlocal i
        if not typing_animation_running:
            label.configure(text="")
            return
        label.configure(text=f"👩‍💻 Codey is typing{dots[i % 4]}")
        i += 1
        label.after(500, loop)
    loop()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        user_entry.delete(0, "end")
        user_entry.insert(0, "Listening...")
        try:
            audio = recognizer.listen(source, timeout=4)
            text = recognizer.recognize_google(audio)
            user_entry.delete(0, "end")
            user_entry.insert(0, text)
            handle_input()
        except Exception:
            user_entry.delete(0, "end")
            user_entry.insert(0, "Couldn't understand you.")

def reset_chat():
    for widget in chat_frame.winfo_children():
        widget.destroy()

app.mainloop()

