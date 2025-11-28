from fastapi import Request
import secrets
import string

def generate_unique_url(db_session, model, length=8):
    """
    Generates a unique URL-friendly string.
    """
    alphabet = string.ascii_letters + string.digits
    while True:
        url = "".join(secrets.choice(alphabet) for _ in range(length))
        if not db_session.query(model).filter(model.url == url).first():
            return url

def get_poll_url(request: Request, poll_url: str) -> str:
    """
    Constructs the full poll URL.
    """
    return str(request.url_for("get_poll_by_url", poll_url=poll_url))
