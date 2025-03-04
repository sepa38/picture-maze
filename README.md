# Picture Maze
Picture Maze is a Python project that generates and visualizes mazes based on predefined routes. The mazes are displayed using `matplotlib`, and solutions can be highlighted in the visualization.

## Features
- Generate mazes based on predefined routes.
- Display mazes with `matplotlib`.
- Highlight the correct path in the maze.
- Save maze images to a file.

## Usage
### Generating and Displaying a Maze
```python
from route_generator import RouteGenerator
from maze_generator import MazeGenerator

# Generate a route
route_generator = RouteGenerator(rows=5, cols=10)

# Generate a maze based on the route
maze_gen = MazeGenerator(rows=5, cols=10, route=route_generator.visited_stack)
maze_gen.generate_maze()

# Display the maze
maze_gen.show_maze(show_solution=True)
```

### Saving the Maze Image
You can save the generated maze to a file by specifying a filename:
```python
maze_gen.show_maze(show_solution=True, filename="maze.png")
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
