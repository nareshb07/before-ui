import hashlib
import random
import string

def generate_checksum(data, merchant_key):
    params = {}
    for key, value in data.items():
        params[key] = str(value)
    params['MID'] = merchant_key

    # Create a string using all the parameters
    params_string = "&".join([f"{key}={value}" for key, value in params.items()])

    salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    final_string = f"{params_string}&salt={salt}"

    # Generate a checksum using the final string and your merchant key
    hash_object = hashlib.sha256(final_string.encode('utf-8'))
    checksum = hash_object.hexdigest()
    return checksum, salt
