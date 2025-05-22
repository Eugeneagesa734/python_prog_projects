import heapq
from collections import defaultdict

class Solution:
    def maxRemoval(self, nums, queries):
        n = len(nums)
        m = len(queries)

        def canConvert(query_indices):
            coverage = [0] * (n + 1)
            for idx in query_indices:
                left, right = queries[idx]
                coverage[left] += 1
                if right + 1 < n:
                    coverage[right + 1] -= 1
            
            current_coverage = 0
            for i in range(n):
                current_coverage += coverage[i]
                if current_coverage < nums[i]:
                    return False
            return True
        
        if not canConvert(range(m)):
            return -1

        queries_by_start = defaultdict(list)
        for i, (left, right) in enumerate(queries):
            queries_by_start[left].append((right, i))
        
        for start in queries_by_start:
            queries_by_start[start].sort(reverse=True)

        def findMinimumQueries():
            needed = nums[:]
            used_queries = []
            available_queries = []
            
            for pos in range(n):
                if pos in queries_by_start:
                    for end, query_idx in queries_by_start[pos]:
                        heapq.heappush(available_queries, (-end, query_idx))
                
                valid_queries = []
                while available_queries:
                    neg_end, query_idx = heapq.heappop(available_queries)
                    end = -neg_end
                    if end >= pos:
                        valid_queries.append((neg_end, query_idx))
                
                available_queries = valid_queries
                heapq.heapify(available_queries)

                while needed[pos] > 0 and available_queries:
                    neg_end, query_idx = heapq.heappop(available_queries)
                    end = -neg_end
                    left = queries[query_idx][0]
                    
                    used_queries.append(query_idx)
                    for i in range(left, min(end + 1, n)):
                        needed[i] -= 1
                
                if needed[pos] > 0:
                    return None
            
            return used_queries

        min_queries = findMinimumQueries()
        if min_queries is None:
            return -1
        
        return m - len(min_queries)