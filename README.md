```
███████╗██╗██████╗ ███████╗                                                                       
██╔════╝██║██╔══██╗██╔════╝                                                                       
█████╗  ██║██████╔╝█████╗                                                                         
██╔══╝  ██║██╔══██╗██╔══╝                                                                         
██║     ██║██║  ██║███████╗                                                                       
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝                                                                       
                                                                                                  
███████╗███╗   ███╗███████╗██████╗  ██████╗ ███████╗███╗   ██╗ ██████╗██╗███████╗███████╗         
██╔════╝████╗ ████║██╔════╝██╔══██╗██╔════╝ ██╔════╝████╗  ██║██╔════╝██║██╔════╝██╔════╝██╗      
█████╗  ██╔████╔██║█████╗  ██████╔╝██║  ███╗█████╗  ██╔██╗ ██║██║     ██║█████╗  ███████╗╚═╝      
██╔══╝  ██║╚██╔╝██║██╔══╝  ██╔══██╗██║   ██║██╔══╝  ██║╚██╗██║██║     ██║██╔══╝  ╚════██║██╗      
███████╗██║ ╚═╝ ██║███████╗██║  ██║╚██████╔╝███████╗██║ ╚████║╚██████╗██║███████╗███████║╚═╝      
╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝╚══════╝╚══════╝         
                                                                                                  
███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗    ██████╗ ███████╗███████╗██╗ ██████╗ ███╗   ██╗
██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝    ██╔══██╗██╔════╝██╔════╝██║██╔════╝ ████╗  ██║
█████╗  ███████╗██║     ███████║██████╔╝█████╗      ██║  ██║█████╗  ███████╗██║██║  ███╗██╔██╗ ██║
██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝      ██║  ██║██╔══╝  ╚════██║██║██║   ██║██║╚██╗██║
███████╗███████║╚██████╗██║  ██║██║     ███████╗    ██████╔╝███████╗███████║██║╚██████╔╝██║ ╚████║
╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝    ╚═════╝ ╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

A multi-story building fire evacuation simulator that models agent behavior, fire spread, and pathfinding algorithms in real-time.

## Overview

This project simulates emergency evacuation scenarios in multi-story buildings during a fire. It includes:
- **3D pathfinding**: Agents navigate through multi-floor buildings using BFS algorithms
- **Dynamic fire spread**: Fire propagates to adjacent tiles probabilistically
- **Real-time visualisation**: Color-coded terminal display showing the simulation state
- **Multi-story support**: Buildings with stairwells connecting floors

## Features

- Multi-floor building simulation with stairwell connections
- BFS-based pathfinding algorithm for agent evacuation
- Probabilistic fire spread mechanism
- Real-time visualisation using ANSI color codes
- Support for multiple map files and scenarios

## Project Structure

```
FireEvacuationApplication/
├── simulation/          # Python simulation code
│   ├── Agent.py        # Agent movement logic
│   ├── algorithm.py    # BFS pathfinding implementation
│   ├── Position.py     # Position and Position3D classes
│   ├── Tile.py         # Tile types and parsing
│   ├── simulation.py   # Main simulation loop
│   ├── txtConverters.py # Map file parsing
│   ├── map.txt         # Default map file
│   └── maps/           # Additional map files (map_1.txt - map_15.txt)
├── sim.c               # C visualisation program
├── sim                 # Compiled visualisation binary
├── pythonLock.py       # File locking utility for map updates
├── Standard.md         # Symbol definitions
└── minutes.md          # Project planning notes
```

## Map Symbols

According to `Standard.md`, the following symbols are used:

| Symbol | Description |
|--------|-------------|
| `#` | Wall |
| `P` | Person (Agent) |
| `F` | Fire |
| `O` | Obstruction |
| `E` | Exit |
| `+` | Path |
| `0-C` | Smoke (different levels) |
| `S` | Stairwell |
| ` ` | Empty/Void space |

## Requirements

- Python 3.x
- C compiler (gcc/clang) for visualisation
- Unix-like system (Linux/macOS) for file locking features

## Usage

### Running the Simulation

1. **Run the Python simulation :**
   ```bash
   cd simulation
   python3 simulation.py <map_file>
   ```

2. **View the visualisation (in a separate terminal):**
   ```bash
   ./sim simulation/map.txt
   ```

   The visualisation program reads the map file and displays it with color-coded tiles, updating in real-time as the simulation progresses.

### Simulation Output

The simulation prints:
- The current state of the building at each tick
- Total number of ticks to complete
- Number of people trapped
- Number of people who escaped

## Map File Format

Map files follow this format:
- First line: `<height> <width>` - dimensions of the map
- Subsequent lines: Character grid representing the building layout
- Multiple floors can be separated and will be processed as separate levels

## Development Notes

- The project uses file locking (`fcntl`) for synchronised map updates between Python and C processes
- The visualisation program (`sim.c`) uses ANSI escape codes for colored terminal output
- Maps are stored in the `simulation/maps/` directory

## Authors
- Angus Holliday
- Armaan Rai
- Jack Chamberlain
- Naga Maddali
- Tom Jackson


