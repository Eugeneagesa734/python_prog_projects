from collections import defaultdict, deque

class Solution:
    def largestPathValue(self, colors, edges):
        n = len(colors)
        graph = defaultdict(list)
        indegree = [0] * n
        
        for u, v in edges:
            graph[u].append(v)
            indegree[v] += 1

        dp = [[0] * 26 for _ in range(n)]
        queue = deque()

        for i in range(n):
            if indegree[i] == 0:
                queue.append(i)

        processed = 0
        max_color_value = 0

        while queue:
            node = queue.popleft()
            processed += 1

            color_idx = ord(colors[node]) - ord('a')
            dp[node][color_idx] += 1
            max_color_value = max(max_color_value, dp[node][color_idx])

            for neighbor in graph[node]:
                for c in range(26):
                    dp[neighbor][c] = max(dp[neighbor][c], dp[node][c])
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return max_color_value if processed == n else -1