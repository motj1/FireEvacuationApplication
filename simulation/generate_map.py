import argparse
import random
import sys
import os

def generate_map(seed, floors, width, height, output_file, num_people=None, num_fire_spots=None):
    random.seed(seed)
    
    # Validate dimensions
    if width < 4 or height < 4:
        print("Error: Width and height must be at least 4.")
        return

    # Stair shafts: vertical columns that have stairs
    # Realistic number of staircases based on building size
    area = width * height
    if area < 400:  # Small building (< 20x20)
        num_shafts = random.randint(1, 2)
    elif area < 1000:  # Medium building (< ~30x30)
        num_shafts = random.randint(2, 3)
    elif area < 2000:  # Large building (< ~45x45)
        num_shafts = random.randint(2, 4)
    else:  # Very large building
        num_shafts = random.randint(3, 5)
    
    shafts = []
    attempts = 0
    while len(shafts) < num_shafts and attempts < num_shafts * 10:
        # Keep shafts inside, not on border
        r = random.randint(1, height - 2)
        c = random.randint(1, width - 2)
        if (r, c) not in shafts:
            shafts.append((r, c))
        attempts += 1
            
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
                    
                    stair_mappings.append(f"{f_down} {r_down} {c_down} {f_up} {r_up} {c_up}")
                    current_floor_stairs.append((r, c))

            # Write num stairs
            f.write(f"{len(stair_mappings)}\n")
            # Write mappings
            if stair_mappings:
                f.write("\n".join(stair_mappings) + "\n")
            else:
                # f.write("\n") # Empty line if no stairs
                pass

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
            
            # Generate Rooms with walls and doorways
            def create_rooms(grid, width, height, current_floor_stairs):
                """Create simple rectangular/square rooms with spacing to avoid clumping"""
                rooms = []
                
                # Fewer, larger rooms based on floor size
                num_rooms = random.randint(1, max(1, (width * height) // 120))
                
                def check_room_spacing(room_r, room_c, room_height, room_width, existing_rooms, min_spacing=3):
                    """Check if room has enough spacing from existing rooms"""
                    for (er, ec, eh, ew) in existing_rooms:
                        # Check if rooms are too close
                        if not (room_r + room_height + min_spacing < er or 
                                room_r > er + eh + min_spacing or
                                room_c + room_width + min_spacing < ec or
                                room_c > ec + ew + min_spacing):
                            return False
                    return True
                
                # Try to place rectangular rooms with spacing
                attempts = 0
                max_attempts = num_rooms * 10
                
                while len(rooms) < num_rooms and attempts < max_attempts:
                    attempts += 1
                    
                    # Larger room sizes (min 5x5, max 1/2 of floor dimension)
                    room_width = random.randint(6, max(6, width // 4))
                    room_height = random.randint(6, max(6, height // 4))
                    
                    # Random position (ensure it's inside boundaries)
                    room_r = random.randint(2, max(2, height - room_height - 2))
                    room_c = random.randint(2, max(2, width - room_width - 2))
                    
                    # Check if room overlaps with stairs
                    overlaps_stairs = False
                    for (sr, sc) in current_floor_stairs:
                        if room_r <= sr < room_r + room_height and room_c <= sc < room_c + room_width:
                            overlaps_stairs = True
                            break
                    
                    # Check spacing from other rooms
                    if not overlaps_stairs and check_room_spacing(room_r, room_c, room_height, room_width, rooms):
                        rooms.append((room_r, room_c, room_height, room_width))
                
                # Draw rooms with closed walls
                for (room_r, room_c, room_height, room_width) in rooms:
                    # Draw all walls (fully closed room)
                    for r in range(room_r, room_r + room_height):
                        for c in range(room_c, room_c + room_width):
                            # Draw perimeter walls only
                            if r == room_r or r == room_r + room_height - 1 or c == room_c or c == room_c + room_width - 1:
                                if grid[r][c] == ' ':
                                    grid[r][c] = '#'
                    
                    # Add 1-2 doors per room
                    num_doors = random.randint(1, 2)
                    for _ in range(num_doors):
                        side = random.choice(['top', 'bottom', 'left', 'right'])
                        if side == 'top' and room_c + 1 < room_c + room_width - 1:
                            door_c = random.randint(room_c + 1, room_c + room_width - 2)
                            grid[room_r][door_c] = ' '
                        elif side == 'bottom' and room_c + 1 < room_c + room_width - 1:
                            door_c = random.randint(room_c + 1, room_c + room_width - 2)
                            grid[room_r + room_height - 1][door_c] = ' '
                        elif side == 'left' and room_r + 1 < room_r + room_height - 1:
                            door_r = random.randint(room_r + 1, room_r + room_height - 2)
                            grid[door_r][room_c] = ' '
                        elif side == 'right' and room_r + 1 < room_r + room_height - 1:
                            door_r = random.randint(room_r + 1, room_r + room_height - 2)
                            grid[door_r][room_c + room_width - 1] = ' '
                
                return rooms
            
            rooms = create_rooms(grid, width, height, current_floor_stairs)
            
            # Place Furniture (chairs, tables, obstacles) inside rooms and hallways
            def place_furniture(grid, rooms, width, height):
                """Place minimal furniture and obstacles inside rooms"""
                # Place furniture inside rooms only (minimal)
                for (room_r, room_c, room_height, room_width) in rooms:
                    # Very few obstructions (0-2 per room)
                    num_furniture = random.randint(0, 2)
                    placed = 0
                    attempts = 0
                    
                    while placed < num_furniture and attempts < 20:
                        # Place inside the room (not on walls)
                        r = random.randint(room_r + 1, room_r + room_height - 2)
                        c = random.randint(room_c + 1, room_c + room_width - 2)
                        if grid[r][c] == ' ':
                            grid[r][c] = 'O'  # O for obstacles (chairs, tables, etc.)
                            placed += 1
                        attempts += 1
                
                # Almost no obstacles in hallways (keep hallways clear)
                hallway_obstacles = random.randint(0, max(0, width * height // 200))
                placed = 0
                attempts = 0
                while placed < hallway_obstacles and attempts < 30:
                    r = random.randint(1, height - 2)
                    c = random.randint(1, width - 2)
                    if grid[r][c] == ' ':
                        grid[r][c] = 'O'
                        placed += 1
                    attempts += 1
            
            place_furniture(grid, rooms, width, height)
                        
            # Place People (P) - prioritize spawning inside rooms
            def place_people(grid, rooms, width, height, total_people):
                """Place people inside rooms and some in hallways"""
                placed = 0
                
                # First, try to place people inside rooms
                for (room_r, room_c, room_height, room_width) in rooms:
                    if placed >= total_people:
                        break
                    
                    # Place some people in each room
                    people_in_room = random.randint(1, min(3, total_people - placed))
                    room_placed = 0
                    attempts = 0
                    
                    while room_placed < people_in_room and attempts < 30:
                        r = random.randint(room_r + 1, room_r + room_height - 2)
                        c = random.randint(room_c + 1, room_c + room_width - 2)
                        if grid[r][c] == ' ':
                            grid[r][c] = 'P'
                            room_placed += 1
                            placed += 1
                        attempts += 1
                
                # If we still need more people, place them anywhere in hallways
                attempts = 0
                while placed < total_people and attempts < 100:
                    r = random.randint(1, height - 2)
                    c = random.randint(1, width - 2)
                    if grid[r][c] == ' ':
                        grid[r][c] = 'P'
                        placed += 1
                    attempts += 1

            # Determine number of people for this floor
            if num_people is None:
                people_count = random.randint(1, max(1, width * height // 10))
            else:
                people_count = num_people
            
            place_people(grid, rooms, width, height, people_count)

            # Place Fire (F) - spread it around in multiple locations
            def spread_fire(grid, width, height, fire_sources):
                """Place fire in multiple locations and spread it"""
                fire_locations = []
                
                for _ in range(fire_sources):
                    attempts = 0
                    while attempts < 50:
                        r = random.randint(1, height - 2)
                        c = random.randint(1, width - 2)
                        if grid[r][c] == ' ':
                            grid[r][c] = 'F'
                            fire_locations.append((r, c))
                            break
                        attempts += 1
                
                # Spread fire to adjacent spaces (simulate initial spread - less aggressive)
                for (fr, fc) in fire_locations:
                    # Fire spread to nearby spaces with lower probability
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for dr, dc in directions:
                        if random.random() < 0.2:  # 20% chance to spread (reduced)
                            nr, nc = fr + dr, fc + dc
                            if 0 < nr < height - 1 and 0 < nc < width - 1:
                                if grid[nr][nc] == ' ':
                                    grid[nr][nc] = 'F'
            
            # Determine number of fire spots for this floor
            if num_fire_spots is not None and num_fire_spots > 0:
                spread_fire(grid, width, height, num_fire_spots)
            elif random.random() < 0.4:
                # Default: random fire with 40% chance (less fire)
                fire_sources = random.randint(1, 2)
                spread_fire(grid, width, height, fire_sources)

            # Write Grid
            for row in grid:
                f.write("".join(row) + "\n")
                
            f.write("\n")

    print(f"Map generated: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a seed-based map for Fire Evacuation Simulator",
        epilog="Example: python generate_map.py --seed 42 --floors 2 --width 10 --height 10 --people 5 --fire 2 --output maps/generated_map.txt"
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--floors", type=int, default=2, help="Number of floors")
    parser.add_argument("--width", type=int, default=10, help="Width of each floor")
    parser.add_argument("--height", type=int, default=10, help="Height of each floor")
    parser.add_argument("--people", type=int, default=None, help="Number of people per floor (default: random)")
    parser.add_argument("--fire", type=int, default=None, help="Number of fire spots per floor (default: random)")
    parser.add_argument("--output", type=str, default="maps/generated_map.txt", help="Output file path")
    
    args = parser.parse_args()
    
    generate_map(args.seed, args.floors, args.width, args.height, args.output, args.people, args.fire)

