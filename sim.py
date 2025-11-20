#!/usr/bin/env python3
"""
Fire Evacuation Simulation Visualizer
Python version of sim.c
"""

import sys
import time
import os
import fcntl
import hashlib

# ANSI Color definitions (using 256-color palette)
WALL_COLOR = 0
EMPTY_COLOR = 231
PERSON_COLOR = 136
FIRE_COLOR = 9
EXIT_COLOR = 34
PATH_COLOR = 1
OBJECT_COLOR = 19
STAIR_COLOR = 129
DOOR_COLOR = 239
FIRE_DOOR_COLOR = 51

# Number of base colors (non-smoke)
NUM_COLOURS = 10
COLOURS = [
    EMPTY_COLOR,      # 0: Empty
    WALL_COLOR,       # 1: Wall
    PERSON_COLOR,     # 2: Person
    FIRE_COLOR,       # 3: Fire
    EXIT_COLOR,       # 4: Exit
    PATH_COLOR,       # 5: Path
    OBJECT_COLOR,     # 6: Object
    STAIR_COLOR,      # 7: Stair
    DOOR_COLOR,       # 8: Door
    FIRE_DOOR_COLOR   # 9: Fire Door
]

# Map size
SIZE_X = 0
SIZE_Y = 0

# Map data
map_data = None
floors = ""


def smoke_color(smoke_index):
    """Calculate smoke color based on smoke intensity (0-12), gray to light gray"""
    # Use ANSI 256-color grayscale from 242 (gray) to 255 (very light gray)
    # Good starting darkness with lighter end for better visibility gradient
    index = min(smoke_index, 13)
    gray = 243
    light_gray = 255
    return gray + int((light_gray - gray) * (index / 13))


def hash_file(filename):
    """Hash file contents using SHA256"""
    try:
        with open(filename, 'rb') as fp:
            # Lock file for shared reading
            fcntl.flock(fp.fileno(), fcntl.LOCK_SH)
            
            # Read and hash file contents
            file_hash = hashlib.sha256(fp.read()).hexdigest()
            
            # Unlock file
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            
            return file_hash
    except FileNotFoundError:
        return 0


def print_maze():
    """Print the maze with ANSI color codes"""
    global map_data, floors, SIZE_X, SIZE_Y
    
    # Clear screen and build output
    output = ["\033c", floors, "\n"]
    
    for i in range(SIZE_Y):
        for j in range(SIZE_X):
            cell_value = map_data[i][j]
            
            if cell_value < NUM_COLOURS:
                # Base colors
                color = COLOURS[cell_value]
                output.append(f"\033[48;5;{color}m  \033[0m")
            elif cell_value < 14 + NUM_COLOURS:
                # Smoke colors (10-23)
                smoke_idx = cell_value - NUM_COLOURS
                color = smoke_color(smoke_idx)
                output.append(f"\033[48;5;{color}m  \033[0m")
            else:
                # Path color for other values
                output.append(f"\033[48;5;{PATH_COLOR}m  \033[0m")
        
        output.append("\n")
    
    output.append("\n")
    print(''.join(output), end='', flush=True)


def update_map(filename):
    """Read and update the map from file"""
    global map_data, floors, SIZE_X, SIZE_Y
    
    try:
        # Open with exclusive lock
        with open(filename, 'r+') as fp:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
        
        # Reopen for reading with exclusive lock
        with open(filename, 'r') as fp:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            
            # Read dimensions
            first_line = fp.readline().strip()
            tmp_x, tmp_y = map(int, first_line.split())
            
            # Sanity check
            if tmp_x > 10000 or tmp_y > 10000:
                fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
                return
            
            # Resize map if necessary
            if tmp_x != SIZE_X or tmp_y != SIZE_Y or map_data is None:
                if map_data is None:
                    print(f"Initializing map: {tmp_x} x {tmp_y}")
                
                SIZE_X = tmp_x
                SIZE_Y = tmp_y
                map_data = [[0 for _ in range(SIZE_X)] for _ in range(SIZE_Y)]
            
            # Read floor names/labels
            floor_line = fp.readline().rstrip('\n')
            floors = floor_line[:SIZE_X - 1] if len(floor_line) >= SIZE_X - 1 else floor_line
            
            # Read map data
            hex_chars = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, 
                        '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12}
            
            i = 0
            j = 0
            
            while True:
                char = fp.read(1)
                if not char:
                    break
                
                if j >= SIZE_X:
                    # Skip to next line
                    while char != '\n' and char != '':
                        char = fp.read(1)
                        if not char:
                            break
                    i += 1
                    j = 0
                    continue
                
                if i >= SIZE_Y:
                    break
                
                # Parse character
                if char == ' ':
                    map_data[i][j] = 0
                    j += 1
                elif char == '#' or char == '|':
                    map_data[i][j] = 1
                    j += 1
                elif char == 'P':
                    map_data[i][j] = 2
                    j += 1
                elif char == 'F':
                    map_data[i][j] = 3
                    j += 1
                elif char == 'E':
                    map_data[i][j] = 4
                    j += 1
                elif char == '+':
                    map_data[i][j] = 5
                    j += 1
                elif char == 'O':
                    map_data[i][j] = 6
                    j += 1
                elif char == 'S':
                    map_data[i][j] = 7
                    j += 1
                elif char == 'd':
                    map_data[i][j] = 8
                    j += 1
                elif char == 'D':
                    map_data[i][j] = 9
                    j += 1
                elif char == '\n':
                    i += 1
                    j = 0
                elif char in hex_chars:
                    map_data[i][j] = hex_chars[char] + NUM_COLOURS
                    j += 1
            
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
    
    except Exception as e:
        print(f"Error reading file: {e}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python sim.py <map_file>")
        return 1
    
    filename = sys.argv[1]
    
    # Initial file lock check
    try:
        with open(filename, 'r') as fp:
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            time.sleep(1)
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return 1
    
    prev_hash = 0
    
    while True:
        try:
            current_hash = hash_file(filename)
            
            if current_hash != prev_hash:
                update_map(filename)
                print_maze()
                prev_hash = current_hash
            
            time.sleep(0.0001)  # 100 microseconds
        
        except KeyboardInterrupt:
            print("\n\nSimulation stopped by user")
            break
        except Exception as e:
            print(f"\nError in main loop: {e}")
            time.sleep(0.1)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

