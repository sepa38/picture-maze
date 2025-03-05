# Picture Maze
Picture Maze is a Python project that generates a maze based on a predefined route and allows visualization using `matplotlib`. Users can create a route interactively using `RouteGenerator` and then generate a corresponding maze with `MazeGenerator`.

## Features
- **Interactive Route Creation:** Users can define a route by dragging the mouse or using arrow keys in a `matplotlib` window.
- **Maze Generation:** The generated maze follows the predefined route and fills the remaining space using a randomized algorithm.
- **Visualization:** The maze can be displayed using `matplotlib`, and the solution path can be highlighted.
- **Image Saving:** The generated maze can be saved as an image file.

## Usage
### Generating a Route
```python
from route_generator import RouteGenerator

route_generator = RouteGenerator(rows=5, cols=10)
route_generator.show()  # Opens a Matplotlib window for route creation
route = route_generator.visited_stack

```
Users can create a route by dragging the mouse or using arrow keys within the `matplotlib` window.

### Generating a Maze
```python
from maze_generator import MazeGenerator

maze_gen = MazeGenerator(rows=5, cols=10, route=route)
maze_gen.generate_maze()
maze_gen.show_maze(show_solution=True, save_path="maze.png")

```
This generates a maze based on the created route and displays it with the solution highlighted. The maze can also be saved as an image file.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
