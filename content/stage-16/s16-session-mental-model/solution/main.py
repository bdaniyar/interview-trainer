def load_twice(session, model, object_id):
    return session.get(model, object_id), session.get(model, object_id)
