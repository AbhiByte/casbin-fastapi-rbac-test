from fastapi import FastAPI, Depends, HTTPException
import casbin

app = FastAPI()

# Initialize enforcer once at startup
enforcer = casbin.Enforcer("rbac_model.conf", "policy.csv")


def get_current_user():
    # Stub: in a real app you'd extract from token/session
    return "bob"


def casbin_authorize(obj: str, act: str):
    def dependency(user: str = Depends(get_current_user)):
        if not enforcer.enforce(user, obj, act):
            raise HTTPException(status_code=403, detail="Access denied")
    return dependency


@app.get("/read-data")
def read_data(dep=Depends(casbin_authorize("data1", "read"))):
    return {"data": "Here is your data"}

@app.post("/write-data")
def write_data(dep=Depends(casbin_authorize("data1", "write"))):
    return {"status": "Data written successfully"}
