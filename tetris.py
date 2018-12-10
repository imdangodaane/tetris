#!/usr/bin/env python3
import curses
import time
from collections import deque
from random import randint


class MakeBlock:
    def __init__(self, width):
        self.blocks = [[
                        [1, 1, 1, 1]
                       ],
                       [
                        [1, 1, 1],
                        [0, 0, 1]
                       ],
                       [
                        [1, 1, 1],
                        [1, 0, 0]
                       ],
                       [
                        [1, 1],
                        [1, 1]
                       ],
                       [
                        [0, 1, 1],
                        [1, 1, 0]
                       ],
                       [
                        [1, 1, 1],
                        [0, 1, 0]
                       ],
                       [
                        [1, 1, 0],
                        [0, 1, 1]
                       ]]
        self.y = 0
        self.shape = self.blocks[randint(0, 6)]
        self.x = randint(0, (width - 3) // 2 - 1)
        self.cell = chr(9617)
        while self.x + len(self.shape[0]) > (width - 3) // 2:
            self.x = randint(0, (width - 3) // 2 - 1)


class Tetris:
    def __init__(self):
        self.screen = None
        self.win_height, self.win_width = 22, 23
        self.score = 0
        self.blocks = deque()
        self.block = 'Empty'
        self.timeout = 0.5
        self.timeflag = time.time()
        self.wall = deque([0 for _ in range((self.win_width - 3) // 2)]
                          for _ in range(self.win_height - 2))
        self.screen_operate()

    def draw_board(self):
        # self.win_height, self.win_width = self.screen.getmaxyx()
        player = 'nqui'[:self.win_width - 1]
        board = 'Tetris'[:self.win_width - 1]
        # self.screen.clear()
        self.screen.border('|', '|', '-', '-', '+', '+', '+', '+')
        self.screen.addstr(0, int(self.win_width / 4) - int(len(player) / 2),
                           player)
        self.screen.addstr(0, int(self.win_width / 4) * 3 -
                           int(len(board) / 2), board)
        self.screen.addstr(int(self.win_height / 3), int(self.win_width / 4)*3
                           - int(len('Score') / 2) + 2, 'Score')
        self.screen.addstr(int(self.win_height / 3) + 1,
                           int(self.win_width / 4) * 3 + 2, str(self.score))
        for y in range(1, self.win_height - 1):
            self.screen.addch(y, self.win_width // 2, '|')
        self.screen.refresh()

    def screen_init(self):
        curses.initscr()
        curses.curs_set(0)
        self.screen = curses.newwin(self.win_height, self.win_width, 0, 0)
        self.screen.keypad(1)
        self.screen.nodelay(1)

    def screen_config(self):
        curses.start_color()
        curses.init_color(1, 0, 450, 450)
        curses.init_color(2, 128, 128, 128)
        curses.init_pair(3, 1, 2)
        curses.init_pair(4, 2, 1)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.bkgd(' ', curses.color_pair(0))
        self.screen.bkgdset(' ', curses.color_pair(3))

    def terminate_screen(self):
        curses.endwin()
        print("Error: Can't operate in this size, terminated program")
        exit(1)

    def press_LEFT(self):
        if (self.block.x > 0 and self.wall[self.block.y][self.block.x-1] == 0):
            self.block.x -= 1

    def press_RIGHT(self):
        if (self.block.x + len(self.block.shape[0]) - 1 <
           (self.win_width - 3) // 2 - 1 and
           self.wall[self.block.y][self.block.x+1] == 0):
            self.block.x += 1

    def rotate(self, m, right):
        if right:
            b = list(zip(*reversed(m)))
        else:
            b = list(zip(*m))
        for i in range(len(b)):
            b[i] = list(b[i])
        return b

    def press_UP(self):
        self.block.shape = self.rotate(self.block.shape, True)

    def press_DOWN(self):
        if self.block.y + len(self.block.shape) < self.win_height - 2:
            if self.can_falling():
                self.block.y += 1

    def falling(self):
        if self.block.y + len(self.block.shape) < self.win_height - 2:
            self.block.y += 1

    def draw_block_shape(self):
        for y in range(len(self.block.shape)):
            for x in range(len(self.block.shape[y])):
                if self.block.shape[y][x] == 1:
                    self.screen.addstr(self.block.y+1+y, self.block.x+1+x,
                                       self.block.cell, curses.color_pair(6))

    def burn_and_update_score(self):
        for i in range(len(self.wall)):
            if 1 in self.wall[i] and sum(self.wall[i]) == 10:
                del self.wall[i]
                self.wall.appendleft([0 for _ in range((self.win_width - 3)
                                     // 2)])
                self.score += 1

    def can_falling(self):
        try:
            for y in range(len(self.block.shape)):
                for x in range(len(self.block.shape[y])):
                    if self.block.shape[y][x] == 0:
                        continue
                    elif (self.block.shape[y][x] == 1 and self.wall
                          [self.block.y+y+1][self.block.x+x] == 0):
                        continue
                    else:
                        return False
            return True
        except IndexError:
            return False

    def update_wall(self):
        for y in range(len(self.block.shape)):
            for x in range(len(self.block.shape[y])):
                if self.block.shape[y][x] == 1:
                    self.wall[self.block.y+y][self.block.x+x] = 1
        self.block = self.blocks.popleft()

    def draw_wall(self):
        for y in range(len(self.wall)):
            for x in range(len(self.wall[y])):
                if self.wall[y][x] == 1:
                    self.screen.addstr(y+1, x+1, self.block.cell)
                else:
                    self.screen.addstr(y+1, x+1, ' ')

    def draw_score(self):
        self.screen.addstr(int(self.win_height / 3) + 1,
                           int(self.win_width / 4) * 3 + 2, str(self.score))

    def update(self):
        self.burn_and_update_score()
        if time.time() - self.timeflag > self.timeout:
            self.timeflag = time.time()
            able_falling = self.can_falling()
            # f = open('log', 'w')
            # for i in self.wall:
            #     f.write(str(i) + '\n')
            # f.write('\n')
            # f.close()
            if able_falling:
                self.falling()
            else:
                self.update_wall()
        if self.block.y + len(self.block.shape) == self.win_height - 2:
            self.update_wall()
        self.draw_wall()
        self.draw_block_shape()
        self.draw_score()

    def object_process(self):
        if not self.blocks:
            self.blocks.append(MakeBlock(self.win_width))
        if self.block == 'Empty':
            self.block = self.blocks.popleft()

    def is_game_over(self):
        if 1 in self.wall[0]:
            return True
        pass

    def game_over(self):
        self.screen.addstr((self.win_height - 2) // 2,
                           ((self.win_width - 3) // 2) - 3,
                           'Game Over', curses.color_pair(5))
        self.screen.addstr((self.win_height - 2) // 2 + 1,
                           ((self.win_width - 3) // 2) - 3,
                           'Score: ' + str(self.score), curses.color_pair(5))
        self.screen.refresh()
        time.sleep(2)
        curses.endwin()
        exit(0)

    def screen_operate(self):
        self.screen_init()
        self.screen_config()
        self.screen.clear()
        key_pressed = -1
        while key_pressed != ord('q'):
            self.draw_board()
            self.object_process()
            if self.screen.getmaxyx() != (self.win_height, self.win_width):
                self.terminate_screen()
            if self.is_game_over():
                self.game_over()
            if key_pressed == curses.KEY_UP:
                self.press_UP()
            elif key_pressed == curses.KEY_DOWN:
                self.press_DOWN()
            elif key_pressed == curses.KEY_LEFT:
                self.press_LEFT()
            elif key_pressed == curses.KEY_RIGHT:
                self.press_RIGHT()
            else:
                pass
            self.update()
            key_pressed = self.screen.getch()
        curses.endwin()


if __name__ == '__main__':
    Tetris()
