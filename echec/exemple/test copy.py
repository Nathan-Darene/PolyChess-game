from moviepy.editor import VideoFileClip
import pygame
import numpy as np
import sys

pygame.init()

# Taille de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
clock = pygame.time.Clock()

# Charger la vidéo
video = VideoFileClip("video/6824-196344457_small.mp4")

# Convertir la première image en une surface Pygame
video_surface = pygame.image.fromstring(np.array(video.get_frame(0)).tobytes(), video.size, "RGB")

running = True
current_frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Afficher la vidéo
    fenetre.blit(video_surface, (0, 0))
    pygame.display.flip()

    # Passer à l'image suivante
    current_frame += 1
    if current_frame < video.fps * video.duration:
        video_surface = pygame.image.fromstring(np.array(video.get_frame(current_frame / video.fps)).tobytes(), video.size, "RGB")
    else:
        running = False

    clock.tick(video.fps)

pygame.quit()
sys.exit()
