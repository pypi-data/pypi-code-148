import pathlib
import random


def get_default_config_path():
    return pathlib.Path(__file__).parent / "res" / "config.json"


class Snake:
    """
    Snake class. Defines one snake for one player.

    :param start_pos: Starting position for the snake. This is position of the head block
                      in pixels, as tuple of x and y position.
    :type start_pos: tuple of int

    :param move_keys: Dictionary that binds directions to keyboard keys. Dictionary should
                      have four keys: 'up', 'right', 'down', and 'left'. Corresponding values
                      should be pygame keyboard codes.
    :type move_keys: dict

    :param color: Color of the snake as rgb code in tuple.
    :type color: tuple

    :param block_size: Size of one block of the snake in pixels.
    :type block_size: int

    :param num_of_start_blocks: Number of starting blocks for the snake.
    :type num_of_start_blocks: int
    """

    def __init__(self, start_pos, move_keys, color, block_size, num_of_start_blocks):

        self.block_size = block_size
        self.start_pos = start_pos
        self.move_keys = move_keys
        self.color = color
        self.num_of_start_blocks = num_of_start_blocks
        self.curr_dir = [1, 0]
        self.key_stack = []
        self.collision = False

        # set first start blocks
        self.block_pos_lst = []
        for i in range(num_of_start_blocks):
            self.block_pos_lst.append((self.start_pos[0] - i * self.block_size, self.start_pos[1]))

    def get_dir_from_keystack(self):
        """
        Updates snake's direction by checking which key was pressed.
        """
        if self.key_stack:
            key_pressed = self.key_stack[0]
            if key_pressed == self.move_keys["up"]:
                new_dir = [0, -1]
            elif key_pressed == self.move_keys["right"]:
                new_dir = [1, 0]
            elif key_pressed == self.move_keys["down"]:
                new_dir = [0, 1]
            elif key_pressed == self.move_keys["left"]:
                new_dir = [-1, 0]
            else:
                new_dir = self.curr_dir

            # if snake just reverts direction, don't allow it
            if new_dir == [-self.curr_dir[0], -self.curr_dir[1]]:
                new_dir = self.curr_dir

            self.curr_dir = new_dir

            self.key_stack.pop(0)

    def set_new_state(self, game_dims, snakes_lst):
        """
        Sets new snake position and also checks if there was a collision with game
        frames or other snakes.

        :param game_dims: Game frame dimensions as tuple of x and y.
        :type game_dims: tuple

        :param snakes_lst: List containing all snakes in the game.
        :type snakes_lst: list of Snake
        """
        # add new block to front of snake according to direction
        new_block = [
            (
                self.block_pos_lst[0][0] + self.curr_dir[0] * self.block_size,
                self.block_pos_lst[0][1] + self.curr_dir[1] * self.block_size,
            )
        ]
        self.block_pos_lst = new_block + self.block_pos_lst

        # remove last block from snake
        self.block_pos_lst.pop()

        # check for collision with screen frame or with other snakes
        # get list of snakes with self removed from it
        othr_snake_lst = [snake for snake in snakes_lst if snake is not self]
        if self.is_frame_collision(game_dims) or self.is_snake_collision(othr_snake_lst):
            self.collision = True
        else:
            self.collision = False

    def is_snake_collision(self, other_snakes):
        """
        Returns True if snake is in collision with itself or other snakes.

        :param other_snakes: List of other snakes in the game.
        :type other_snakes: list of Snake

        :return: True, if snake is in collision with itself or other snakes, False
                 otherwise.
        :rtype: bool
        """
        # check for collision with itself
        if self.block_pos_lst[0] in self.block_pos_lst[1:]:
            return True

        # check for collision with other snakes
        for snake in other_snakes:
            if self.block_pos_lst[0] in snake.block_pos_lst:
                return True

        return False

    def is_frame_collision(self, game_dims):
        """
        Returns True if snake is in collision with game frame.

        :param game_dims: Game frame dimensions as tuple of x and y.
        :type game_dims: tuple

        :return: True, if snake is in collision with game frame, False
                 otherwise.
        :rtype: bool
        """
        return not ((0 <= self.block_pos_lst[0][0] < game_dims[0]) and (0 <= self.block_pos_lst[0][1] < game_dims[1]))


class Cherry:
    """
    Cherry class, defines one cherry in the game.

    :param block_size: Dimension of the block, which represents a cherry.
    :type block_size: int
    """

    def __init__(self, block_size):
        self.block_size = block_size
        self.position = None

    def _is_cherry_position_valid(self, snake_lst):
        """
        Checks that cherry position is not placed onto some snake.

        :param snake_lst: List of snakes in the game.
        :type snake_lst: list of Snake

        :return: True, if cherry is not placed on one of the snakes, False otherwise.
        :rtype: bool
        """
        for snake in snake_lst:
            if self.position in snake.block_pos_lst:
                return False

        return True

    def set_new_random_position(self, snake_lst, game_dims):
        """
        Sets new random position for cherry.

        :param snake_lst: List of snakes in the game.
        :type snake_lst: list of Snake

        :param game_dims: Game frame dimensions as tuple of x and y.
        :type game_dims: tuple
        """

        self.position = (
            random.randrange(0, game_dims[0], self.block_size),
            random.randrange(0, game_dims[1], self.block_size),
        )

        # recursively call function until new cherry position is valid
        if not self._is_cherry_position_valid(snake_lst):
            self.set_new_random_position(snake_lst, game_dims)


class SnakeGameStatusFlags:
    COLLISION_OCCURENCE = 1
