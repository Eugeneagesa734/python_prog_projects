from collections import deque

class Solution:
    def snakesAndLadders(self, board):
        n = len(board)

        def get_pos(square):
            square -= 1
            r = square // n
            c = square % n
            if r % 2 == 1:
                c = n - 1 - c
            return (n - 1 - r, c)

        queue = deque([(1, 0)])
        visited = set()
        visited.add(1)

        while queue:
            curr, steps = queue.popleft()

            for i in range(1, 7):
                next_square = curr + i

                if next_square > n * n:
                    continue

                r, c = get_pos(next_square)

                if board[r][c] != -1:
                    next_square = board[r][c]

                if next_square == n * n:
                    return steps + 1

                if next_square not in visited:
                    visited.add(next_square)
                    queue.append((next_square, steps + 1))

        return -1