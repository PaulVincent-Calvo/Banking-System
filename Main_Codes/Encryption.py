class Cipher:
  alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

  def __init__(self, shift):
    self.shift = shift

  def encrypt(self, string):
    ciphertext = ""

    # Jumbles Placement of letters
    string = string[-1] + string[1:-1] + string[0]
    string = string[0:2] + string[-1] + string[3:-1] + string[2]

    # Shifts letters based on the parameter
    for char in string:
      if char in self.alphabet:
        index = self.alphabet.index(char)
        new_index = (index + self.shift) % 52
        new_char = self.alphabet[new_index]
        ciphertext += new_char
      else:
        ciphertext += char
    return ciphertext

  def decrypt(self, string):
    plaintext = ""
    for char in string:
      if char in self.alphabet:
        index = self.alphabet.index(char)
        new_index = (index - self.shift) % 52
        new_char = self.alphabet[new_index]
        plaintext += new_char
      else:
        plaintext += char
    plaintext = plaintext[0:2] + plaintext[-1] + plaintext[3:-1] + plaintext[2]
    plaintext = plaintext[-1] + plaintext[1:-1] + plaintext[0]
    return plaintext

# Parameter determines the amount the letter would shift
cipher = Cipher(30)

# Password should 4 characters in length, otherwise adjust jumble placement values on both encrypt and decrypt
password = "Hello, World!"

# Test Code
encrypted = cipher.encrypt(password)
decrypted = cipher.decrypt(encrypted)
print("Password:", password)
print("Encrypted:", encrypted)
print("Decrypted:", decrypted)