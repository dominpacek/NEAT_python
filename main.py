import random
import time

import numpy as np
import pygame

import genetic_alg


# TODO squash all commits before pushing

def generate_new_apple():
    apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
    return apple_position


def collision_with_boundaries(snake_head):
    if snake_head[0] >= 500 or snake_head[0] < 0 or snake_head[1] >= 500 or snake_head[1] < 0:
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


def draw_snake(snake_position):
    for position in snake_position:
        pygame.draw.rect(display, (0, 120, 0), pygame.Rect(position[0], position[1], 10, 10))


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

    return [get_angle_to_apple(snake_position, apple_position),
            is_left_blocked, is_front_blocked, is_right_blocked]


def get_angle_to_apple(snake_position, apple_position):
    snake_head = np.array(snake_position[0])
    direction = np.array(snake_head) - np.array(snake_position[1])

    # Calculate the vector from the snake head to the apple
    apple_vector = np.array(apple_position) - snake_head

    # Calculate the cosine of the angle between the direction and apple_vector
    dot_product = np.dot(direction, apple_vector)
    magnitude_direction = np.linalg.norm(direction)
    magnitude_apple_vector = np.linalg.norm(apple_vector)

    # Avoid division by zero
    if magnitude_direction == 0 or magnitude_apple_vector == 0:
        return 0.0

    cosine_angle = dot_product / (magnitude_direction * magnitude_apple_vector)

    # Calculate the angle in radians
    angle_rad = np.arccos(np.clip(cosine_angle, -1.0, 1.0))

    # Convert angle to the range [0, 1]
    normalized_angle = (angle_rad % (2 * np.pi)) / (2 * np.pi)

    return normalized_angle


def display_text(text, size=12, keep_opened=False, x=100, y=100):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf = largeText.render(text, True, (0, 0, 0))
    TextRect = TextSurf.get_rect()

    TextRect.center = (550, 40)
    display.blit(TextSurf, TextRect)
    pygame.display.update()

    if keep_opened:
        while keep_opened:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_opened = False
                elif event.keep_opened == pygame.KEYDOWN:
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


def play_game(nn=None, human_controlled=True, clock_speed=10, score=0):
    crashed = False
    # TODO rewrite all usages to use snake_position[0] instead of snake_head
    snake_head = [250, 250]
    snake_position = [[250, 250], [240, 250], [230, 250]]
    apple_position = generate_new_apple()
    previous_direction = 1

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
                if human_controlled:
                    if event.key == pygame.K_LEFT:
                        new_direction = 0
                    elif event.key == pygame.K_RIGHT:
                        new_direction = 1
                    elif event.key == pygame.K_DOWN:
                        new_direction = 2
                    elif event.key == pygame.K_UP:
                        new_direction = 3
                if event.key == pygame.K_SPACE:
                    paused = True
                    while paused:
                        for event in (events := pygame.event.get()):

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                exit(1)
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                paused = False
        if not human_controlled:
            if score == lastscore:
                time_since_score_change += 1
                if time_since_score_change > 2500:
                    crashed = True
            inp = get_inputs(snake_position, apple_position)
            out = nn.evaluate(inp)
            new_direction = int(''.join(map(str, out)), 2)

        new_direction = pick_correct_direction(previous_direction, new_direction)
        display.fill(window_color)
        draw_apple(display, apple_position)
        draw_snake(snake_position)
        snake_position, apple_position, score = move_snake(snake_head, snake_position, apple_position,
                                                           new_direction, score)

        pygame.display.set_caption(f"SCORE: {score}, Generation {i}")
        pygame.display.update()

        previous_direction = new_direction

        if snake_hit_obstacle(snake_position):
            crashed = True

        clock.tick(clock_speed)

    return score


if __name__ == "__main__":
    # SETUP #

    display_width = 500
    display_height = 500

    window_color = (200, 200, 200)
    clock = pygame.time.Clock()

    # todo move pygame stuff to its class
    pygame.init()  # initialize pygame modules

    display = pygame.display.set_mode((display_width, display_height))
    display.fill(window_color)
    pygame.display.update()

    # Neural network #
    generations = 2000
    population_size = 50
    start = time.time()
    inputs = 4 + 1
    population = genetic_alg.generate_new_population(population_size, inputs, 2)
    for i in range(generations):
        # Letting each genome play the game
        print()
        print(f'Generation {i}')
        max_score = 0
        avg = 0
        max_nodes = 0
        for genome in population:
            # fitness function is just score
            genome_score = play_game(genome.nn, False, 5000)

            genome.fitness = genome_score * 5000
            max_score = max(genome_score, max_score)
            avg += genome_score
            max_nodes = max(max_nodes, len(genome.nn.neurons))

        avg = avg / len(population)
        end = time.time()
        print(f'took {(end - start):.2f} seconds')
        print(f'Best score: {max_score}')
        print(f'Average score: {avg:.2f}')
        print(f'Max nodes: {max_nodes}')

        start = time.time()
        population = genetic_alg.next_generation(population)

    pygame.display.update()

    text = f'Final score: {genome_score}'
    display_text(text, 35, True, 500, 250)

    pygame.quit()
