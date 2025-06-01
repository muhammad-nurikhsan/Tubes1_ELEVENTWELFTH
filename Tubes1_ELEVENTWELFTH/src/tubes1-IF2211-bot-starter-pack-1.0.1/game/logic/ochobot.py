# Kelompok : ELEVENTWELFTH (STIGMA RD)
# Nama Anggota:
# 1. Muhammad Nurikhsan 123140057
# 2. Aryasatya Widyatna Akbar 123140164
# 3. Devina Kartika 123140036

import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class Ochobot(BaseLogic): 
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.board_width = 15
        self.board_height = 15

    def manhattan_distance(self, pos1: Position, pos2: tuple):
        return abs(pos1.x - pos2[0]) + abs(pos1.y - pos2[1])

    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.board_width and 0 <= y < self.board_height
    
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        current_position = board_bot.position
        my_x, my_y = current_position.x, current_position.y

        if props.diamonds >= 4:
            self.goal_position = props.base
        else:
            diamonds = [
                obj for obj in board.game_objects
                if obj.type == "DiamondGameObject"
            ]
            teleporters = [
                obj for obj in board.game_objects
                if obj.type == "TeleporterGameObject"
            ]
            button = next(
                (obj for obj in board.game_objects if obj.type == "DiamondButtonGameObject"),
                None
            )
            opponents = [
                p for p in board.bots
                if p != board_bot and p.properties.diamonds > 0
            ]

            if opponents:
                nearest_opponent = min(
                    opponents,
                    key=lambda p: self.manhattan_distance(current_position, (p.position.x, p.position.y))
                )
                if self.manhattan_distance(current_position, (nearest_opponent.position.x, nearest_opponent.position.y)) <= 2:
                    self.goal_position = nearest_opponent.position
                else:
                    self.goal_position = None
            else:
                self.goal_position = None

            if not self.goal_position and diamonds:
                target_diamond = min(
                    diamonds,
                    key=lambda d: (
                        self.manhattan_distance(current_position, (d.position.x, d.position.y)),
                        -d.properties.points 
                    )
                )
                self.goal_position = target_diamond.position

            if not self.goal_position and teleporters and len(teleporters) == 2:
                t1, t2 = teleporters
                t1_pos = (t1.position.x, t1.position.y)
                t2_pos = (t2.position.x, t2.position.y)
                if diamonds:
                    nearest_diamond = min(
                        diamonds,
                        key=lambda d: self.manhattan_distance(current_position, (d.position.x, d.position.y))
                    )
                    diamond_pos = (nearest_diamond.position.x, nearest_diamond.position.y)
                    dist_to_diamond = self.manhattan_distance(current_position, diamond_pos)
                    dist_t1 = self.manhattan_distance(current_position, t1_pos)
                    dist_t2 = self.manhattan_distance(current_position, t2_pos)
                    dist_after_t1 = self.manhattan_distance(Position(t2_pos[0], t2_pos[1]), diamond_pos)
                    dist_after_t2 = self.manhattan_distance(Position(t1_pos[0], t1_pos[1]), diamond_pos)
                    if dist_t1 + dist_after_t1 < dist_to_diamond:
                        self.goal_position = t1.position
                    elif dist_t2 + dist_after_t2 < dist_to_diamond:
                        self.goal_position = t2.position

            if not self.goal_position and button and len(diamonds) < 3:
                self.goal_position = button.position

            if not self.goal_position:
                self.goal_position = props.base

        if self.goal_position:
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
            next_x, next_y = my_x + delta_x, my_y + delta_y
            if not self.is_valid_position(next_x, next_y):
                delta_x, delta_y = 0, 0  
            else:
                obstacles = [
                    (obj.position.x, obj.position.y)
                    for obj in board.game_objects
                    if obj.type in ["WallGameObject", "BotGameObject"]
                ]
                if (next_x, next_y) in obstacles and not (self.goal_position.x == next_x and self.goal_position.y == next_y):
                    delta_x, delta_y = 0, 0  

        if delta_x == 0 and delta_y == 0:
            valid_moves = [
                (dx, dy) for dx, dy in self.directions
                if self.is_valid_position(my_x + dx, my_y + dy)
                and (my_x + dx, my_y + dy) not in [
                    (obj.position.x, obj.position.y)
                    for obj in board.game_objects
                    if obj.type in ["WallGameObject", "BotGameObject"]
                ]
            ]
            if valid_moves:
                delta_x, delta_y = random.choice(valid_moves)
            else:
                delta_x, delta_y = self.directions[self.current_direction]
                self.current_direction = (self.current_direction + 1) % len(self.directions)

        return delta_x, delta_y
    