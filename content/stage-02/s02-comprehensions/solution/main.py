def active_emails(users):
    return [
        user["email"].strip().lower()
        for user in users
        if user.get("active") and user.get("email", "").strip()
    ]
