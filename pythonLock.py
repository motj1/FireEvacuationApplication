import fcntl
import os
import time

file_path = "altering.map"

map = [ ['#', '#', '#', '#'],
        ['#', 'P', ' ', '#'],
        ['#', ' ', ' ', 'E'],
        ['#', '#', '#', '#'], ]

while 1:
    with open(file_path, "r") as f:
        # Acquire an exclusive, blocking lock
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        time.sleep(0.5)
    with open(file_path, "w") as f:
        # Acquire an exclusive, blocking lock
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        
        # Perform operations on the file while holding the lock
        f.write(''.join(map[0]) + "\n")
        f.write(''.join(map[1]) + "\n")
        f.write(''.join(map[2]) + "\n")
        f.write(''.join(map[3]) + "\n")
    if map[1][2] == ' ':
        map[1][2] = '+'
    else:
        map[1][2] = ' '