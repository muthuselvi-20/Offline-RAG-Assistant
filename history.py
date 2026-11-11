import json
import uuid

from pathlib import Path
from datetime import datetime


HISTORY_DIR = Path("chat_history")

HISTORY_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def create_session():

    session_id = str(uuid.uuid4())

    history_file = (
        HISTORY_DIR / f"{session_id}.json"
    )

    history_file.write_text(
        json.dumps([]),
        encoding="utf-8"
    )

    return session_id


def save_message(
    session_id,
    role,
    content
):

    history_file = (
        HISTORY_DIR / f"{session_id}.json"
    )

    if history_file.exists():

        history = json.loads(
            history_file.read_text(
                encoding="utf-8"
            )
        )

    else:

        history = []

    history.append({

        "role": role,

        "content": content,

        "timestamp": datetime.now().isoformat()

    })

    history_file.write_text(

        json.dumps(
            history,
            indent=4,
            ensure_ascii=False
        ),

        encoding="utf-8"

    )


def get_history(session_id):

    history_file = (
        HISTORY_DIR / f"{session_id}.json"
    )

    if not history_file.exists():

        return []

    return json.loads(
        history_file.read_text(
            encoding="utf-8"
        )
    )


def clear_history(session_id):

    history_file = (
        HISTORY_DIR / f"{session_id}.json"
    )

    if history_file.exists():

        history_file.unlink()