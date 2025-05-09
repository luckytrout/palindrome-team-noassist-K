# palindrome_stats.py

class PalindromeStats:
    def __init__(self, data):
        # Ensure backward compatibility
        self.data = data
        self.data.setdefault("palindrome_count", 0)
        self.data.setdefault("palindrome_total_length", 0)

    def update_stats(self, word):
        """Update stats when a new palindrome is found."""
        self.data['palindrome_count'] += 1
        self.data['palindrome_total_length'] += len(word)

    def get_average_length(self):
        """Return average palindrome length."""
        if self.data['palindrome_count'] == 0:
            return 0
        return self.data['palindrome_total_length'] / self.data['palindrome_count']

    def compare_to_average(self, word):
        """Return feedback comparing word length to average."""
        average = self.get_average_length()
        length = len(word)
        if length > average:
            return f"This palindrome is longer than the average ({average:.2f})."
        elif length < average:
            return f"This palindrome is shorter than the average ({average:.2f})."
        else:
            return "This palindrome matches the average length exactly!"
