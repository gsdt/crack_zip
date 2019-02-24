import zipfile
import sys
import threading
import curses

def try_to_extract(file, password):
    try:
        file.extractall(pwd=bytes(password, 'utf-8'))
        return True # fine, extract successfully!
    except:
        return False # failed, wrong password?

def try_hard(file, min, max):
    global found
    t_name = int(threading.current_thread().getName())
    # try with password in rang [min .. max]
    for password in range(min, max+1):
        if found:
            break
        _pass = "{:06d}".format(password) # password must have 6 digits, ex: 423 -> 000423
        status = try_to_extract(file, str(_pass))
        if status == True:
            found = True
            stdscr.addstr(t_name, 0, f"[Thread {t_name}] Password: {_pass} -> Found correct password.")
            break # exit program
        else:
            stdscr.addstr(t_name, 0, f"[Thread {t_name}] Password: {_pass} -> Faild password.")
        
        stdscr.refresh()
    

if __name__ == "__main__":
    # init data
    file = zipfile.ZipFile("hello.zip")
    thread_list = []
    min = 0
    found = False

    # create curses screen
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    # create 10 thread
    for index in range(10):
        thread_list.append(threading.Thread(
            target=try_hard, 
            name=str(index), 
            args=(file, min, min + 100000)
        ))
        min += 100000

    # start them
    for thread in thread_list:
        thread.start()

    # waiting for all thread finish their jobs.
    for thread in thread_list:
        thread.join()

    # exiting program
    file.close()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    stdscr.addstr(10, 0, "Press [enter] key to exit")
    stdscr.getkey()
    curses.endwin()



