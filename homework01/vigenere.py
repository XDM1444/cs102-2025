def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    # PUT YOUR CODE HERE
    if not keyword:
        return plaintext
    ciphertext = ""
    key_index = 0
    n = len(keyword)
    for ch in plaintext:
        key_ch = keyword[key_index % n]
        shift = (ord(key_ch.lower()) - ord("a")) % 26
        if "A" <= ch <= "Z":
            ciphertext += chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
        elif "a" <= ch <= "z":
            ciphertext += chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
        else:
            ciphertext += ch
        key_index += 1
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    if not keyword:
        return ciphertext
    plaintext = ""
    key_index = 0
    n = len(keyword)
    for ch in ciphertext:
        key_ch = keyword[key_index % n]
        shift = (ord(key_ch.lower()) - ord("a")) % 26
        if "A" <= ch <= "Z":
            plaintext += chr((ord(ch) - ord("A") - shift) % 26 + ord("A"))
        elif "a" <= ch <= "z":
            plaintext += chr((ord(ch) - ord("a") - shift) % 26 + ord("a"))
        else:
            plaintext += ch
        key_index += 1
    return plaintext
