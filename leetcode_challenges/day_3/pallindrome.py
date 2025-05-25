from collections import Counter

class Solution:
    def longestPalindrome(self, words):
        count = Counter(words)
        res = 0
        used_in_center = False

        for word in list(count.keys()):
            rev = word[::-1]
            if word == rev:
                # Palindromic word (like "aa", "cc")
                pairs = count[word] // 2
                res += pairs * 4
                count[word] -= pairs * 2
                if not used_in_center and count[word] > 0:
                    res += 2  # One can go in the center
                    used_in_center = True
            else:
                if rev in count:
                    pairs = min(count[word], count[rev])
                    res += pairs * 4
                    count[word] -= pairs
                    count[rev] -= pairs

        return res