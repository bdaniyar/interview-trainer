from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def require_admin(x_role: Annotated[str | None, Header()] = None):
    if x_role != "admin":
        raise HTTPException(403, "admin role required")
    return x_role

@app.get("/admin")
def admin(role: Annotated[str, Depends(require_admin)]):
    return {"role": role}
