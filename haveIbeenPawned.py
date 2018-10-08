import pyHIBP

def is_breached(email):
    resp = pyHIBP.get_account_breaches(account=email, truncate_response=True)
    if resp:
        return True
    else:
        return False

    
# Required import if password check is implemented
# from pyHIBP import pwnedpasswords as pw

# Check a password to see if it has been disclosed in a public breach corpus
# Exists just in case we want to implement a password check of some kind
# resp = pw.is_password_breached(password="secret")
# if resp:
#    print("Password breached!")
#    print("This password was used " + str(resp) + " time(s) before.")

# Get breaches that affect a given account
