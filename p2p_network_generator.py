import random
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Network:
    def __init__(self):
        self.num_peers = 0
        self.graph = {} # Adjacency list representation: {peer_id: set_of_connected_peers}

    def generate_network(self):
        while True:
            self.num_peers = random.randint(50, 100)
            self.graph = {i: set() for i in range(self.num_peers)}
            
            # Attempt to build connections satisfying degree constraints
            # This is a simplified approach, a more robust method would involve
            # iterative edge additions with checks.
            for i in range(self.num_peers):
                while len(self.graph[i]) < 3: # Ensure minimum degree
                    peer_to_connect = random.randint(0, self.num_peers - 1)
                    if peer_to_connect != i and \
                       len(self.graph[peer_to_connect]) < 6 and \
                       peer_to_connect not in self.graph[i]:
                        self.add_connection(i, peer_to_connect)
            
            # Now, attempt to add more connections to reach max degree
            for i in range(self.num_peers):
                while len(self.graph[i]) < random.randint(3, 6): # Try to reach a random degree within range
                    peer_to_connect = random.randint(0, self.num_peers - 1)
                    if peer_to_connect != i and \
                       len(self.graph[peer_to_connect]) < 6 and \
                       peer_to_connect not in self.graph[i]:
                        self.add_connection(i, peer_to_connect)

            if self.validate_network():
                print(f"Successfully generated a valid network with {self.num_peers} peers.")
                break
            else:
                print("Generated network is invalid. Regenerating...")

    def add_connection(self, peer1, peer2):
        self.graph[peer1].add(peer2)
        self.graph[peer2].add(peer1)

    def validate_network(self):
        # 1. Check Peer Degree
        for peer_id, connections in self.graph.items():
            degree = len(connections)
            if not (3 <= degree <= 6):
                print(f"Degree violation for peer {peer_id}: {degree}")
                return False

        # 2. Check Network Connectivity (using BFS)
        if not self.num_peers: # Handle empty graph case
            return True

        start_node = 0
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)

        while queue:
            current_node = queue.popleft()
            for neighbor in self.graph[current_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        if len(visited) != self.num_peers:
            print("Network is not connected.")
            return False

        return True

    def visualize_network(self, filename="network.png"):
        G = nx.Graph()
        for peer_id, connections in self.graph.items():
            G.add_node(peer_id)
            for connected_peer in connections:
                G.add_edge(peer_id, connected_peer)

        plt.figure(figsize=(10, 8))
        nx.draw_networkx(G, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray', font_size=8)
        plt.title("P2P Network Visualization")
        plt.axis('off') # Turn off the axis
        plt.savefig(filename)
        print(f"Network visualization saved as {filename}")

if __name__ == "__main__":
    print("Script execution started.") # Added for initial confirmation
    p2p_net = Network()
    try:
        print("Attempting to generate network...")
        p2p_net.generate_network()
        
        print("Network generation complete. Attempting to visualize...")
        p2p_net.visualize_network()
        print("Script finished successfully.") # Added for final confirmation
    except Exception as e:
        # This will catch any unexpected errors during the process
        print(f"An unexpected error occurred during execution: {e}")
        import traceback
        traceback.print_exc() # This will print the full error stack trace
