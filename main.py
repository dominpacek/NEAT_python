import pygame
import numpy as np
import random


def generate_new_apple():
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    return apple_position


def collision_with_boundaries(snake_head):
    if snake_head[0] >= 500 or snake_head[0] < 0 or snake_head[1] >= 500 or snake_head[1] < 0:
        return 1
    else:
        return 0


def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return 1
    else:
        return 0


def is_direction_blocked(snake_position, current_direction_vector):
    next_step = snake_position[0] + current_direction_vector
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) == 1 or collision_with_self(snake_position) == 1:
        return 1
    else:
        return 0


def move_snake(snake_head, snake_position, apple_position, direction, score):
    if direction == 0:
        snake_head[0] -= 10
    elif direction == 1:
        snake_head[0] += 10
    elif direction == 2:
        snake_head[1] += 10
    elif direction == 3:
        snake_head[1] -= 10
    else:
        pass

    if snake_head == apple_position:
        apple_position = generate_new_apple()
        score += 1
        snake_position.insert(0, list(snake_head))

    else:
        snake_position.insert(0, list(snake_head))
        snake_position.pop()

    return snake_position, apple_position, score


def draw_snake(snake_position):
    for position in snake_position:
        pygame.draw.rect(display, (0, 120, 0), pygame.Rect(position[0], position[1], 10, 10))


def draw_apple(display, apple_position):
    pygame.draw.rect(display, (230, 60, 0), pygame.Rect(apple_position[0], apple_position[1], 10, 10))


def display_final_score(display_text, final_score):
    largeText = pygame.font.Font('freesansbold.ttf', 35)
    TextSurf = largeText.render(display_text, True, (0, 0, 0))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width / 2), (display_height / 2))
    display.blit(TextSurf, TextRect)
    pygame.display.update()

    display_screen = True
    while display_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_screen = False
            elif event.type == pygame.KEYDOWN:
                display_screen = False


# TODO enum for directions
def pick_correct_direction(previous_direction, new_direction):
    if (new_direction == 0 and previous_direction == 1) \
            or (new_direction == 1 and previous_direction == 0) \
            or (new_direction == 2 and previous_direction == 3) \
            or (new_direction == 3 and previous_direction == 2):
        new_direction = previous_direction

    return new_direction


'''
LEFT -> button_direction = 0
RIGHT -> button_direction = 1
DOWN -> button_direction = 2
UP -> button_direction = 3
'''


def play_game(snake_head, snake_position, apple_position, nn=None, human_controlled=True, score=0, clock_speed=10):
    crashed = False
    previous_direction = 1
    previous_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

    # Main game loop
    while crashed is not True:
        for event in (events := pygame.event.get()):

            if event.type == pygame.QUIT:
                crashed = True
                continue
            if human_controlled:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        new_direction = 0
                    elif event.key == pygame.K_RIGHT:
                        new_direction = 1
                    elif event.key == pygame.K_DOWN:
                        new_direction = 2
                    elif event.key == pygame.K_UP:
                        new_direction = 3
                else:
                    new_direction = previous_direction
        if not human_controlled:
            new_direction = random.randint(0, 3)

        new_direction = pick_correct_direction(previous_direction, new_direction)
        display.fill(window_color)
        draw_apple(display, apple_position)
        draw_snake(snake_position)

        snake_position, apple_position, score = move_snake(snake_head, snake_position, apple_position,
                                                           new_direction, score)

        pygame.display.set_caption("SCORE: " + str(score))
        pygame.display.update()

        previous_direction = new_direction

        if is_direction_blocked(snake_position, previous_direction_vector) == 1:
            crashed = True

        clock.tick(clock_speed)

    return score


if __name__ == "__main__":

    # SETUP #
    display_width = 500
    display_height = 500

    window_color = (200, 200, 200)
    clock = pygame.time.Clock()

    # TODO rewrite all usages to use snake_position[0] instead of snake_head
    head_startpos = [250, 250]
    snake_startpos = [[250, 250], [240, 250], [230, 250]]
    # todo move pygame stuff to its class
    pygame.init()  # initialize pygame modules

    display = pygame.display.set_mode((display_width, display_height))
    display.fill(window_color)
    pygame.display.update()

    # Neural network #



    score = play_game(head_startpos, snake_startpos, generate_new_apple(), None, False)
    pygame.display.update()



    display_text = f'Final score: {score}'
    display_final_score(display_text, score)

    pygame.quit()
