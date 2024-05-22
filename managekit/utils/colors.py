class Colors:
    BLUE = "\033[94m"
    END = "\033[0m"
    AMBER = "\033[38;5;214m"
    TEAL = "\033[38;5;30m"
    ORANGE = "\033[38;5;208m"
    EMERALD = "\033[38;5;48m"
    ZINC = "\033[38;5;243m"

    @staticmethod
    def blue(text):
        return f"{Colors.BLUE}{text}{Colors.END}"

    @staticmethod
    def amber(text):
        return f"{Colors.AMBER}{text}{Colors.END}"

    @staticmethod
    def teal(text):
        return f"{Colors.TEAL}{text}{Colors.END}"

    @staticmethod
    def orange(text):
        return f"{Colors.ORANGE}{text}{Colors.END}"

    @staticmethod
    def emerald(text):
        return f"{Colors.EMERALD}{text}{Colors.END}"

    @staticmethod
    def zinc(text):
        return f"{Colors.ZINC}{text}{Colors.END}"


# managekit/utils/colors.py
