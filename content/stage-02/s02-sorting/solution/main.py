def sort_events(events):
    return sorted(events, key=lambda event: event["created_at"], reverse=True)
