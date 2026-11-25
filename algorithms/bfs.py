from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial.tiles}
        result = SearchResult(solution=None, nodes_generated=1, max_frontier_size=1)

        while frontier:
            state = frontier.popleft()
            if state.is_goal:
                result.solution = state
                result.depth = state.cost - initial.cost
                break

            result.nodes_expanded += 1
            for neighbor in state.neighbors():
                if neighbor.tiles in visited:
                    continue
                visited.add(neighbor.tiles)
                frontier.append(neighbor)
                result.nodes_generated += 1
            result.max_frontier_size = max(result.max_frontier_size, len(frontier))

        return result
