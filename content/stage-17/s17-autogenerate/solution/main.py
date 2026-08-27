def unsafe_operations(operations):
    markers = ("drop ", "delete ", "set not null", "nullable=false")
    return [operation for operation in operations if any(marker in operation.lower() for marker in markers)]
