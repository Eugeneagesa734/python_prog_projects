class Solution(object):
    def differenceOfSums(self, n, m):
        total = n * (n + 1) // 2
        k = n // m
        divisible_sum = m * k * (k + 1) // 2
        return total - 2 * divisible_sum