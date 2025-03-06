import pickle
import numpy as np
import matplotlib.pyplot as plt


class RouteGenerator:
    def __init__(self, rows, cols, start_pos=(0, 0)):
        self.rows = rows
        self.cols = cols
        self.grid = np.zeros((rows, cols))
        self.current = start_pos
        self.visited_stack = [self.current]
        self.grid[self.current] = 1
        self.is_dragging = False

        self.fig, self.ax = plt.subplots()
        self.update_plot()

        self.fig.canvas.mpl_connect("button_press_event", self.on_press)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

    def whiten_connection(self, row, col, adj_row, adj_col):
        if adj_row == row + 1:
            self.ax.add_patch(plt.Rectangle((col + 0.4, row + 0.6), 0.2, 0.4, color="white"))
        elif adj_row == row - 1:
            self.ax.add_patch(plt.Rectangle((col + 0.4, row), 0.2, 0.4, color="white"))
        elif adj_col == col + 1:
            self.ax.add_patch(plt.Rectangle((col + 0.6, row + 0.4), 0.4, 0.2, color="white"))
        elif adj_col == col - 1:
            self.ax.add_patch(plt.Rectangle((col, row + 0.4), 0.4, 0.2, color="white"))

    def update_plot(self):
        self.ax.clear()
        for i in range(len(self.visited_stack) - 1):
            row, col = self.visited_stack[i]

            self.ax.add_patch(plt.Rectangle((col, row), 1, 1, color="black"))
            self.ax.add_patch(plt.Rectangle((col + 0.4, row + 0.4), 0.2, 0.2, color="white"))

            # Whiten the connection to the next cell.
            next_row, next_col = self.visited_stack[i + 1]
            self.whiten_connection(row, col, next_row, next_col)

            # Whiten the connection to the previous cell.
            if i > 0:
                prev_row, prev_col = self.visited_stack[i - 1]
                self.whiten_connection(row, col, prev_row, prev_col)

        # Redden the current cell
        row, col = self.current
        self.ax.add_patch(plt.Rectangle((col, row), 1, 1, color="red"))

        self.ax.set_xlim(0, self.cols)
        self.ax.set_ylim(0, self.rows)
        self.ax.set_xticks(np.arange(0, self.cols + 1, 1))
        self.ax.set_yticks(np.arange(0, self.rows + 1, 1))
        self.ax.grid(which="both", color="black", linestyle="-", linewidth=1)
        self.ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        self.ax.set_aspect("equal")

    def move_to(self, new_pos):
        row, col = new_pos
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if new_pos == self.visited_stack[-1]:
            return
        if abs(new_pos[0] - self.current[0]) + abs(new_pos[1] - self.current[1]) > 1:
            return

        if len(self.visited_stack) >= 2 and self.visited_stack[-2] == new_pos:
            self.grid[self.current] = 0
            self.current = new_pos
            self.visited_stack.pop()
        elif new_pos not in self.visited_stack:
            self.current = new_pos
            self.visited_stack.append(self.current)
            self.grid[self.current] = 1

        self.update_plot()
        self.fig.canvas.draw_idle()

    def on_key(self, event):
        moves = {"up": (1, 0), "down": (-1, 0), "left": (0, -1), "right": (0, 1)}
        if event.key in moves:
            delta = moves[event.key]
            new_pos = (self.current[0] + delta[0], self.current[1] + delta[1])
            self.move_to(new_pos)
        elif event.key == "u" and len(self.visited_stack) > 1:  # undo
            popped = self.visited_stack.pop()
            self.grid[popped] = 0
            self.current = self.visited_stack[-1]
            self.update_plot()
            self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.xdata is not None and event.ydata is not None:
            col, row = int(event.xdata), int(event.ydata)
            if (row, col) == self.current:
                self.is_dragging = True

    def on_release(self, event):
        self.is_dragging = False

    def on_motion(self, event):
        if self.is_dragging and event.xdata is not None and event.ydata is not None:
            col, row = int(event.xdata), int(event.ydata)
            self.move_to((row, col))

    def save_route(self, filename="route.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self.visited_stack, f)

    def show(self):
        plt.show()


if __name__ == "__main__":
    rows, cols = map(int, input().split())
    start_pos = tuple(map(int, input().split()))
    if start_pos:
        generator = RouteGenerator(rows, cols, start_pos)
    else:
        generator = RouteGenerator(rows, cols)
    generator.show()
    generator.save_route()
