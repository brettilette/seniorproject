import hashlib

import requests
import six

import pyHIBP

PWNED_PASSWORDS_API_BASE_URI = "https://api.pwnedpasswords.com/"
PWNED_PASSWORDS_API_ENDPOINT_RANGE_SEARCH = "range/"

RESPONSE_ENCODING = "utf-8-sig"


def is_password_breached(password=None, sha1_hash=None, first_5_hash_chars=None):
    """
    Execute a search for a password via the k-anonymity model, checking for hashes which match a specified
    prefix instead of supplying the full hash to the Pwned Passwords API.

    Uses the first five characters of a SHA-1 hash to provide a list of hash suffixes along with the
    number of times that hash appears in the data set. In doing so, the API is not provided the information
    required to reconstruct the password (e.g., by brute-forcing the hash).

    Either ```password``, `first_5_hash_chars``, or ``sha1_hash`` must be specified. Only one parameter should be provided.

    The precedence of parameters is as follows:
    1) password - Computes the remaining two parameters.
    2) sha1_hash - Computes the following parameter, and will determine if a match was found.
    3) first_5_hash_chars - Returns a list of partial hashes for the calling application to process.

    If ``password`` is provided,
    the password will be converted to a SHA-1 hash, then the first five characters checked against the API's returned
    information, much like as if a full `sha1_hash` were supplied.

    Suffix example: 0018A45C4D1DEF81644B54AB7F969B88D65:1

    :param password: The password to check. Will be converted to a SHA-1 string.
    :param first_5_hash_chars: The first five characters of a SHA-1 hash string.
    :param sha1_hash: A full SHA-1 hash.
    :return: If ``first_5_hash_chars`` is supplied, a [list] of hash suffixes. If ``password`` or ``sha1_hash`` is supplied,
    and the password was found in the corpus, an Integer representing the number of times the password is in
    the data set; if not found, Integer zero (0) is returned.
    """
    if not password and not first_5_hash_chars and not sha1_hash:
        raise AttributeError("One of password, first_5_hash_chars, or sha1_hash must be provided.")
    elif password is not None and not isinstance(password, six.string_types):
        raise AttributeError("password must be a string type.")
    elif sha1_hash is not None and not isinstance(sha1_hash, six.string_types):
        raise AttributeError("sha1_hash must be a string type.")
    elif first_5_hash_chars is not None and not isinstance(first_5_hash_chars, six.string_types):
        raise AttributeError("first_5_hash_chars must be a string type.")
    if first_5_hash_chars and len(first_5_hash_chars) != 5:
        raise AttributeError("first_5_hash_chars must be of length 5.")

    if password:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    if sha1_hash:
        sha1_hash = sha1_hash.upper()
        first_5_hash_chars = sha1_hash[0:5]

    uri = PWNED_PASSWORDS_API_BASE_URI + PWNED_PASSWORDS_API_ENDPOINT_RANGE_SEARCH + first_5_hash_chars

    resp = requests.get(url=uri, headers=pyHIBP.pyHIBP_HEADERS)

    # The server response will have a BOM if we don't do this.
    resp.encoding = RESPONSE_ENCODING

    if resp.status_code != 200:
        # The HTTP Status should always be 200 for this request
        raise RuntimeError("Response from the endpoint was not HTTP200; this should not happen. Code was: " + str(resp.status_code))
    elif not sha1_hash:
        # Return the list of hash suffixes.
        return resp.text.split()
    else:
        # Since the full SHA-1 hash was provided, check to see if it was in the resultant hash suffixes returned.
        response_lines = resp.text.split()

        for hash_suffix in response_lines:
            if sha1_hash[5:] in hash_suffix:
                # We found the full hash, so return
                return int(hash_suffix.split(':')[1])

        # If we get here, there was no match to the supplied SHA-1 hash; return zero.
        return 0
