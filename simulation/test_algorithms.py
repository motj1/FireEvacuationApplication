#!/usr/bin/env python3
"""
Algorithm Performance Testing Script
Tests all evacuation algorithms across different map sizes and configurations
"""

import sys
import os
import json
import time
from pathlib import Path
from tabulate import tabulate

# Import required modules (avoiding simulation.py's main execution)
from generate_map import generate_map
from algorithm import *
from Position import *
from txtConverters import *
from Agent import *
from Smoke import *
from fire import *
import random

# Test configurations
TEST_CONFIGS = [
    {"name": "Small", "floors": 1, "width": 15, "height": 15, "people": 5, "fire": 1},
    {"name": "Medium", "floors": 2, "width": 25, "height": 25, "people": 10, "fire": 2},
    {"name": "Large", "floors": 3, "width": 35, "height": 35, "people": 15, "fire": 3},
    {"name": "XLarge", "floors": 2, "width": 50, "height": 50, "people": 20, "fire": 3},
]

ALGORITHMS = ["bfs", "bfsPred", "bfsPredPess", "astar", "nextMove"]

def run_simulation(map_file, algo):
    """
    Run a single simulation and return statistics
    """
    # Load map
    m, dims, a = generateMultiStoryMapStairs(map_file)
    
    if len(a) == 0:
        return {
            "evacuated": 0,
            "trapped": 0,
            "total": 0,
            "survival_rate": 0,
            "ticks": 0,
            "total_wait": 0,
            "avg_wait": 0,
            "error": "No agents in map"
        }
    
    waitGraph = []
    for i in range(len(dims)):
        waitGraph.append([[0 for _ in range(dims[i][1])] for _ in range(dims[i][0])])
    
    tick = 0
    trapped = 0
    finished = [False for _ in range(len(a))]
    max_ticks = 1000  # Prevent infinite loops
    
    try:
        while tick < max_ticks:
            nextInstructions = []
            
            # Spread fire and smoke
            spreadFire(m, dims, 0.2)
            spreadSmoke(m, dims)
            
            # Prepare algorithm-specific data
            if algo == "nextMove":
                cell_details = calculate_dests(m, dims)
            elif algo == "bfsPred":
                depth_maps = getPredictiveMaps(m, dims, 3, 2)
            elif algo == "bfsPredPess":
                depth_maps = getPredictiveMaps(m, dims, 3, 5)
            
            # Calculate next move for each agent
            for i in range(len(a)):
                if finished[i] == True:
                    nextInstructions.append(Position3D(-1, -1, -1))
                    continue
                
                try:
                    if algo == "bfs":
                        nextInstruction = bfs3D(m, a[i], dims)
                    elif algo == "bfsPred":
                        nextInstruction = bfsPredictive(m, depth_maps, a[i], dims)
                    elif algo == "bfsPredPess":
                        nextInstruction = bfsPredictive(m, depth_maps, a[i], dims)
                    elif algo == "astar":
                        nextInstruction = astar(m, a[i], dims)
                    elif algo == "nextMove":
                        nextInstruction = nextmove(a[i], cell_details)

                    curTile = m[a[i].floor][a[i].row][a[i].col]
                    charMap = {"A":10, "B":11, "C":12, "D":13}
                    adjacencyCoords = [[0, 1], [1, 0], [0, -1], [-1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]

                    if curTile.kind[0:5] == "smoke":
                        curTileInty = int(curTile.kind[5]) if curTile.kind[5].isdigit() else charMap[curTile.kind[5]]

                        if random.randint(1, (curTileInty+2)//2) <= 1:
                            traversableCoords = []
                            for coords in adjacencyCoords:
                                adjacentTile = m[a[i].floor][a[i].row + coords[0]][a[i].col + coords[1]]
                                if adjacentTile.isTraversable():
                                    traversableCoords.append(Position3D(a[i].floor, a[i].row + coords[0], a[i].col + coords[1]))

                            if len(traversableCoords) != 0:
                                randCoord = traversableCoords[random.randint(1, len(traversableCoords))-1]
                                nextInstruction = Position3D(a[i].floor, randCoord.row, randCoord.col)
                            else:
                                nextInstruction = Position3D(-1, -1, -1)
                    
                    if nextInstruction.floor == -1:
                        trapped += 1
                        finished[i] = True
                        nextInstructions.append(Position3D(-1, -1, -1))
                    else:
                        nextInstructions.append(nextInstruction)
                except Exception as e:
                    # Agent trapped due to algorithm error
                    trapped += 1
                    finished[i] = True
                    nextInstructions.append(Position3D(-1, -1, -1))
            
            # Move agents
            for i in range(len(a)):
                if finished[i] == True:
                    continue
                
                moved, a[i] = moveAgent3D(m, a[i], nextInstructions[i])
                
                if moved == False and waitGraph[a[i].floor][a[i].row][a[i].col] < 9:
                    waitGraph[a[i].floor][a[i].row][a[i].col] += 1
            
            # Check for agents at exits
            for agent in reversed(a):
                if m[agent.floor][agent.row][agent.col].kind == "exit":
                    m[agent.floor][agent.row][agent.col].hasAgent = False
                    finished[a.index(agent)] = True
            
            # Check if all agents are done
            numAgentsFinished = sum(1 for f in finished if f)
            if len(a) == numAgentsFinished:
                break
            
            tick += 1
        
        # Calculate statistics
        evacuated = len(a) - trapped
        total_wait = getTotalWait(waitGraph, dims)
        avg_wait = total_wait / len(a) if len(a) > 0 else 0
        survival_rate = (evacuated / len(a)) * 100 if len(a) > 0 else 0
        
        return {
            "evacuated": evacuated,
            "trapped": trapped,
            "total": len(a),
            "survival_rate": survival_rate,
            "ticks": tick,
            "total_wait": total_wait,
            "avg_wait": avg_wait,
            "error": None if tick < max_ticks else "Timeout"
        }
    
    except Exception as e:
        return {
            "evacuated": 0,
            "trapped": len(a),
            "total": len(a),
            "survival_rate": 0,
            "ticks": tick,
            "total_wait": 0,
            "avg_wait": 0,
            "error": str(e)
        }

def run_tests(num_trials=5):
    results = []

    print("=" * 80)
    print("EVACUATION ALGORITHM PERFORMANCE TESTING")
    print("=" * 80)
    print()

    maps_dir = Path("test_maps")
    maps_dir.mkdir(exist_ok=True)

    test_num = 0
    total_tests = len(TEST_CONFIGS) * len(ALGORITHMS) * num_trials

    for config in TEST_CONFIGS:
        print(f"\n{'=' * 80}")
        print(f"Testing Configuration: {config['name']}")
        print(f"  Floors: {config['floors']}, Size: {config['width']}x{config['height']}")
        print(f"  People: {config['people']}, Fire Spots: {config['fire']}")
        print(f"{'=' * 80}\n")

        # ----------------------------------------------------
        # GENERATE ONE STABLE MAP PER CONFIGURATION
        # ----------------------------------------------------
        seed = hash(f"{config['name']}_fixed_seed") % (2**31)
        map_file = maps_dir / f"{config['name']}.txt"

        if not map_file.exists():
            generate_map(
                seed=seed,
                floors=config['floors'],
                width=config['width'],
                height=config['height'],
                output_file=str(map_file),
                num_people=config['people'],
                num_fire_spots=config['fire']
            )

        # ----------------------------------------------------
        # RUN ALL ALGORITHMS ON SAME MAP FOR num_trials TRIALS
        # ----------------------------------------------------
        for algo in ALGORITHMS:
            results_for_algo = []

            for trial in range(num_trials):

                test_num += 1
                print(f"  {algo.upper()} - Trial {trial + 1}/{num_trials} "
                      f"(Test {test_num}/{total_tests})...", end=" ")

                stats = run_simulation(str(map_file), algo)
                results_for_algo.append(stats)

                print(f"✓ (Survived: {stats['evacuated']}/{stats['total']}, "
                      f"Ticks: {stats['ticks']})")

            # ------------------------------------------------
            # AVERAGE RESULTS FOR THIS ALGO + CONFIG
            # ------------------------------------------------
            avg_stats = {
                "config": config['name'],
                "algorithm": algo,
                "avg_survival_rate": sum(r['survival_rate'] for r in results_for_algo) / num_trials,
                "avg_evacuated": sum(r['evacuated'] for r in results_for_algo) / num_trials,
                "avg_trapped": sum(r['trapped'] for r in results_for_algo) / num_trials,
                "avg_ticks": sum(r['ticks'] for r in results_for_algo) / num_trials,
                "avg_total_wait": sum(r['total_wait'] for r in results_for_algo) / num_trials,
                "avg_avg_wait": sum(r['avg_wait'] for r in results_for_algo) / num_trials,
                "trials": num_trials,
                "errors": sum(1 for r in results_for_algo if r['error'] is not None)
            }

            results.append(avg_stats)

        # ----------------------------------------------------
        # DELETE MAP AFTER ALL ALGOS & TRIALS COMPLETE
        # ----------------------------------------------------
        map_file.unlink()

    return results

def print_results(results):
    """
    Print comprehensive results comparison
    """
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80 + "\n")
    
    # Group results by configuration
    configs = sorted(set(r['config'] for r in results))
    
    for config in configs:
        config_results = [r for r in results if r['config'] == config]
        
        print(f"\n{config} Configuration")
        print("-" * 80)
        
        # Survival Rate Table
        table_data = []
        for r in config_results:
            table_data.append([
                r['algorithm'].upper(),
                f"{r['avg_survival_rate']:.1f}%",
                f"{r['avg_evacuated']:.1f}",
                f"{r['avg_trapped']:.1f}",
                f"{r['avg_ticks']:.1f}",
                f"{r['avg_avg_wait']:.2f}",
                r['errors']
            ])
        
        headers = ["Algorithm", "Survival %", "Avg Evacuated", "Avg Trapped", 
                   "Avg Ticks", "Avg Wait/Person", "Errors"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    # Overall Rankings
    print("\n" + "=" * 80)
    print("OVERALL ALGORITHM RANKINGS")
    print("=" * 80 + "\n")
    
    # Rank by survival rate
    algo_survival = {}
    algo_speed = {}
    algo_wait = {}
    
    for algo in ALGORITHMS:
        algo_results = [r for r in results if r['algorithm'] == algo]
        algo_survival[algo] = sum(r['avg_survival_rate'] for r in algo_results) / len(algo_results)
        algo_speed[algo] = sum(r['avg_ticks'] for r in algo_results) / len(algo_results)
        algo_wait[algo] = sum(r['avg_avg_wait'] for r in algo_results) / len(algo_results)
    
    # Survival Rate Ranking
    print("1. By Survival Rate (Higher is Better)")
    survival_ranking = sorted(algo_survival.items(), key=lambda x: x[1], reverse=True)
    ranking_data = []
    for i, (algo, rate) in enumerate(survival_ranking, 1):
        ranking_data.append([i, algo.upper(), f"{rate:.2f}%"])
    print(tabulate(ranking_data, headers=["Rank", "Algorithm", "Avg Survival Rate"], tablefmt="fancy_grid"))
    
    # Speed Ranking
    print("\n2. By Speed (Lower is Better)")
    speed_ranking = sorted(algo_speed.items(), key=lambda x: x[1])
    ranking_data = []
    for i, (algo, ticks) in enumerate(speed_ranking, 1):
        ranking_data.append([i, algo.upper(), f"{ticks:.2f}"])
    print(tabulate(ranking_data, headers=["Rank", "Algorithm", "Avg Ticks"], tablefmt="fancy_grid"))
    
    # Wait Time Ranking
    print("\n3. By Wait Time (Lower is Better)")
    wait_ranking = sorted(algo_wait.items(), key=lambda x: x[1])
    ranking_data = []
    for i, (algo, wait) in enumerate(wait_ranking, 1):
        ranking_data.append([i, algo.upper(), f"{wait:.2f}"])
    print(tabulate(ranking_data, headers=["Rank", "Algorithm", "Avg Wait/Person"], tablefmt="fancy_grid"))
    
    # Composite Score (weighted average)
    print("\n4. Composite Score (Weighted)")
    print("   Formula: (Survival% * 0.5) + ((100 - Normalized_Ticks) * 0.3) + ((100 - Normalized_Wait) * 0.2)")
    
    # Normalize metrics
    max_ticks = max(algo_speed.values())
    max_wait = max(algo_wait.values())
    
    composite_scores = {}
    for algo in ALGORITHMS:
        survival_score = algo_survival[algo]
        speed_score = 100 - (algo_speed[algo] / max_ticks * 100) if max_ticks > 0 else 0
        wait_score = 100 - (algo_wait[algo] / max_wait * 100) if max_wait > 0 else 0
        
        composite_scores[algo] = (survival_score * 0.5 + speed_score * 0.3 + wait_score * 0.2)
    
    composite_ranking = sorted(composite_scores.items(), key=lambda x: x[1], reverse=True)
    ranking_data = []
    for i, (algo, score) in enumerate(composite_ranking, 1):
        ranking_data.append([i, algo.upper(), f"{score:.2f}"])
    print(tabulate(ranking_data, headers=["Rank", "Algorithm", "Composite Score"], tablefmt="fancy_grid"))
    
    # Winner announcement
    print("\n" + "=" * 80)
    winner = composite_ranking[0][0]
    print(f"🏆 BEST OVERALL ALGORITHM: {winner.upper()} 🏆")
    print("=" * 80)
    
    return winner

def save_results(results, filename="algorithm_test_results.json"):
    """Save results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Results saved to {filename}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test evacuation algorithms")
    parser.add_argument("--trials", type=int, default=5, help="Number of trials per configuration (default: 5)")
    parser.add_argument("--output", type=str, default="algorithm_test_results.json", help="Output file for results")
    
    args = parser.parse_args()
    
    print(f"\nStarting algorithm performance tests with {args.trials} trials per configuration...")
    print(f"This will run {len(TEST_CONFIGS) * len(ALGORITHMS) * args.trials} total simulations.\n")
    
    start_time = time.time()
    results = run_tests(num_trials=args.trials)
    end_time = time.time()
    
    winner = print_results(results)
    save_results(results, args.output)
    
    print(f"\n✓ Testing completed in {end_time - start_time:.2f} seconds")
    print(f"✓ Best algorithm for survivability: {winner.upper()}\n")

