def apply_caesar_shift(msg: str, shift: int):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    decrypted = ""
    for c in msg.lower():
        if c.lower().isalpha():
            i_enc = alphabet.find(c)
            i_dec = (i_enc + shift) % 26
            decrypted += alphabet[i_dec]
        else:
            decrypted += c
    return decrypted


def decrypt_caesar(message: str, shift: int = None) -> list[str]:
    results = []
    if shift is None:
        for i in range(26):
            msg_decrypted = apply_caesar_shift(msg=message, shift=i)
            results.append(msg_decrypted)
    else:
        results.append(apply_caesar_shift(msg=message, shift=shift))
    return results


if __name__ == "__main__":
    a = decrypt_caesar(message="lbh ner abg fnsr")
    b = decrypt_caesar(message="QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD")
    c = apply_caesar_shift("FUCK THE DUCK", 17)
    e = apply_caesar_shift("alpha beta gamma delta xylophone z", shift=6)
    f = apply_caesar_shift("grvng hkzg mgssg jkrzg deruvnutk f", shift=-6)
    print(f)