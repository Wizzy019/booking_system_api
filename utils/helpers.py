from datetime import datetime

def build_avatar_filename(user_id: str):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    return f"users/{user_id}/avatar/{timestamp}.jpg"