import re

def is_password_strong(password):
    # Check length requirement
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False

    # Check for at least one digit
    if not re.search(r"\d", password):
        return False

    # Check for at least one special character (you can expand this set)
    if not re.search(r"[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]", password):
        return False

    # If all conditions are met, the password is considered strong
    return True
