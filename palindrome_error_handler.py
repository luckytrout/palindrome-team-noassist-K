from tkinter import messagebox
from tkinter import Toplevel, Label, Button


class ErrorHandler:
    @staticmethod
    def validate_input(word: str) -> bool:
        """
        Validate the input word to ensure it is a palindrome.
        """
        if not word:
            ErrorHandler.show_popup("Input cannot be empty.", "warning")
            return False
        if any(char.isdigit() for char in word):
            ErrorHandler.show_popup("Numbers are not allowed.", "warning")
            return False
        if not word.isalpha():
            ErrorHandler.show_popup("Special characters are not allowed. Use letters only.", "warning")
            return False
        return True
    
    @staticmethod
    def show_popup(message: str, level: str = "info"):
        """
        Show a popup message with the specified message and type.
        """
        colors = {
            "info": "green",
            "warning": "orange",
            "error": "red"
        }
        title_map = {
            "info": "Info",
            "warning": "Warning",
            "error": "Error"
        }

        popup = Toplevel()
        popup.title(title_map.get(level, "Message"))
        popup.attributes("-topmost", True)

        label = Label(popup, text=message, font=("Arial", 12), fg=colors.get(level, "black"), wraplength=280, justify="center")
        label.pack(pady=20)

        btn = Button(popup, text="OK", command=popup.destroy)
        btn.pack(pady=10)

        popup.grab_set()

    @staticmethod
    def show_error(title: str, message: str):
        """
        Show an error message box.
        """
        ErrorHandler.show_popup(message, "error")


    @staticmethod
    def show_info(title: str, message: str):
        """
        Show an information message box.
        """
        ErrorHandler.show_popup(message, "info")
    
    @staticmethod
    def show_failure(title: str, message: str):
        """
        Show a failure message box.
        """
        ErrorHandler.show_popup(message, "error")
        