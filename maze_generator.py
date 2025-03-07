import random
import numpy as np
import matplotlib.pyplot as plt

from route_generator import RouteGenerator


class MazeGenerator:
    def __init__(self, rows, cols, route):
        self.rows = rows
        self.cols = cols
        self.route = route
        self.maze = np.full(  # Initialize everything with walls.
            (2 * rows + 1, 2 * cols + 1), "#"
        )

    def generate_maze(self):
        self._carve_route()
        self._add_extra_paths()

    def _carve_route(self):
        for i, (r, c) in enumerate(self.route):
            self.maze[2 * r + 1, 2 * c + 1] = "."  # Make the root cell a pathway.
            if i > 0:
                prev_r, prev_c = self.route[i - 1]
                wall_r = (2 * r + 1 + 2 * prev_r + 1) // 2
                wall_c = (2 * c + 1 + 2 * prev_c + 1) // 2
                self.maze[wall_r, wall_c] = "."  # Open adjacent walls

        # Set start and goal
        start_r, start_c = self.route[0]
        goal_r, goal_c = self.route[-1]
        self.maze[2 * start_r + 1, 2 * start_c + 1] = "S"
        self.maze[2 * goal_r + 1, 2 * goal_c + 1] = "G"

    def _add_extra_paths(self):
        diggables = self._get_initial_diggables()

        while diggables:
            idx = random.randrange(len(diggables))
            (r, c), (dr, dc) = diggables.pop(idx)

            if self.maze[2 * (r + dr) + 1, 2 * (c + dc) + 1] == ".":
                continue

            self._dig_path(r, c, dr, dc)
            self._add_new_diggables(diggables, r + dr, c + dc)

    def _get_initial_diggables(self):
        diggables = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) == (self.rows - 1, self.cols - 1):
                    continue
                if self.maze[2 * r + 1, 2 * c + 1] == "#":
                    continue

                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.maze[2 * nr + 1, 2 * nc + 1] == "#":
                            diggables.append([(r, c), (dr, dc)])

        return diggables

    def _dig_path(self, r, c, dr, dc):
        self.maze[2 * (r + dr) + 1, 2 * (c + dc) + 1] = "."
        self.maze[2 * r + dr + 1, 2 * c + dc + 1] = "."

    def _add_new_diggables(self, diggables, r, c):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.maze[2 * nr + 1, 2 * nc + 1] == "#":
                    diggables.append([(r, c), (dr, dc)])

    def print_maze(self):
        for row in reversed(self.maze):
            print("".join(row))

    def show_maze(self, show_solution=False, filename=None):
        fig, ax = plt.subplots(figsize=(self.cols, self.rows))
        ax.set_xlim(0, 2 * self.cols + 1)
        ax.set_ylim(0, 2 * self.rows + 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")

        for r in range(2 * self.rows + 1):
            for c in range(2 * self.cols + 1):
                if self.maze[r, c] == "#":
                    ax.add_patch(plt.Rectangle((c, r), 1, 1, color="black"))
                elif self.maze[r, c] == "S":
                    ax.add_patch(plt.Rectangle((c, r), 1, 1, color="blue"))
                elif self.maze[r, c] == "G":
                    ax.add_patch(plt.Rectangle((c, r), 1, 1, color="red"))

        if show_solution:
            prev_r, prev_c = self.route[0]
            for i in range(1, len(self.route)):
                r, c = self.route[i]
                ax.add_patch(  # Paint the connections
                    plt.Rectangle((c + prev_c + 1, r + prev_r + 1), 1, 1, color="yellow")
                )
                if i < len(self.route) - 1:  # Goal cell should not be painted.
                    ax.add_patch(  # Paint the route corridor
                        plt.Rectangle((2 * c + 1, 2 * r + 1), 1, 1, color="yellow")
                    )
                prev_r, prev_c = r, c

        if filename:
            plt.savefig(filename, bbox_inches="tight")
            print(f"Saved maze to {filename}")
        else:
            plt.show()

        plt.close(fig)


if __name__ == "__main__":
    rows, cols = map(int, input().split())
    start_pos = tuple(map(int, input().split()))
    if start_pos:
        route_generator = RouteGenerator(rows, cols, start_pos)
    else:
        route_generator = RouteGenerator(rows, cols)
    route_generator.show()

    maze_gen = MazeGenerator(rows, cols, route_generator.visited_stack)
    maze_gen.generate_maze()
    maze_gen.show_maze()
    maze_gen.show_maze(show_solution=True)
