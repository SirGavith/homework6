# Algorithm Evaluation 

First we consider the three algorithms

## Dijkstra's
### Optimality:
- Always guarantees an optimal solution
### Efficiency:
- $O(E + V \log V)$ optimally, though mroe realistic implementations are $O(E \log V)$
- Relatively slow since it always checks all paths in all directions until finding the shortest to the destination
### Memory usage:
- Requires storing a priority queue of all adjacent nodes to the current search tree
### Suitability for dynamic changes:
- Requires a re-run after dynamic changes, especially if you want to guarantee the optimality of the solution

## Greedy BFS
### Optimality:
- Not guaranteed; traded at the interest of speed
### Efficiency:
- $O(E \log V)$
- Runs quickly since it only explores nodes that heuristally are closer to the destination
### Memory usage:
- Visits fewer nodes, so has less information to store
### Suitability for dynamic changes:
- Good for a quick non-optimal route

## A*
### Optimality:
- Can be optimal if the heuristic function is well-made
### Efficiency:
- $O((E + V) \log V)$
- Runs fast thatnks the heuristic function
### Memory usage:
- Similar to Dijkstra, but should be a little smaller becuase it visits fewer nodes
### Suitability for dynamic changes:
- Good, and we can also change the heuristic function to find diffferent types of routes

# Our choice
It's clear that for this application A* is the best choice. In practice, it runs fast, gives nearly-optimal roues, and is suitable for change. In many scenarios, A* is the best-of-both-worlds of GBFS and Dijkstra's. While it's memory usage could be slightly more, machines these days are not memory constrained, especially since our graph is likely to be very small. In reality, for asuch a small graph, any of these algorithms would probably work fine (the network would still likely be the bottleneck) but those AWS bills don't go anywhere, so we optimize anyway.


# Implementation Experimentation 
First I construct a test graph. I tried some simple graphs with like 8, then 20 nodes, but the runtime of the algorithms was still 0. So im an attempt to create a harder test-case, I created the graph you find in `output.txt`. It's a grid-like graph where I start with a 100x100 grid, and randomally generate 30% barriers. A `.` represents a node, and a `B` is a barrier. `S` is the start, and `G` is the end; in order to make the solution interesting (not just a length 200 snaking across the grid), I let `S = (20,20)` and `G=(80,80)` (I left some comments to help you find those), and distribute the barriers normally, so that the shortest path skirts around the large mass in the middle. It's taken this away from the theme park example, but that's because that example is so trivial that the algorithm choice doesn't matter, so in the interest of knowledge itself we continue. I couldn't think of a realistic example that would take any real compute.
I use the manhattan distance as the heuristic.

```
Dijkstra: Shortest Path = 150, Visited 6191 nodes, Time Taken = 13.020515441894531 ms
GBFS: Shortest Path = 176, Visited 303 nodes, Time Taken = 1.0094642639160156 ms
A*: Shortest Path = 150, Visited 2903 nodes, Time Taken = 11.107206344604492 ms
```

Next we analyze the results and make some observations: 

- GBFS is way faster, on the order of 10x faster. And that makes sense, since it only visits 10% of the nodes of A* (300 vs 3000), and just 5% of Dijkstra's 6000.
- We can see directly how A* improves on Dijkstra; it only looks at half of the nodes (Dijkstra visits ~6000 of the 7000 nodes). However, due to its increased overhead, it takes more than half the time, so it's not quite twice as fast.
- GBFS does not find the shortest path; it finds a path that's 20% longer. This is unacceptable for a routefinding application, so it's good we didn't choose that one. 

Therefore, upon reviewing this concrete data, I am happy standing behind my choice of A*.