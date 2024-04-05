import heapq

class Node:
    def __init__(self, state, parent=None, move=None, depth=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = self.calcular_custo()

    def calcular_custo(self):
        return self.depth + self.calcular_heuristica()

    def calcular_heuristica(self):
        distancia = 0
        estado_final = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    goal_row, goal_col = divmod(self.state[i][j] - 1, 3)
                    distancia += abs(i - goal_row) + abs(j - goal_col)
        return distancia

    def __lt__(self, other):
        return self.cost < other.cost

    def generate_children(self):
        children = []
        i, j = self.find_blank()
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for move in moves:
            new_i, new_j = i + move[0], j + move[1]
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in self.state]
                new_state[i][j], new_state[new_i][new_j] = (
                    new_state[new_i][new_j],
                    new_state[i][j],
                )
                children.append(
                    Node(
                        new_state,
                        parent=self,
                        move=(new_i, new_j),
                        depth=self.depth + 1,
                    )
                )
        return children

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j

    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]


def a_star(initial_state):
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, initial_state)
    steps = 0

    while open_list:
        current_node = heapq.heappop(open_list)
        steps += 1
        if current_node.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            return current_node.get_path(), steps

        closed_set.add(tuple(map(tuple, current_node.state)))
        children = current_node.generate_children()

        for child in children:
            if tuple(map(tuple, child.state)) not in closed_set:
                heapq.heappush(open_list, child)
                closed_set.add(tuple(map(tuple, child.state)))

    return None, steps


def resultado(solution, steps):
    if solution:
        for i, step in enumerate(solution):
            print(f"Step {i + 1}:")
            for row in step:
                print(row)
            print("----")
        print(f"Quantidade total de steps: {steps}")
    else:
        print("Nenhuma solução encontrada.")


if __name__ == "__main__":
    initial_state = [[1, 0, 3], [4, 2, 5], [7, 8, 6]]
    initial_node = Node(initial_state)
    solution, steps = a_star(initial_node)
    resultado(solution, steps)
