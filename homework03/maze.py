from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

Cell = Union[str, int]
Coord = Tuple[int, int]
Path = List[Coord]


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


EMPTY = " "


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    dirs = []
    if x - 2 >= 1:
        dirs.append("U")
    if y + 2 <= cols - 2:
        dirs.append("R")
    if not dirs:
        return grid

    d = choice(dirs)
    if d == "U":
        grid[x - 1][y] = EMPTY
    else:
        grid[x][y + 1] = EMPTY
    return grid


def bin_tree_maze(
    rows: int = 15,
    cols: int = 15,
    random_exit: bool = True,
) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []

    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        direction = choice(["up", "right"])
        can_go_up = x > 1
        can_go_right = y < cols - 2

        if direction == "up":
            if can_go_up:
                grid[x - 1][y] = " "
            elif can_go_right:
                grid[x][y + 1] = " "
        elif direction == "right":
            if can_go_right:
                grid[x][y + 1] = " "
            elif can_go_up:
                grid[x - 1][y] = " "

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    exits = []

    for j in range(cols):
        if grid[0][j] == "X":
            exits.append((0, j))
    for j in range(cols):
        if grid[rows - 1][j] == "X":
            exits.append((rows - 1, j))

    for i in range(rows):
        if grid[i][0] == "X":
            exits.append((i, 0))
    for i in range(rows):
        if grid[i][cols - 1] == "X":
            exits.append((i, cols - 1))

    uniq = []
    for e in exits:
        if e not in uniq:
            uniq.append(e)
    return uniq


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    rows, cols = len(grid), len(grid[0])
    nk = k + 1

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                for ni, nj in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0:
                        grid[ni][nj] = nk

    return grid


def shortest_path(grid: List[List[Cell]], exit_coord: Coord) -> Optional[Path]:
    ex, ey = exit_coord
    val = grid[ex][ey]
    if not isinstance(val, int) or val <= 0:
        return None

    path: Path = [(ex, ey)]
    k: int = val

    while k != 1:
        x, y = path[-1]
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == k - 1:
                path.append((nx, ny))
                k -= 1
                break
        else:
            return None

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    checks = []
    if x == 0:
        checks.append((1, y))
    if x == rows - 1:
        checks.append((rows - 2, y))
    if y == 0:
        checks.append((x, 1))
    if y == cols - 1:
        checks.append((x, cols - 2))

    for cx, cy in checks:
        if 0 <= cx < rows and 0 <= cy < cols and grid[cx][cy] == " ":
            return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    exits = get_exits(grid)

    if len(exits) < 2:
        return grid, exits[0] if exits else None

    entrance, exit_ = exits[0], exits[1]

    if entrance[1] == 0 and exit_[1] == 0 and entrance[0] < exit_[0]:
        entrance, exit_ = exit_, entrance

    if encircled_exit(grid, entrance) or encircled_exit(grid, exit_):
        return grid, None

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if grid[i][j] == " ":
                grid[i][j] = 0

    grid[entrance[0]][entrance[1]] = 1
    grid[exit_[0]][exit_[1]] = 0

    k = 0
    while grid[exit_[0]][exit_[1]] == 0:
        k += 1
        prev = [r[:] for r in grid]
        make_step(grid, k)
        if grid == prev:
            return grid, None

    path = shortest_path(grid, exit_)
    if path is not None:
        path = list(reversed(path))
    return grid, path


def add_path_to_grid(grid: List[List[Cell]], path: Optional[Path]) -> List[List[Cell]]:
    if path is None:
        return grid
    for x, y in path:
        grid[x][y] = "X"
    return grid
