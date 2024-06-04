# Wybrana reprezentacja: lista sąsiedztwa - najbardziej efektywna, graf spójny, nieskierowany

import argparse, random, copy, sys

sys.setrecursionlimit(1000000000)

class Node:
    def __init__(self, key):
        self.val = key
        self.neighbors = []

    def __repr__(self): 
        return f"Node({self.val})"

def create_hamilton_graph(nodes, saturation):
    cycle = [Node(i) for i in range(1, nodes + 1)]
    random.shuffle(cycle)
    
    for i in range(nodes):
        cycle[i-1].neighbors.append(cycle[i % nodes])
        cycle[i % nodes].neighbors.append(cycle[i-1])


    edges = nodes * (nodes - 1) // 2
    additional_edges = int(edges * saturation / 100) - nodes
    additional_edges_needed = additional_edges

    while additional_edges_needed > 0:
        NodeA, NodeB, NodeC = random.sample(cycle, 3)
        if NodeB not in NodeA.neighbors and NodeC not in NodeA.neighbors and NodeA not in NodeB.neighbors and NodeC not in NodeB.neighbors and NodeA not in NodeC.neighbors and NodeB not in NodeC.neighbors:
            NodeA.neighbors.append(NodeB)
            NodeB.neighbors.append(NodeA)
            NodeB.neighbors.append(NodeC)
            NodeC.neighbors.append(NodeB)
            NodeC.neighbors.append(NodeA)
            NodeA.neighbors.append(NodeC)
            additional_edges_needed -= 3

    return cycle

def print_graph(graph):
    for node in sorted(graph, key=lambda node: node.val):
        print(f"Wierzchołek {node.val}: {[neighbor.val for neighbor in node.neighbors]}")

def help():
    print("Dostępne komendy:")
    print("  print - wydrukuj graf")
    print("  help - wyświetl dostępne komendy")
    print("  exit - zakończ program")

def remove_edge(graph, vNode, uNode):
    for node in graph:
        if node.val == vNode.val and uNode in node.neighbors:
            node.neighbors.remove(uNode)
        if node.val == uNode.val and vNode in node.neighbors:
            node.neighbors.remove(vNode)

def DFS_Euler_iterative(start_node, graph):
    eulerCycleResult = []
    visited_edges = set()
    stack = [start_node]

    while stack:
        vNode = stack[-1]
        unvisited = None
        for uNode in vNode.neighbors:
            if (vNode, uNode) not in visited_edges:
                unvisited = uNode
                break

        if unvisited is None:
            eulerCycleResult.append(stack.pop().val)
        else:
            visited_edges.add((vNode, unvisited))
            visited_edges.add((unvisited, vNode))
            remove_edge(graph, vNode, unvisited)
            stack.append(unvisited)

    eulerCycleResult.reverse()
    return eulerCycleResult

def find_euler_cycle(graph):
    return DFS_Euler_iterative(graph[0], graph)

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument("--hamilton", action='store_true') 
    args = parser.parse_args()

    if args.hamilton:
        while True:
            nodes = int(input("nodes> "))
            if nodes % 2 == 0:
                break
            else:
                print("Liczba wierzchołków musi być parzysta, aby każdy wierzchołek był parzystego stopnia. Proszę wprowadzić parzystą liczbę.")
        while True:
            saturation = int(input("saturation> "))
            if saturation in [30, 70]:
                break
            else:
                print("Nieprawidłowe nasycenie. Proszę wprowadzić 30 lub 70.")
        Graph = create_hamilton_graph(nodes, saturation)

        while True:
            print("> ", end="")
            action = input().strip()
            if action.lower() == "print":
                print_graph(Graph)
            elif action.lower() == "help":
                help()
            elif action.lower() == "exit":
                break
            elif action.lower() == "euler":
                Graph_tmp = copy.deepcopy(Graph)
                euler_cycle = find_euler_cycle(Graph_tmp)
                if euler_cycle:
                        print(" -> ".join(map(str, euler_cycle)))
                else:
                    print("Graf nie posiada cyklu Eulera.")
            else:
                print("Nieznana komenda. Dostępne komendy to: print, help, exit.")

if __name__ == "__main__":
    main()
