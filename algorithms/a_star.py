import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import GOAL_STATE, State
from puzzle.result import SearchResult


GOAL_POSITIONS = {tile: divmod(index, 3) for index, tile in enumerate(GOAL_STATE) if tile != 0}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(index, 3)
            goal_row, goal_col = GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        order = count()
        frontier = [(initial.cost + self.heuristic(initial), next(order), initial)]
        best_cost = {initial.tiles: initial.cost}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            _, _, state = heapq.heappop(frontier)
            if state.cost != best_cost[state.tiles]:
                continue
            if state.is_goal:
                result.solution = state
                result.depth = state.cost - initial.cost
                break

            result.nodes_expanded += 1
            for neighbor in state.neighbors():
                previous_cost = best_cost.get(neighbor.tiles)
                if previous_cost is not None and previous_cost <= neighbor.cost:
                    continue
                best_cost[neighbor.tiles] = neighbor.cost
                priority = neighbor.cost + self.heuristic(neighbor)
                heapq.heappush(frontier, (priority, next(order), neighbor))
                result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
