import heapq
from collections import defaultdict

class BIT:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 2)  # 1-based indexing

    def update(self, idx, delta):
        # Update the BIT at index
        while idx <= self.n + 1:
            self.tree[idx] += delta
            idx += idx & -idx

    def range_add(self, l, r, delta):
        # Add delta to the interval [l, r] (1-based)
        self.update(l, delta)
        self.update(r + 1, -delta)

    def query_point(self, idx):
        # Get prefix sum up to idx (1-based: corresponds to position idx in BIT)
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

class Solution:
    def maxRemoval(self, nums, queries):
        n = len(nums)
        m = len(queries)

        # Check if all queries can cover the nums array
        def canConvert():
            coverage = [0] * (n + 1)
            for l, r in queries:
                coverage[l] += 1
                if r + 1 < n:
                    coverage[r + 1] -= 1
            current = 0
            for i in range(n):
                current += coverage[i]
                if current < nums[i]:
                    return False
            return True

        if not canConvert():
            return -1

        # Group queries by start position, store as (-end, query_index) for max-heap
        queries_by_start = defaultdict(list)
        for idx, (l, r) in enumerate(queries):
            queries_by_start[l].append((-r, idx))  # Negative end for min-heap max effect

        for l in queries_by_start:
            # Sort the list in ascending order (since stored as -r, we get largest r first)
            queries_by_start[l].sort()

        def findMinimumQueries():
            bit = BIT(n)
            used_queries = []
            heap = []  # min-heap of (-end, query_idx)

            for pos in range(n):
                # Add all queries starting at this pos
                while queries_by_start[pos]:
                    neg_end, q_idx = queries_by_start[pos].pop()
                    heapq.heappush(heap, (neg_end, q_idx))

                # Remove queries from heap that end before pos (using BIT 1-based, pos+1)
                while heap:
                    neg_end, q_idx = heap[0]
                    end = -neg_end
                    if end < pos:
                        heapq.heappop(heap)
                    else:
                        break

                # Calculate current coverage
                current_coverage = bit.query_point(pos + 1)  # BIT is 1-based, pos+1 is current index
                deficit = nums[pos] - current_coverage

                while deficit > 0:
                    if not heap:
                        return None
                    neg_end, q_idx = heapq.heappop(heap)
                    l, r = queries[q_idx]
                    # Apply this query's effect to BIT
                    bit.range_add(l + 1, r + 1, 1)
                    used_queries.append(q_idx)
                    deficit -= 1  # Each selected query covers 1 at this pos

            return used_queries

        min_queries = findMinimumQueries()
        if min_queries is None:
            return -1
        return m - len(min_queries)
