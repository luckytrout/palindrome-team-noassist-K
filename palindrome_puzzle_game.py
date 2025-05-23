import re
import tkinter as tk
from tkinter import messagebox
import datetime
import os
import json
from palindrome_stats import PalindromeStats
from palindrome_error_handler import ErrorHandler

DATA_FILE = 'palindrome_data.json'
leaderboard = []


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "saved_words": [],
            "attempts": 0,
            "successes": 0,
            "failures": 0,
            "last_access": str(datetime.datetime.now())
        }


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def get_palindrome_type(text: str) -> str:
    """
    returns 'single-word' if text (ignoring punctuation) has no spaces,
    otherwise 'phrase'
    """
    cleaned = re.sub(r'[^A-Za-z0-9 ]+', '', text).strip()
    return 'phrase' if ' ' in cleaned else 'single-word'


class PalindromeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Palindrome Puzzle Game")
        self.data = load_data()
        self.stats = PalindromeStats(self.data)     # stats

        self.label = tk.Label(
            root, text="Welcome to the Palindrome Puzzle Game!", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=5)

        self.check_button = tk.Button(
        root, text="Check", command=self.check_palindrome)
        self.check_button.pack(pady=5)

        self.letters_frame = tk.Frame(root)
        self.letters_frame.pack(pady=5)

        self.reverse_frame = tk.Frame(root)
        self.reverse_frame.pack(pady=5)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        game_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Menu", menu=game_menu)
        game_menu.add_command(label="Save Word", command=self.save_word)
        game_menu.add_command(label="Show Saved Words",
                              command=self.show_words)
        game_menu.add_command(label="Attempts", command=self.show_attempts)
        game_menu.add_command(label="Successes", command=self.show_successes)
        game_menu.add_command(label="Failures", command=self.show_failures)

        game_menu.add_command(label="Show Leaderboard",
                              command=self.show_leaderboard)
        game_menu.add_command(label="Average Palindrome Length", command=self.show_average_length)

        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=root.quit)

        self.last_access_label = tk.Label(
            root, text=f"Last access: {self.data['last_access']}", font=("Arial", 10))
        self.last_access_label.pack(pady=5)

    def check_palindrome(self):
        word = self.entry.get().strip()
        self.clear_frames()

        if not ErrorHandler.validate_input(word):
            return

        self.data['attempts'] += 1

        for char in word:
            tk.Label(self.letters_frame, text=char, font=(
                "Courier", 18)).pack(side=tk.LEFT)

        for char in word[::-1]:
            tk.Label(self.reverse_frame, text=char, font=(
                "Courier", 18)).pack(side=tk.LEFT)

        if word.lower() == word[::-1].lower():
            if len(leaderboard) < 3:
                leaderboard.append(word)
            else:
                # find the smallest word
                min_word = None
                for wrd in leaderboard:
                    if not min_word:
                        min_word = wrd
                    else:
                        if len(min_word) > len(wrd):
                            min_word = wrd
                if len(leaderboard[leaderboard.index(min_word)]) < len(word.lower()):
                    leaderboard[leaderboard.index(min_word)] = word.lower()

            self.data['successes'] += 1
            
            self.stats.update_stats(word)
            feedback = self.stats.compare_to_average(word)
            ErrorHandler.show_info("Result", "You are successful\n" + feedback)
  

        else:
            ErrorHandler.show_failure("Result", "You failed. Again!")
            self.data['failures'] += 1

        self.data['last_access'] = str(datetime.datetime.now())
        save_data(self.data)

    def clear_frames(self):
        for widget in self.letters_frame.winfo_children():
            widget.destroy()
        for widget in self.reverse_frame.winfo_children():
            widget.destroy()

    def save_word(self):
        word = self.entry.get().strip()
        if word and word.lower() == word[::-1].lower():
            if word not in self.data['saved_words']:
                self.data['saved_words'].append(word)
                save_data(self.data)
                ErrorHandler.show_info("Saved", f"'{word}' saved to dictionary.")
            else:
               ErrorHandler.show_info("Duplicate", f"'{word}' is already saved.")
        else:
            ErrorHandler.show_error("Not a Palindrome", "Only palindromes can be saved.")

    def show_words(self):
        words = self.data['saved_words']
        ErrorHandler.showinfo("Saved Words", "\n".join(
            words) if words else "No words saved yet.", "info")

    def show_attempts(self):
        ErrorHandler.show_info("Attempts", f"Total attempts: {self.data['attempts']}")

    def show_successes(self):
        ErrorHandler.show_info("Successes", f"Successful attempts: {self.data['successes']}")

    def show_failures(self):
        ErrorHandler.show_info("Failures", f"Failed attempts: {self.data['failures']}")
        
    def show_leaderboard(self):
        leaderboard_map = [(word, len(word)) for word in leaderboard]
        print(leaderboard_map)
        messagebox.showinfo(
            "Leaderboard", f"Top 3: {leaderboard_map}")
        
    def show_average_length(self):
        avg = self.stats.get_average_length()
        if avg == 0:
            messagebox.showinfo("Average Length", "No palindromes entered yet.")
        else:
            messagebox.showinfo("Average Length", f"Average palindrome length: {avg:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PalindromeApp(root)
    root.mainloop()
