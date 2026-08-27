def normalize_scopes(scopes):
    return frozenset(scope.strip().lower() for scope in scopes if scope.strip())
