def encrypt_affine(plaintext: str, a: int, b: int) -> str:
    """
    >>> encrypt_affine("ABC", 5, 8)
    'INS'
    >>> encrypt_affine("python", 7, 2)
    'dofzwp'
    >>> encrypt_affine("Affine Cipher!", 5, 8)
    'Ihhwvc Swfrcp!'

    """
    ciphertext = ""
    for ch in plaintext:
        if "A" <= ch <= "Z":
            x = ord(ch) - ord("A")
            y = (a * x + b) % 26
            ciphertext += chr(y + ord("A"))
        elif "a" <= ch <= "z":
            x = ord(ch) - ord("a")
            y = (a * x + b) % 26
            ciphertext += chr(y + ord("a"))
        else:
            ciphertext += ch
    return ciphertext
