import networkx as nx
import random
import os

def generate_random_graph(n):
    assert 8 <= n <= 75
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    max_possible_edges = n * (n - 1) // 2
    min_edges = max(0, max_possible_edges - 12)
    num_edges = random.randint(min_edges, max_possible_edges - 3)

    all_possible_edges = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)]
    selected_edges = random.sample(all_possible_edges, num_edges)

    G.add_edges_from(selected_edges)
    return G

def generate_graph_instances(num_instances, k, output_dir="./graphs"):
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    for i in range(29, 29+num_instances):
        n = random.randint(8, 15)
        G = generate_random_graph(n)

        filename = os.path.join(output_dir, f"graph_{i}.dzn")
        with open(filename, "w") as f:
            output = f"n={n};\nm={G.number_of_edges()};\nk={k};\ninitial_edges=[\n"
            for u, v in G.edges:
                output += f"({u}, {v}),\n"
            output += "];"
            f.write(output)

        print(f"Graph {i}: {n} nodes, {G.number_of_edges()} edges → saved to {filename}")


# Example usage
if __name__ == "__main__":
    num_instances = int(input("Enter number of graph instances to generate: "))
    k = int(input("K value:"))
    graphs = generate_graph_instances(num_instances, k)
