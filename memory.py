# In-memory chat storage (can be replaced with DB later)

_conversations = {}

def add_message(user_id: str, role: str, content: str):
    if user_id not in _conversations:
        _conversations[user_id] = []

    _conversations[user_id].append({
        "role": role,
        "content": content
    })

    # Keep last 10 messages only (memory control)
    _conversations[user_id] = _conversations[user_id][-10:]


def get_conversation(user_id: str):
    return _conversations.get(user_id, [])
