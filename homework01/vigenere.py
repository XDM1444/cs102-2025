def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    >>> encrypt_vigenere("Python 3.6!", "Key")
    'Zcxiqb 3.6!'
    >>> encrypt_vigenere("introduction to python", "lsci")
    'tfvzzvwkeaqv lq aqvpzf'
    """
    if not keyword:
        return plaintext
    res = []
    n = len(keyword)
    k = 0
    for ch in plaintext:
        key_ch = keyword[k % n]
        shift = (ord(key_ch.lower()) - ord('a')) % 26
        if 'A' <= ch <= 'Z':
            res.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
        elif 'a' <= ch <= 'z':
            res.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
        else:
            res.append(ch)
        k += 1  # двигаем ключ НА КАЖДОМ символе
    return "".join(res)


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    >>> decrypt_vigenere("Zcxiqb 3.6!", "Key")
    'Python 3.6!'
    >>> decrypt_vigenere("tfvzzvwkeaqv lq aqvpzf", "lsci")
    'introduction to python'
    """
    if not keyword:
        return ciphertext
    res = []
    n = len(keyword)
    k = 0
    for ch in ciphertext:
        key_ch = keyword[k % n]
        shift = (ord(key_ch.lower()) - ord('a')) % 26
        if 'A' <= ch <= 'Z':
            res.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
        elif 'a' <= ch <= 'z':
            res.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
        else:
            res.append(ch)
        k += 1  # двигаем ключ НА КАЖДОМ символе
    return "".join(res)
