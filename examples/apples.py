import recall as rl

import curses
import random
import time

# globals
g_win_height = 40
g_win_width = 100
g_score = 0

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)  # cursor is invisible on the screen

    win = curses.newwin(g_win_height, g_win_width, 0, 0)
    win.keypad(1)  # takeuser input from the keypad

    loop(win)

    curses.endwin()


def loop(win):
    win.timeout(50)

    basket_width = int(g_win_width / 10)
    basket_pos_x = int(g_win_width / 2)
    
    basket = [] 
    for i in range(basket_width):
        basket.append([basket_pos_x - int(basket_width * 0.5) + i, g_win_height-2])
    apples = [[5, 5], [10, 12]]

    pos_x = 1
    pos_y = 1

    key = curses.KEY_F0
    next_key = key
    while True:
        key = win.getch()
        update(apples, basket, key)

        win.clear()
        win.border(0) # render the border
        render_basket(win, basket)
        render_apples(win, apples)
        render_score(win)

        pos_x += 1
        pos_y += 1
        pos_x = pos_x % 100
        pos_y = pos_y % 40
        

        if int(key) == 27: # esc key
            break

#        time.sleep(0.1)
        
def update(apples, basket, key):
    global g_score

    basket_dir = 0
    if key == curses.KEY_LEFT:
        basket_dir = -2
    elif key == curses.KEY_RIGHT:
        basket_dir = 2

    # make sure the basket stay inbounds
    if basket[0][0] + basket_dir > 1 and basket[-1][0] + basket_dir < g_win_width - 2:
        for b in basket:
            b[0] += basket_dir

    # create new apples
    if random.randint(1,10) == 1:
        apples.append([random.randint(1, g_win_width-2), 1])

    # update the apple positions
    for apple in apples:
        apple[1] += 1


    # see if apple falls off screen or in basket
    for apple in apples:
        if apple in basket:
            g_score += 1
            apples.remove(apple)
        elif apple[1] > g_win_height - 2:
            apples.remove(apple)


def render_basket(win, basket):
    for b in basket:
        win.addch(b[1], b[0], 'B')

def render_apples(win, apples):
    for apple in apples:
        win.addch(apple[1], apple[0], 'a')

def render_score(win):
    win.addstr(0, 0, "score: {}".format(g_score))

if __name__ == "__main__":
    # Wrapper handles the init and cleanup of the curses terminal
    curses.wrapper(main) 
