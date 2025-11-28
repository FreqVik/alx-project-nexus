from fastapi import FastAPI
from app.routers import users, polls, votes

app = FastAPI(title="API Gateway")

# Include the routers for each service
app.include_router(users.router, prefix="/users", tags=["User Service"])
app.include_router(polls.router, prefix="/polls", tags=["Poll Service"])
app.include_router(votes.router, prefix="/votes", tags=["Vote Service"])

@app.get("/")
def read_root():
    return {"message": "API Gateway is running"}
