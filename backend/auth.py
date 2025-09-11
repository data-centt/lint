from firebase_admin import auth as fb_auth

def verify_id_token(authorisation_header: str | None) -> str | None:
    """
    Accepts an HTTP Authorization header like: 'Bearer <idToken>'
    Returns the Firebase UID if valid, otherwise None.
    """

    if not authorisation_header:
        return None
    parts = authorisation_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

