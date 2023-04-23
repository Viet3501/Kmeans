import math
import random
import pygame
import numpy as np
from sklearn.cluster import KMeans
def distance(p1, p2):
    return math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2))
pygame.init()
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption('Kmeans visualization')
running = True
clock = pygame.time.Clock()

BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
BACKGROUND_PANEL = (249, 255, 230)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (255, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)
COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

font = pygame.font.SysFont('sans', 40)
font_small = pygame.font.SysFont('sans', 20)
text_plus = font.render('+', True, WHITE)
text_subtraction = font.render('-', True, WHITE)
text_run = font.render('Run', True, WHITE)
text_random = font.render('Random', True, WHITE)
text_algorithm = font.render('Algorithm', True, WHITE)
text_reset = font.render('Reset', True, WHITE)
K = 0

points = []
clusters = []
labels = []
while running:
    # End draw interface
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clock.tick(60)
    screen.fill(BACKGROUND)
    # Draw interface
    # Draw panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    # K button +
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    screen.blit(text_plus, (860, 50))
    # K button -
    pygame.draw.rect(screen, BLACK, (950, 50, 50, 50))
    screen.blit(text_subtraction, (960, 50))

    text_k = font.render('K = ' + str(K), True, BLACK)
    screen.blit(text_k, (1060, 50))

    # Run
    pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
    screen.blit(text_run, (860, 150))
    # Random
    pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
    screen.blit((text_random), (860, 250))

    # algorithm
    pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
    screen.blit((text_algorithm), (860, 450))

    # reset
    pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
    screen.blit((text_reset), (860, 550))

    # Draw mouse position when mouse is in panel
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render(('(' + str(mouse_x - 50) + ',' + str(mouse_y - 50) + ')'), True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = [mouse_x - 50, mouse_y - 50]
                points.append(point)

            # Change K button +
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                if K > 7:
                    K = 7
                if K >= len(points):
                    K = len(points)
                else:
                    K += 1
            elif 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                if K <= 0:
                    K = 0
                else:
                    K -= 1
            # Run button
            elif 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                for i in range(len(points)):
                    distances_to_clusters = []
                    for j in range(len(clusters)):
                        dis = distance(points[i], clusters[j])
                        distances_to_clusters.append(dis)
                    min_distance = min(distances_to_clusters)
                    label = distances_to_clusters.index(min_distance)
                    labels.append(label)
                for i in range(len(clusters)):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    if count != 0:
                        new_cluster_x = sum_x / count
                        new_cluster_y = sum_y / count
                        clusters[i] = [new_cluster_x, new_cluster_y]

            # random button
            elif 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                clusters = []
                labels = []
                for i in range(K):
                    random_point = [random.randint(0, 700), random.randint(0, 500)]
                    clusters.append(random_point)

            # algorithm button
            elif 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                kmeans = KMeans(n_clusters=K).fit(points)
                labels = kmeans.predict(points)
                clusters = kmeans.cluster_centers_

            # reset button
            elif 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                clusters = []
                points = []
                labels = []
                K = 0
                error = 0
    # Draw point
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, (points[i][0] + 50, points[i][1] + 50), 6)
        if labels == []:
            pygame.draw.circle(screen, WHITE, (points[i][0] + 50, points[i][1] + 50), 5)
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 5)
    # Draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (clusters[i][0] + 50, clusters[i][1] + 50), 10)

    # Calculate and draw error
    error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            error = error + distance(points[i],clusters[labels[i]])
    text_error = font.render('Error = ' + str(int(error)), True, BLACK)
    screen.blit(text_error, (860, 350))
    pygame.display.flip()
pygame.quit()
