import random

import numpy as np
import pygame

# SETUP #

display_width = 30 * 10
display_height = 30 * 10

window_color = (200, 200, 200)
clock = pygame.time.Clock()

pygame.init()  # initialize pygame modules

display = pygame.display.set_mode((display_width, display_height))
display.fill(window_color)
pygame.display.update()

def generate_new_apple():
    apple_position = [random.randrange(1, display_width // 10) * 10, random.randrange(1, display_height // 10) * 10]
    return apple_position


def collision_with_boundaries(snake_head):
    if snake_head[0] >= display_width or snake_head[0] < 0 or snake_head[1] >= display_height or snake_head[1] < 0:
        return True
    else:
        return False


def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1:]:
        return True
    else:
        return False


def snake_hit_obstacle(snake_position):
    snake_head = snake_position[0]
    if collision_with_boundaries(snake_head) or collision_with_self(snake_position):
        return True
    else:
        return False


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


def draw_snake(snake_position, color):
    for position in snake_position:
        pygame.draw.rect(display, color, pygame.Rect(position[0], position[1], 10, 10))


def draw_apple(display, apple_position):
    pygame.draw.rect(display, (230, 60, 0), pygame.Rect(apple_position[0], apple_position[1], 10, 10))


def get_inputs(snake_position, apple_position):
    snake_head = snake_position[0]

    direction = np.array(snake_head) - np.array(snake_position[1])
    next_position = list(snake_head + direction)
    is_front_blocked = 1 if snake_hit_obstacle([next_position] + snake_position[0:-1]) else 0

    left_position = list(np.array(snake_head + np.array([direction[1], -direction[0]])))

    is_left_blocked = 1 if snake_hit_obstacle([left_position] + snake_position[0:-1]) else 0

    right_position = list(np.array(snake_head + np.array([-direction[1], direction[0]])))
    is_right_blocked = 1 if snake_hit_obstacle([right_position] + snake_position[0:-1]) else 0

    direction = direction // 10

    x_apple_to_snake = apple_position[0] - snake_head[0]
    y_apple_to_snake = apple_position[1] - snake_head[1]
    x_snake = snake_head[0]
    y_snake = snake_head[1]

    # normalize
    x_apple_to_snake = x_apple_to_snake / display_width
    y_apple_to_snake = y_apple_to_snake / display_height
    x_snake = x_snake / display_width
    y_snake = y_snake / display_height

    result = [x_apple_to_snake, y_apple_to_snake, x_snake, y_snake,
              is_left_blocked, is_front_blocked, is_right_blocked]

    return result


def get_angle_to_apple(snake_position, apple_position):
    snake_head = np.array(snake_position[0])
    direction = np.array(snake_head) - np.array(snake_position[1])

    # Calculate the vector from the snake head to the apple
    apple_vector = np.array(apple_position) - snake_head

    # Calculate the cosine of the angle between the vectors
    cosine_angle = np.dot(apple_vector, direction) / (np.linalg.norm(direction) * np.linalg.norm(apple_vector))

    # Calculate the angle in radians
    angle_rad = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    # Map the angle to the range [-π, π]
    angle_mapped = (angle_rad % (2 * np.pi)) - np.pi

    # Normalize to the range [-1, 1]
    normalized_angle = angle_mapped / np.pi + 1

    return normalized_angle


# def display_text(text, size=12, keep_opened=False, x=100, y=100):
#     largeText = pygame.font.Font('freesansbold.ttf', size)
#     TextSurf = largeText.render(text, True, (0, 0, 0))
#     TextRect = TextSurf.get_rect()
#
#     TextRect.center = (550, 40)
#     display.blit(TextSurf, TextRect)
#     pygame.display.update()
#
#     if keep_opened:
#         while keep_opened:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     keep_opened = False
#                 elif event.keep_opened == pygame.KEYDOWN:
#                     keep_opened = False


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


def turn_left(direction):
    left = [2, 3, 1, 0]
    return left[direction]


def turn_right(direction):
    right = [3, 2, 0, 1]
    return right[direction]


def get_dist_to_apple(snake_position, apple_position):
    snake_head = snake_position[0]
    return np.linalg.norm(np.array(snake_head) - np.array(apple_position))


def play_game(nn=None, human_controlled=True, clock_speed=10, generation=0, snake_color=(0, 120, 0), score=0):
    crashed = False
    # TODO rewrite all usages to use snake_position[0] instead of snake_head
    snake_head = [display_width / 2, display_height / 2]
    snake_position = [[display_width / 2, display_height / 2],
                      [display_width / 2 - 10, display_height / 2],
                      [display_width / 2 - 2 * 10, display_height / 2]]
    apple_position = generate_new_apple()
    previous_direction = 1
    last_out = [0, 0, 0]
    directions_changed = 0
    fitness = 0
    starting_distance = get_dist_to_apple(snake_position, apple_position)

    lastscore = score
    time_since_score_change = 0
    # Main game loop
    new_direction = previous_direction
    while crashed is not True:
        for event in (events := pygame.event.get()):

            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
            if event.type == pygame.KEYDOWN:

                # for playing the game manually
                if human_controlled:
                    if event.key == pygame.K_LEFT:
                        new_direction = 0
                    elif event.key == pygame.K_RIGHT:
                        new_direction = 1
                    elif event.key == pygame.K_DOWN:
                        new_direction = 2
                    elif event.key == pygame.K_UP:
                        new_direction = 3
                    new_direction = pick_correct_direction(previous_direction, new_direction)

                if event.key == pygame.K_SPACE:
                    paused = True
                    print("pause")
                    while paused:
                        for event in (events := pygame.event.get()):

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit(1)
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                paused = False
                                print("unpause")
        if not human_controlled:
            if score == lastscore:
                time_since_score_change += 1
                if time_since_score_change > display_width // 5:
                    crashed = True
            inp = get_inputs(snake_position, apple_position)
            out = nn.evaluate(inp)
            if out != last_out:
                directions_changed += 1
            debug = True
            if debug and snake_color != (0, 120, 0):
                print(out)
            decision = np.argmax(out)
            if decision == 0:
                new_direction = previous_direction
            elif decision == 1:
                new_direction = turn_left(previous_direction)
            else:
                new_direction = turn_right(previous_direction)
        display.fill(window_color)
        draw_apple(display, apple_position)
        draw_snake(snake_position, snake_color)
        snake_position, apple_position, score = move_snake(snake_head, snake_position, apple_position,
                                                           new_direction, score)
        if lastscore != score:
            # Snake ate an apple
            fitness += 50000
            lastscore = score

        pygame.display.set_caption(f"SCORE: {score}, Gen {generation}, ch:{directions_changed}")
        pygame.display.update()

        previous_direction = new_direction

        if snake_hit_obstacle(snake_position):
            fitness -= 1000
            crashed = True

        clock.tick(clock_speed)

    end_distance = get_dist_to_apple(snake_position, apple_position)

    fitness += (starting_distance - end_distance) * 10

    return score, fitness
