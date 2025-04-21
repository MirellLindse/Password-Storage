import string
import random


class PasswordGenerator:
    # Initialize the generator with default values for password length and requirements
    def __init__(self):
        self.length = 8  # Default password length
        self.requirements = {"uppercase": False, "lowercase": False, "digit": False, "special": False}  # Default requirements (no specific types of characters required)

    # Set password requirements and length
    def set_requirements(self, uppercase=False, lowercase=False, digit=False, special=False, length=8):
        # Update the requirements with user input
        self.requirements["uppercase"] = uppercase
        self.requirements["lowercase"] = lowercase
        self.requirements["digit"] = digit
        self.requirements["special"] = special
        self.length = length  # Set the desired length for the password

    # Method to generate the password
    def generate_password(self):
        character_set = ""  # Initialize an empty string to store the available characters

        # Add digits to the character set if required
        if self.requirements["digit"]:
            character_set += string.digits
        # Add uppercase letters to the character set if required
        if self.requirements["uppercase"]:
            character_set += string.ascii_uppercase
        # Add lowercase letters to the character set if required
        if self.requirements["lowercase"]:
            character_set += string.ascii_lowercase
        # Add special characters to the character set if required
        if self.requirements["special"]:
            character_set += string.punctuation

        # If no character set has been selected, return a warning message
        if not character_set:
            return "Select at least one option"

        # Generate a password by randomly selecting characters from the character set
        password = [random.choice(character_set) for _ in range(self.length)]

        # Check if the password meets the requirements for uppercase letters
        if self.requirements["uppercase"] and not any(c.isupper() for c in password):
            # If no uppercase letter is found, replace a random character with an uppercase letter
            password[random.randint(0, self.length - 1)] = random.choice(string.ascii_uppercase)

        # Check if the password meets the requirements for lowercase letters
        if self.requirements["lowercase"] and not any(c.islower() for c in password):
            # If no lowercase letter is found, replace a random character with a lowercase letter
            password[random.randint(0, self.length - 1)] = random.choice(string.ascii_lowercase)

        # Check if the password meets the requirements for digits
        if self.requirements["digit"] and not any(c.isdigit() for c in password):
            # If no digit is found, replace a random character with a digit
            password[random.randint(0, self.length - 1)] = random.choice(string.digits)

        # Check if the password meets the requirements for special characters
        if self.requirements["special"] and not any(c in string.punctuation for c in password):
            # If no special character is found, replace a random character with a special character
            password[random.randint(0, self.length - 1)] = random.choice(string.punctuation)

        # Join the list of characters into a string and return the generated password
        return "".join(password)
