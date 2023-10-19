import tkinter as tk
from tkinter import messagebox
import random
from KBC_Data import Questions, Money_Prices
from lifeline50 import ranopt
import os
import re
import pygame

RED = "#FF0000"
GREEN = "#00FF00"
DEFAULT_BUTTON_COLOR = "#d9d9d9"

class StartScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.bg_image = tk.PhotoImage(file="kbc_background.png")
        self.label = tk.Label(self, image=self.bg_image)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)

        self.title_label = tk.Label(self, text="Kaun Banega Crorepati", font=("Arial", 24))
        self.title_label.pack(pady=20)

        self.name_entry = tk.Entry(self)
        self.name_entry.insert(0, "Enter your name")
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_entry_on_focus(e, "Enter your name"))
        self.name_entry.pack(pady=10)

        self.age_entry = tk.Entry(self)
        self.age_entry.insert(0, "Enter your age")
        self.age_entry.bind("<FocusIn>", lambda e: self.clear_entry_on_focus(e, "Enter your age"))
        self.age_entry.pack(pady=10)

        self.email_entry = tk.Entry(self)
        self.email_entry.insert(0, "Enter your email-id")
        self.email_entry.bind("<FocusIn>", lambda e: self.clear_entry_on_focus(e, "Enter your email-id"))
        self.email_entry.pack(pady=10)

        self.submit_button = tk.Button(self, text="Proceed", command=self.proceed_to_instructions)
        self.submit_button.pack(pady=20)

    def clear_entry_on_focus(self, event, default_text):
        if event.widget.get() == default_text:
            event.widget.delete(0, tk.END)

    def proceed_to_instructions(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        
        # Validating the inputs
        if not name or not age or not email:
            messagebox.showerror("Error", "All fields are mandatory!")
            return

        if any(char.isdigit() for char in name):
            messagebox.showerror("Error", "Name should not contain numbers.")
            return

        if not age.isdigit():
            messagebox.showerror("Error", "Age should only contain numbers.")
            return

        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Enter a valid email address.")
            return
        
        # Storing player details in parent
        self.parent.player_name = name
        self.parent.player_age = age
        self.parent.player_email = email
        
        self.destroy()
        self.parent.show_instructions()

class InstructionsScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.parent = parent
        self.title_label = tk.Label(self, text="Instructions", font=("Arial", 20))
        self.title_label.pack(pady=20)

        instructions_text = (
            "1. You will have multiple levels of questions.\n"
            "2. Each question will have a timer. Answer before time runs out.\n"
            "3. Use lifelines wisely.\n"
            "4. Ensure your answers are confirmed before submitting.\n"
            "5. Enjoy the game!"
        )
        self.instructions_label = tk.Label(self, text=instructions_text, font=("Arial", 14), wraplength=700)
        self.instructions_label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        self.destroy()
        self.parent.start_game()

class KBCGame(tk.Tk):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()


        self.title("Kon Banega Crorepati")
        self.geometry("1000x600")  # Adjusted for extra frames on left and right

        # Player details
        self.player_name = ""
        self.player_age = ""
        self.player_email = ""

        self.money = 0
        self.lifeline_50_50 = True
        self.lifeline_audience = True
        self.current_question_index = 0

        # Creating left, middle, and right frames
        self.left_frame = tk.Frame(self, width=250, bg='gray')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.middle_frame = tk.Frame(self, bg='white')
        self.middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self, width=250, bg='gray')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Left Frame - Prize and Level Details
        self.level_labels = []
        for i, prize in enumerate(Money_Prices, start=1):
            level = i
            text = f"Level {i}: Rs. {prize}"
            label = tk.Label(self.left_frame, text=text, bg='gray', fg='white')
            label.pack(pady=5)
            self.level_labels.append(label)

        # Middle Frame - Questions, Options and Timer
        self.timer_label = tk.Label(self.middle_frame, font=("Arial", 14))
        self.timer_label.pack(fill=tk.X, pady=10, anchor="ne")

        self.question_label = tk.Label(self.middle_frame, wraplength=600, font=("Arial", 16))
        self.question_label.pack(pady=20)

        self.options = [tk.Button(self.middle_frame, text="Option " + str(i), command=lambda i=i: self.check_answer(i), bg=DEFAULT_BUTTON_COLOR) for i in range(4)]
        for btn in self.options:
            btn.pack(side=tk.TOP, fill=tk.X, padx=50, pady=10)

        self.life_line_frame = tk.Frame(self.middle_frame)
        self.life_line_frame.pack(pady=20)

        self.btn_50_50 = tk.Button(self.life_line_frame, text="50-50", command=self.use_50_50)
        self.btn_50_50.grid(row=0, column=0, padx=10)
        self.btn_ask_audience = tk.Button(self.life_line_frame, text="Ask Audience", command=self.ask_audience)
        self.btn_ask_audience.grid(row=0, column=1, padx=10)

        # Right Frame - Player Details
        player_details_label = tk.Label(self.right_frame, text="Player Details", bg='gray', fg='white', font=("Arial", 16))
        player_details_label.pack(pady=10)

        self.name_label = tk.Label(self.right_frame, bg='gray', fg='white', font=("Arial", 14))
        self.name_label.pack(pady=5)

        self.age_label = tk.Label(self.right_frame, bg='gray', fg='white', font=("Arial", 14))
        self.age_label.pack(pady=5)

        self.email_label = tk.Label(self.right_frame, bg='gray', fg='white', font=("Arial", 14))
        self.email_label.pack(pady=5)

        # Initially, hide main game UI and show the start screen
        self.withdraw()
        self.start_screen = StartScreen(self)

    def load_next_question(self):
        for btn in self.options:
            btn.config(bg=DEFAULT_BUTTON_COLOR)
        if self.current_question_index >= len(Questions):
            self.end_game()
            return
        self.question_set = Questions[self.current_question_index][random.randint(0, len(Questions[self.current_question_index]) - 1)]
        self.Question, self.Options, self.Correct_Answer, self.Description = self.question_set.values()
        random.shuffle(self.Options)
        self.question_label.config(text=self.Question)
        for i, btn in enumerate(self.options):
            btn.config(text=self.Options[i])
        self.start_timer()

    def start_timer(self):
        if 0 <= self.current_question_index < 5:
            self.time_left = 30
        elif 5 <= self.current_question_index < 10:
            self.time_left = 60
        elif 10 <= self.current_question_index < 15:
            self.time_left = 90
        else:
            self.time_left = None
        if self.time_left:
            self.update_timer()

    def update_timer(self):
        minutes, seconds = divmod(self.time_left, 60)
        self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
        self.time_left -= 1
        if self.time_left >= 0:
            self.after(1000, self.update_timer)
        else:
            self.end_game()

    def check_answer(self, option_index):
        answer = messagebox.askyesno(
            "Confirm",
            f"Should this option '{self.Options[option_index]}' be locked?"
        )
        if answer:
            for btn in self.options:
                btn.config(state=tk.DISABLED)
            self.after(2000, self.reveal_answer, option_index)

    def reveal_answer(self, option_index):
        if self.Options[option_index] == self.Correct_Answer:
            self.options[option_index].config(bg=GREEN)
            self.play_audio("win.mp3")
            self.money = Money_Prices[self.current_question_index]
            self.current_question_index += 1
            self.after(3000, self.load_next_question)
        else:
            self.options[option_index].config(bg=RED)
            correct_index = self.Options.index(self.Correct_Answer)
            self.options[correct_index].config(bg=GREEN)
            self.play_audio("lose.mp3")
            self.after(6000, self.end_game)
        for btn in self.options:
            btn.config(state=tk.NORMAL)

    def use_50_50(self):
        if self.lifeline_50_50:
            self.btn_50_50.config(state=tk.DISABLED)
            self.lifeline_50_50 = False
            ranopt(self.Question, self.Options, self.Correct_Answer, self.current_question_index)
            for i, btn in enumerate(self.options):
                btn.config(text=self.Options[i])

    def ask_audience(self):
        if self.lifeline_audience:
            self.lifeline_audience = False
            self.btn_ask_audience.config(state=tk.DISABLED)
            messagebox.showinfo("Audience says", "Audience believes it's one of the options!")

    def end_game(self):
        result_text = f"You have won {self.money} Rupay!"
        messagebox.showinfo("Game Over", result_text)

        # Update leaderboard
        with open('leaderboard.txt', 'a') as file:
            file.write(f"{self.player_name},{self.money}\n")

        self.destroy()

    def show_instructions(self):
        self.instructions_screen = InstructionsScreen(self)

    def start_game(self):
        self.load_next_question()
        self.deiconify()

    def play_audio(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

if __name__ == "__main__":
    app = KBCGame()
    app.mainloop()
