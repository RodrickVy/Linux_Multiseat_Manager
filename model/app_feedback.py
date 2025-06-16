class AppFeedback:
    VALID_TYPES = {"success", "warning", "error"}

    def __init__(self, message: str, code: int, function: str, feedback_type: str):
        if feedback_type not in self.VALID_TYPES:
            raise ValueError(f"feedback_type must be one of: {', '.join(self.VALID_TYPES)}")

        self.message = message
        self.code = code
        self.function = function
        self.feedback_type = feedback_type

    @classmethod
    def success(cls, message: str, code: int, function: str):
        return cls(message, code, function, "success")

    @classmethod
    def warning(cls, message: str, code: int, function: str):
        return cls(message, code, function, "warning")

    @classmethod
    def error(cls, message: str, code: int, function: str):
        return cls(message, code, function, "error")

    def __str__(self):
        return f"[{self.feedback_type.upper()}] {self.function} (code {self.code}): {self.message}"

    def to_dict(self):
        return {
            "type": self.feedback_type,
            "code": self.code,
            "function": self.function,
            "message": self.message,
        }
