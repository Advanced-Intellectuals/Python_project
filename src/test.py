from password_hasher import PasswordHasher


def main():
    hasher = PasswordHasher()

    print(hasher.hash('12345'))


if __name__ == "__main__":
    main()
