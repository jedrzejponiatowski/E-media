def save_public_key(public_key):
    e, n = public_key
    with open("public_key.rsa", "w") as file:
        file.write(f"{e},{n}")


def load_public_key():
    with open("public_key.rsa", "r") as file:
        data = file.read()
    e, n = data.split(",")
    return (int(e), int(n))


def save_private_key(private_key):
    d, n = private_key
    with open("private_key.rsa", "w") as file:
        file.write(f"{d},{n}")


def load_private_key():
    with open("private_key.rsa", "r") as file:
        data = file.read()
    d, n = data.split(",")
    return (int(d), int(n))
