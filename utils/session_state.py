import json
import os

class SessionState:
    FILE_NAME = "session_state.json"

    @staticmethod
    def save(state):
        with open(SessionState.FILE_NAME, "w") as f:
            json.dump(state, f)

    @staticmethod
    def load():
        if os.path.exists(SessionState.FILE_NAME):
            with open(SessionState.FILE_NAME, "r") as f:
                return json.load(f)
        return {"last_save_path": None, "is_new_network": True}
