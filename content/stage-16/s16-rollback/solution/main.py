def persist(session, entity):
    try:
        session.add(entity)
        session.commit()
        return entity
    except Exception:
        session.rollback()
        raise
