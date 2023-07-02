def check_nickname(nickname: str):
    if not nickname.isascii():
        return False, "Nickname must be ASCII!"
    elif not nickname:
        return False, "You must provide a nickname!"
    elif len(nickname.strip().split(" ")) > 1:
        return False, "Nickname must not contain spaces!"
    elif len(nickname) > 18:
        return False, "Nickname must be less than 18 characters!"

    return True, None