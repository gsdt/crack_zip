import zipfile
import sys
import threading

def try_to_extract(file, password):
    print("Password:", password, end="")
    try:
        file.extractall(pwd=bytes(password, 'utf-8'))
        return True # fine, extract successfully!
    except:
        return False # failed, wrong password?

def try_hard(min, max):

    file = zipfile.ZipFile("hello.zip")

    # try with password in rang [min .. max]
    for password in range(min, max+1):
        _pass = "{:06d}".format(password) # password must have 6 digits, ex: 423 -> 000423
        status = try_to_extract(file, str(_pass))
        if status == True:
            print(f" -> Found password! -> [{_pass}]")
            sys.exit() # exit program
        else:
            print(" -> Wrong password")
    

if __name__ == "__main__":
    try_hard(0, 999999)


