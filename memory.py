<<<<<<< HEAD
# backend/memory.py

from collections import defaultdict

# Conversation memory
conversation_store = defaultdict(list)

# User profile memory
user_profile = defaultdict(dict)


def add_message(user_id, role, content):
    conversation_store[user_id].append({
        "role": role,
        "content": content
    })


def get_conversation(user_id):
    return conversation_store[user_id]


def set_user_language(user_id, language):
    user_profile[user_id]["language"] = language


def get_user_language(user_id):
    return user_profile[user_id].get("language")

_memory = {}

def get_conversation(user_id):
    return _memory.get(user_id, [])

def add_message(user_id, role, content):
    _memory.setdefault(user_id, []).append({
        "role": role,
        "content": content
    })
=======
# backend/memory.py

from collections import defaultdict

# Conversation memory
conversation_store = defaultdict(list)

# User profile memory
user_profile = defaultdict(dict)


def add_message(user_id, role, content):
    conversation_store[user_id].append({
        "role": role,
        "content": content
    })


def get_conversation(user_id):
    return conversation_store[user_id]


def set_user_language(user_id, language):
    user_profile[user_id]["language"] = language


def get_user_language(user_id):
    return user_profile[user_id].get("language")

_memory = {}

def get_conversation(user_id):
    return _memory.get(user_id, [])

def add_message(user_id, role, content):
    _memory.setdefault(user_id, []).append({
        "role": role,
        "content": content
    })
>>>>>>> c9f2407 (Fix project structure for Render deployment)
