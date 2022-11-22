import asyncio
import curses
import random
import time

# globals
g_win_height = 40
g_win_width = 100
g_score = 0
g_max_possible_score = 0

async def game_loop(win, game_state):
    
    key = await get_user_input(win)

    if key == 27: # esc key
        raise KeyboardInterrupt

    basket_dir = 0
    if key == curses.KEY_LEFT:
        basket_dir = -1
    elif key == curses.KEY_RIGHT:
        basket_dir = 1

    game_state.update(basket_dir)
    await render(win, game_state)
    game_state.time_last_render = await fps_sleep(game_state.fps, game_state.time_last_render)

async def fps_sleep(fps: float, time_last_render: float):
    time_now = time.time()
    time_since_last_render = time_now - time_last_render
    time_to_next_render = 1.0 / fps - time_since_last_render
    if time_to_next_render > 0:
        await asyncio.sleep(time_to_next_render)
    time_last_render = time.time()
    return time_last_render

async def get_user_input(win):
    key = win.getch()
    curses.flushinp()
    return key

async def render(win, game_state):
    global g_score
    global g_win_height
    global g_win_width

    win.clear()
    win.border(0)
    
    # convert from game coords to screen coords and render the basket
    basket_pixel_width = int(g_win_width * game_state.basket_width)
    basket_left_pos = int(g_win_width * (game_state.basket_position[0] + 0.5))
    basket_y = int(g_win_height * (-game_state.basket_position[1] + 0.5))
    for i in range(basket_pixel_width):
        basket_x = basket_left_pos + i
        if basket_x >= 0 and basket_x < g_win_width and basket_y >= 0 and basket_y < g_win_height:
            win.addch(basket_y, basket_x, '#')

    # convert from game coords to screen coords and render the apples
    for apple in game_state.apples:
        apple_x = int(g_win_width * (apple[0] + 0.5))
        apple_y = int(g_win_height * (-apple[1] + 0.5) )
        if apple_x >= 0 and apple_x < g_win_width and apple_y >= 0 and apple_y < g_win_height:
            win.addch(apple_y, apple_x, 'o')
    
    # render score
    win.addstr(0, 0, "score: {}".format(g_score))

class GameState:
    def __init__(self):
        
        self.apples = []
        self.apple_speed = 0.015
        
        self.basket_width = 0.2
        self.basket_speed = 0.035
        self.basket_position = [0.0 - 0.5*self.basket_width, -0.45]

        self.time_last_render = time.time()
        self.fps = 20

    def update(self, basket_dir):
        """
        basket_dir: -1 = left, 0 = no movement, 1 = right
        """
        global g_score
        global g_max_possible_score

        # update the basket position
        new_basket_position = self.basket_position[0] + basket_dir * self.basket_speed
        if new_basket_position > -0.5 and new_basket_position < 0.5 - self.basket_width:
            self.basket_position[0] = new_basket_position

        # create new apples
        if random.randint(1,30) == 1:
            self.apples.append([random.random() - 0.5, 1])

        # update the apple positions, check if any apples were caught
        for apple in self.apples:
            apple[1] -= self.apple_speed
            if apple[1] < self.basket_position[1]:
                if apple[0] > self.basket_position[0] and \
                    apple[0] < self.basket_position[0] + self.basket_width:
                    self.apples.remove(apple)
                    g_score += 1
                    g_max_possible_score += 1
            
            # remove apples that fall off the screen
            if apple[1] < -0.5:
                self.apples.remove(apple)
                g_max_possible_score += 1

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)  # cursor is invisible on the screen\

    win = curses.newwin(g_win_height, g_win_width, 0, 0)
    win.keypad(1)  # takeuser input from the keypad
    win.timeout(0)  # no blocking when reading user input

    try:
        game_state = GameState()
        while True:
            asyncio.run(game_loop(win, game_state))
    except KeyboardInterrupt:
        print("Exiting...")
    
    curses.endwin()

    print(f"Score = {g_score}/{g_max_possible_score}")
    
    

if __name__ == "__main__":
    curses.wrapper(main)
