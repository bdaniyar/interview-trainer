def add_and_flush(session, entity):
    session.add(entity)
    session.flush()
    return entity
