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

    def show_maze(self, show_solution=False, filename=None, wall_width=1):
        fig, ax = plt.subplots()
        grid_size = 1 + wall_width  # route + wall as 1 unit
        ax.set_xlim(0, self.cols * grid_size + wall_width)
        ax.set_ylim(0, self.rows * grid_size + wall_width)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect("equal")

        def cell_to_coord(r, c):
            return c // 2 * grid_size, r // 2 * grid_size

        for r in range(2 * self.rows + 1):
            for c in range(2 * self.cols + 1):
                x, y = cell_to_coord(r, c)

                if self.maze[r, c] == "#":
                    if r % 2 == 0 and c % 2 == 0:  # wall intersection
                        ax.add_patch(
                            plt.Rectangle((x, y), wall_width, wall_width, color="black")
                        )
                    elif r % 2 == 0:  # horizontal wall
                        ax.add_patch(
                            plt.Rectangle((x + wall_width, y), 1, wall_width, color="black")
                        )
                    else:  # vertical wall
                        ax.add_patch(
                            plt.Rectangle((x, y + wall_width), wall_width, 1, color="black")
                        )
                elif self.maze[r, c] == "S":
                    ax.add_patch(
                        plt.Rectangle((x + wall_width, y + wall_width), 1, 1, color="blue")
                    )
                elif self.maze[r, c] == "G":
                    ax.add_patch(
                        plt.Rectangle((x + wall_width, y + wall_width), 1, 1, color="red")
                    )

        if show_solution:

            def paint_route(r, c):
                x, y = cell_to_coord(r, c)
                if r % 2 == 1 and c % 2 == 1:  # route cell
                    ax.add_patch(
                        plt.Rectangle((x + wall_width, y + wall_width), 1, 1, color="yellow")
                    )
                elif r % 2 == 1:  # vertical route
                    ax.add_patch(
                        plt.Rectangle((x, y + wall_width), wall_width, 1, color="yellow")
                    )
                else:  # horizontal route
                    ax.add_patch(
                        plt.Rectangle((x + wall_width, y), 1, wall_width, color="yellow")
                    )

            prev_r, prev_c = self.route[0]
            for i in range(1, len(self.route)):
                r, c = self.route[i]

                paint_route(r + prev_r + 1, c + prev_c + 1)  # Paint the connections
                if i < len(self.route) - 1:  # Goal cell should not be painted.
                    paint_route(2 * r + 1, 2 * c + 1)  # Paint the route corridor
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
    maze_gen.show_maze(wall_width=1 / 2)
    maze_gen.show_maze(show_solution=True, wall_width=1 / 2)
