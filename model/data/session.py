from typing import Optional


class Session:
    def __init__(
        self,
        session_id: str,
        user: str,
        seat: Optional[str],
        state: str,
        tty: Optional[str],
        class_type: str,
        remote: bool,
        active: bool
    ):
        self.session_id = session_id  # e.g., "3"
        self.user = user  # e.g., "rodrick"
        self.seat = seat  # e.g., "seat0" or None
        self.state = state  # e.g., "active", "online", "closing"
        self.tty = tty  # e.g., "tty2", "pts/0", or None
        self.class_type = class_type  # e.g., "user", "greeter", "background", "manager"
        self.remote = remote  # True if remote session
        self.active = active  # True if currently in use

    def is_graphical(self) -> bool:
        """Determine if session is likely GUI based."""
        return self.tty is not None and self.tty.startswith("tty")

