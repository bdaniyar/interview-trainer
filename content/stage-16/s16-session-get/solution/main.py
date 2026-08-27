def get_or_none(session, model, object_id):
    return session.get(model, object_id)
