import pyotp
import secrets
import string
import hashlib

def generate_random_secret_key(length=16):
    """
    Generate a random secret key containing alphabets.
    :param length: The length of the secret key (default is 16).
    :return: The generated random secret key as a string.
    """
    alphabet = string.ascii_letters  # Includes uppercase and lowercase letters
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key


def generate_hotp(secret_key, counter=0, digits=6):
    """
    Generate an HMAC-based OTP (HOTP) using pyotp.
    :param secret_key: The secret key for HOTP generation.
    :param counter: The counter value for HOTP (default is 0).
    :param digits: The number of digits in the OTP (default is 6).
    :return: The generated HOTP as a string.
    """
    hotp = pyotp.HOTP(secret_key, digits=digits)
    return hotp.at(counter)



def hash_otp(otp):
    """
    Hash the OTP using SHA-256.
    :param otp: The OTP to be hashed.
    :return: The hashed OTP as a string.
    """
    hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
    return hashed_otp

def verify_otp(entered_otp, stored_hashed_otp):
    """
    Verify if the entered OTP is correct.
    :param entered_otp: The OTP entered by the user.
    :param stored_hashed_otp: The hashed OTP stored in the database.
    :return: True if the OTP is correct, False otherwise.
    """
    hashed_entered_otp = hash_otp(entered_otp)
    return hashed_entered_otp == stored_hashed_otp

