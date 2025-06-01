class Solution:
    def distributeCandies(self, n, limit):
        def c(k):
            return k * (k - 1) // 2 if k >= 2 else 0
        
        total = c(n + 2)
        total -= 3 * c(n - limit + 1)
        total += 3 * c(n - 2 * limit)
        total -= c(n - 3 * limit - 1)
        
        return max(total, 0)