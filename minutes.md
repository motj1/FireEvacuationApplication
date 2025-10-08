### Week 4 Wednesday

Agenda Items:

1. Setup github
- This was done and all members were added as collaborators

2. Graph representation
- Suggestions
    - Each floor has a 2D graph corresponding to it
    - compare tradeoffs between havignn exits/doorways as nodes vs rooms as nodes
    - Deduced rooms as nodes are better -> room data -> room capacity ->
    - Edgeweight function dependent on distance between rooms and congestion level (dependent on ppl in room -> and edge capacity)
       - Human 
    - Some kind of time information as well estimate exit time? minimum time before we have to leave
    - Simple is better right now -> considerations like human speed
    - Graph representation -> adjacency matrix -> argument against = space -> buildings are usually sparse graphs will littl connections between nodes on different floors
      - Argument for -> edge updates are faster
    - fire spread:
      - could either be fire edges vs human edges -> human edges are a subset of the fire edge graph -> fire can spread along human paths
      - ALSO could do a cell-based fire system where each vertex maps to multiple grid cells that store fire information
         - cellular automata
  Algorithm:
    - Multi source djikstra where single source represents outside 'node' and connects to all exit-adjacent notes within the building with an edge representing the exit status (congestion, availability, hazard?)
      - O(|V| + |E|)
  FACT:
    - number of rooms in burj khalifa is 1200 -> largest number of nodes?? -> largest buiding rooms every 7500 ish??
 
  Simulation tick cycle:
  - Code in python 
  - Existing 3d modeller? -> or just make any 2d representation -> wrap the simulation in some library to display the simulation state

  Simulation:
  - ticks, what does a tick entail? what CAN happen in each tick how far person move,
  - weights in graph -> how is congestion represented? Congestion not only between two nodes but also the nodes themselves (room congestion/exit point congestion)
     - stepping stone nodes
  - Come up with minimum room unweighted path algorithm (multi source)
  - Capacity and congestion -> + threshold capacity at which when number ppl is below, congestion is 0 -> i.e. max(n - tr, 0) where n is number ppl on an edge and tr is threshold
     - i.e. 20 person threshold, 30 ppl at point -> congestion = 10
     - i.e. 20 person threshold, 19 ppl at point -> congestion = 0 -> up to a certain point, we can keep adding ppl without affecting congestion
  - COngestion through the hallway 
4. Simulation representation
5. Generic pathfinding algorithm
6. 
