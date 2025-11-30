from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.routers import users, polls, votes

app = FastAPI(title="UVote Backend API")

# Include the routers for each service
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

app.include_router(users.router, prefix="/users", tags=["User Service"])
app.include_router(polls.router, prefix="/polls", tags=["Poll Service"], dependencies=[Depends(oauth2_scheme)])
app.include_router(votes.router, prefix="/votes", tags=["Vote Service"])

@app.get("/")
def read_root():
    return {"message": "API Gateway is running"}
