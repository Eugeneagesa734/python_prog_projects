from collections import deque

class Solution:
    def getEvenOddCounts(self, adj):
        """
        For each node, calculate how many nodes are at even/odd distances.
        Uses the fact that in a tree, nodes form a bipartite graph based on distance parity.
        """
        n = len(adj)
        if n == 0:
            return []
        
        # First, partition all nodes into two groups based on distance parity from node 0
        color = [-1] * n
        queue = deque([0])
        color[0] = 0
        group0, group1 = [], []
        
        while queue:
            u = queue.popleft()
            if color[u] == 0:
                group0.append(u)
            else:
                group1.append(u)
                
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    queue.append(v)
        
        # Now for each node, count even/odd distances
        result = []
        for i in range(n):
            if color[i] == 0:
                # Nodes in same group are at even distance, opposite group at odd distance
                even_count = len(group0)
                odd_count = len(group1)
            else:
                # Nodes in same group are at even distance, opposite group at odd distance
                even_count = len(group1)
                odd_count = len(group0)
            result.append((even_count, odd_count))
        
        return result
    
    def maxTargetNodes(self, edges1, edges2):
        m = len(edges1) + 1
        n = len(edges2) + 1
        
        # Build adjacency lists
        adj1 = [[] for _ in range(m)]
        for u, v in edges1:
            adj1[u].append(v)
            adj1[v].append(u)
            
        adj2 = [[] for _ in range(n)]
        for u, v in edges2:
            adj2[u].append(v)
            adj2[v].append(u)
        
        # Get even/odd counts for both trees
        counts1 = self.getEvenOddCounts(adj1)
        counts2 = self.getEvenOddCounts(adj2)
        
        # For tree2, we want the maximum odd count (because connecting adds 1 to distance)
        max_odd_tree2 = max(odd for even, odd in counts2)
        
        # For each node in tree1, add its even count + best odd count from tree2
        result = []
        for even, odd in counts1:
            result.append(even + max_odd_tree2)
        
        return result