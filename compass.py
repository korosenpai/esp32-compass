import serial
from time import sleep
from json import loads

import pygame
from pygame.locals import *


# initialize serial
BAUDRATE = 115200
serial_data = serial.Serial("com10", BAUDRATE)
sleep(1)

# when no data is passed
while serial_data.in_waiting == 0:
    pass

# waiting for setup to finish
while (data_packet := str(serial_data.readline(), "utf-8")) != "all set up, starting to send data...\r\n":
    print(data_packet)


# prepare pygame canvas
pygame.init()


# screen res
HEIGHT = 700
WIDTH = 1000

print(f"width: {WIDTH}, height: {HEIGHT}")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("seismometer")

FONT_SIZE = 20
FONT = pygame.font.SysFont("cascadiamonoregular", FONT_SIZE)

compass_bg = pygame.image.load("assets/compass.png")
compass_center = compass_bg.get_rect()
compass_center.center = screen.get_rect().center

compass_needle = pygame.image.load("assets/needle.png")
compass_needle = pygame.transform.scale(
    compass_needle,
    (
        compass_needle.get_width() * 0.6,
        compass_needle.get_height() * 0.6
    )
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    while serial_data.in_waiting == 0:
        pass

    # read data
    data_packet = serial_data.readline()
    data_packet = loads(str(data_packet, "utf-8"))


    screen.fill((0, 0, 0))

    screen.blit(compass_bg, compass_center)

    rotated_needle = pygame.transform.rotate(compass_needle, data_packet["heading"])
    screen.blit(
        rotated_needle,
        (
            compass_center.center[0] - int(rotated_needle.get_width() / 2),
            compass_center.center[1] - int(rotated_needle.get_height() / 2)
        )
    )



    print(data_packet)


    pygame.display.flip()
