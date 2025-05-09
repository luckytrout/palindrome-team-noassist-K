import re
import tkinter as tk
from tkinter import messagebox, filedialog  
import datetime
import os
import json
from palindrome_stats import PalindromeStats

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
    cleaned = re.sub(r'[^A-Za-z0-9 ]+', '', text).strip()
    return 'phrase' if ' ' in cleaned else 'single-word'

class PalindromeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Palindrome Puzzle Game")
        self.data = load_data()
        self.stats = PalindromeStats(self.data)

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
        game_menu.add_command(label="Show Saved Words", command=self.show_words)
        game_menu.add_command(label="Attempts", command=self.show_attempts)
        game_menu.add_command(label="Successes", command=self.show_successes)
        game_menu.add_command(label="Failures", command=self.show_failures)
        game_menu.add_command(label="Show Leaderboard", command=self.show_leaderboard)
        game_menu.add_command(label="Average Palindrome Length", command=self.show_average_length)
        game_menu.add_command(label="Export Session Summary", command=self.export_session_summary)  # added
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=root.quit)

        self.last_access_label = tk.Label(
            root, text=f"Last access: {self.data['last_access']}", font=("Arial", 10))
        self.last_access_label.pack(pady=5)

    def check_palindrome(self):
        word = self.entry.get().strip()
        self.clear_frames()

        if not word.isalpha():
            messagebox.showwarning("Invalid input", "Please enter alphabetic characters only.")
            return

        self.data['attempts'] += 1

        for char in word:
            tk.Label(self.letters_frame, text=char, font=("Courier", 18)).pack(side=tk.LEFT)
        for char in word[::-1]:
            tk.Label(self.reverse_frame, text=char, font=("Courier", 18)).pack(side=tk.LEFT)

        if word.lower() == word[::-1].lower():
            messagebox.showinfo("Result", "You are successful!")
            if len(leaderboard) < 3:
                leaderboard.append(word)
            else:
                min_word = min(leaderboard, key=len)
                if len(word) > len(min_word):
                    leaderboard[leaderboard.index(min_word)] = word
            self.data['successes'] += 1
            self.stats.update_stats(word)
            feedback = self.stats.compare_to_average(word)
            messagebox.showinfo("Feedback", feedback)
        else:
            messagebox.showerror("Result", "You failed. Again!")
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
                messagebox.showinfo("Saved", f"'{word}' saved to dictionary.")
            else:
                messagebox.showinfo("Duplicate", f"'{word}' is already saved.")
        else:
            messagebox.showwarning("Not a Palindrome", "Only palindromes can be saved.")

    def show_words(self):
        words = self.data['saved_words']
        messagebox.showinfo("Saved Words", "\n".join(words) if words else "No words saved yet.")

    def show_attempts(self):
        messagebox.showinfo("Attempts", f"Total attempts: {self.data['attempts']}")

    def show_successes(self):
        messagebox.showinfo("Successes", f"Successful attempts: {self.data['successes']}")

    def show_failures(self):
        messagebox.showinfo("Failures", f"Failed attempts: {self.data['failures']}")

    def show_leaderboard(self):
        if leaderboard:
            messagebox.showinfo("Leaderboard", "\n".join(leaderboard))
        else:
            messagebox.showinfo("Leaderboard", "No successful palindromes yet.")

    def show_average_length(self):
        avg_length = self.stats.get_average_length()
        messagebox.showinfo("Average Length", f"Average palindrome length: {avg_length:.2f}")

    def export_session_summary(self):
        summary = {
            "total_attempts": self.data["attempts"],
            "successful_palindromes": self.data["successes"],
            "failed_attempts": self.data["failures"],
            "saved_palindromes": self.data["saved_words"],
            "last_access": self.data["last_access"]
        }

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Session Summary"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(summary, f, indent=4)
                messagebox.showinfo("Exported", f"Session summary saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save session summary:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PalindromeApp(root)
    root.mainloop()
