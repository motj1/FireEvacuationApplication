import argparse
import random
import sys
import os

def generate_map(seed, floors, width, height, output_file):
    random.seed(seed)
    
    # Validate dimensions
    if width < 4 or height < 4:
        print("Error: Width and height must be at least 4.")
        return

    # Stair shafts: vertical columns that have stairs
    # Randomly place 1 to 3 shafts depending on size
    num_shafts = random.randint(1, max(1, width * height // 50))
    shafts = []
    for _ in range(num_shafts):
        # Keep shafts inside, not on border
        r = random.randint(1, height - 2)
        c = random.randint(1, width - 2)
        if (r, c) not in shafts:
            shafts.append((r, c))
            
    # Sort shafts by position (row then col) to match reading order
    shafts.sort()

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Error creating directory {output_dir}: {e}")
            return

    with open(output_file, 'w') as f:
        f.write(f"{floors}\n")
        
        for floor_idx in range(floors):
            # Write dimensions
            f.write(f"{height}\n{width}\n")
            
            # Determine stairs for this floor
            # A shaft exists on this floor if it connects to something?
            # We assume shafts go from floor 0 to floor floors-1
            # But for a specific floor, we only write mappings for S tiles present.
            
            current_floor_stairs = []
            stair_mappings = []
            
            # For each shaft, calculate mappings
            for (r, c) in shafts:
                # Down connection
                if floor_idx > 0:
                    f_down, r_down, c_down = floor_idx - 1, r, c
                else:
                    f_down, r_down, c_down = -1, -1, -1
                    
                # Up connection
                if floor_idx < floors - 1:
                    f_up, r_up, c_up = floor_idx + 1, r, c
                else:
                    f_up, r_up, c_up = -1, -1, -1
                
                # Add to mappings if it connects somewhere
                if f_down != -1 or f_up != -1:
                    stair_mappings.append(f"({f_down} {r_down} {c_down}) ({f_up} {r_up} {c_up})")
                    current_floor_stairs.append((r, c))

            # Write num stairs
            f.write(f"{len(stair_mappings)}\n")
            # Write mappings
            if stair_mappings:
                f.write(" ".join(stair_mappings) + "\n")
            else:
                f.write("\n") # Empty line if no stairs (though num_stairs is 0)

            # Generate Grid
            grid = [[' ' for _ in range(width)] for _ in range(height)]
            
            # Fill Borders
            for r in range(height):
                for c in range(width):
                    if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                        grid[r][c] = '#'
            
            # Place Exits on Floor 0
            if floor_idx == 0:
                # Place 1-2 exits on random border positions
                num_exits = random.randint(1, 2)
                for _ in range(num_exits):
                    side = random.choice(['top', 'bottom', 'left', 'right'])
                    if side == 'top':
                        grid[0][random.randint(1, width - 2)] = 'E'
                    elif side == 'bottom':
                        grid[height - 1][random.randint(1, width - 2)] = 'E'
                    elif side == 'left':
                        grid[random.randint(1, height - 2)][0] = 'E'
                    elif side == 'right':
                        grid[random.randint(1, height - 2)][width - 1] = 'E'

            # Place Stairs
            for (r, c) in current_floor_stairs:
                grid[r][c] = 'S'
            
            # Place Obstacles and Internal Walls
            # Avoid overwriting S, E
            for r in range(1, height - 1):
                for c in range(1, width - 1):
                    if grid[r][c] != ' ':
                        continue
                    
                    chance = random.random()
                    if chance < 0.1:
                        grid[r][c] = 'O' # Obstacle
                    elif chance < 0.2:
                        grid[r][c] = '#' # Internal Wall
                        
            # Place People (P)
            # Higher chance on upper floors? Uniform for now.
            num_people = random.randint(1, max(1, width * height // 10))
            placed_people = 0
            attempts = 0
            while placed_people < num_people and attempts < 100:
                r = random.randint(1, height - 2)
                c = random.randint(1, width - 2)
                if grid[r][c] == ' ':
                    grid[r][c] = 'P'
                    placed_people += 1
                attempts += 1

            # Place Fire (F)
            # Small chance of fire start
            if random.random() < 0.3:
                r = random.randint(1, height - 2)
                c = random.randint(1, width - 2)
                if grid[r][c] == ' ':
                    grid[r][c] = 'F'

            # Write Grid
            for row in grid:
                f.write("".join(row) + "\n")
                
            # Add newline separation if not last floor?
            # The format seems to just concatenate.
            # But usually there is a newline after the grid rows?
            # readFileForNumbers handles it.
            f.write("\n")

    print(f"Map generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a seed-based map for Fire Evacuation Simulator",
        epilog="Example: python generate_map.py --seed 42 --floors 2 --width 10 --height 10 --output maps/generated_map.txt"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--floors", type=int, default=2, help="Number of floors")
    parser.add_argument("--width", type=int, default=10, help="Width of each floor")
    parser.add_argument("--height", type=int, default=10, help="Height of each floor")
    parser.add_argument("--output", type=str, default="maps/generated_map.txt", help="Output file path")
    
    args = parser.parse_args()
    
    generate_map(args.seed, args.floors, args.width, args.height, args.output)

