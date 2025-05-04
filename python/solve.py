import heapq
import numpy as np
import board

class Puzzle:
    def __init__(self, board, moves=0, previous=None):
        self.board = np.array(board)
        self.moves = moves
        self.previous = previous
        self.size = len(board)
        self.empty_pos = tuple(np.argwhere(self.board == 0)[0])
    
    def __lt__(self, other):
        return (self.moves + self.heuristic()*10) < (other.moves + other.heuristic()*10)
    
    def heuristic(self):
        """Manhattan distance heuristic"""
        dist = 0
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r, c]
                if val != 0:
                    target_r, target_c = divmod(val - 1, self.size)
                    dist += abs(target_r - r) + abs(target_c - c)
        return dist
    
    def possible_moves(self):
        """Generate possible moves"""
        r, c = self.empty_pos
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                new_board = self.board.copy()
                new_board[r, c], new_board[nr, nc] = new_board[nr, nc], new_board[r, c]
                moves.append(Puzzle(new_board, self.moves + 1, self))
        
        return moves
    
    def is_goal(self):
        """Check if current board is solved"""
        return np.array_equal(self.board, np.arange(1, self.size**2 + 1).reshape(self.size, self.size) % (self.size**2))
    
    def reconstruct_path(self):
        """Reconstruct the path from initial to goal state with moves"""
        path = []
        state = self
        while state.previous:
            prev_empty_pos = state.previous.empty_pos
            curr_empty_pos = state.empty_pos
            direction = -1
            if prev_empty_pos[0] > curr_empty_pos[0]:
                direction = 1
            elif prev_empty_pos[0] < curr_empty_pos[0]:
                direction = 3
            elif prev_empty_pos[1] > curr_empty_pos[1]:
                direction = 0
            elif prev_empty_pos[1] < curr_empty_pos[1]:
                direction = 2
            
            path.append((curr_empty_pos[0],curr_empty_pos[1],direction))
            state = state.previous
        return path[::-1]
    
    def __str__(self):
        return str(self.board)
    
def compress_path(path):
    if not path:
        return []

    compressed = [path[0]]  # 最初の要素はそのまま追加
    for i in range(1, len(path)):
        if path[i][2] != compressed[-1][2]:  # dirが異なる場合のみ追加
            compressed.append(path[i])
        else:
            compressed[-1] = path[i]  # 同じdirなら最後の要素を更新
    return compressed

def solve_puzzle():
    start = Puzzle(board.board)
    heap = [start]
    visited = set()
    
    while heap:
        current = heapq.heappop(heap)
        
        if current.is_goal():
            return compress_path(current.reconstruct_path())
        
        visited.add(tuple(current.board.flatten()))
        
        for move in current.possible_moves():
            if tuple(move.board.flatten()) not in visited:
                heapq.heappush(heap, move)
    
    return None

print(solve_puzzle())