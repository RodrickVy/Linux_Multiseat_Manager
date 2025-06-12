import subprocess
from typing import List
from domain.entities.session import Session


def systemd_get_sessions_by_seat(seat_id: str) -> List[Session]:
    output = subprocess.check_output(['loginctl', 'list-sessions'], text=True)
    sessions = []

    for line in output.strip().split('\n')[1:]:  # Skip header line
        parts = line.split()
        if len(parts) < 7:
            continue

        session_id, uid, user, seat, tty, class_type, state, remote = parts[:8]
        print("Seat Id: " + seat_id  +"   seat_session: "+ seat)
        if seat != seat_id:
            continue

        session = Session(
            session_id=session_id,
            user=user,
            seat=seat,
            tty=tty,
            class_type=class_type,
            state=state,
            remote=(remote.lower() == "yes"),
            active=(state.lower() == "active")
        )
        sessions.append(session)

    return sessions
