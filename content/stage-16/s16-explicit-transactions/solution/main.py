def transfer(session, source, target, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    with session.begin():
        if source.balance < amount:
            raise ValueError("insufficient funds")
        source.balance -= amount
        target.balance += amount
