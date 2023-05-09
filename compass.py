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

FONT_SIZE = 60
FONT = pygame.font.SysFont("cascadiamonoregular", FONT_SIZE)

compass_bg = pygame.image.load("assets/compass.png")

compass_center = compass_bg.get_rect()
compass_center.center = screen.get_rect().center
compass_center.move_ip(0, FONT_SIZE) # translate compass down to make space for text

compass_needle = pygame.image.load("assets/needle.png")
compass_needle = pygame.transform.scale(
    compass_needle,
    (
        compass_needle.get_width() * 0.6,
        compass_needle.get_height() * 0.6
    )
)

def degrees_to_heading(degrees):
        heading = ""
        if (degrees > 337) or (degrees >= 0 and degrees <= 22):
                heading = "N " # leave spaces for better formatting when printing font
        if degrees >22 and degrees <= 67:
            heading = "NE"
        if degrees >67 and degrees <= 112:
            heading = "E "
        if degrees >112 and degrees <= 157:
            heading = "SE"
        if degrees > 157 and degrees <= 202:
            heading = "S "
        if degrees > 202 and degrees <= 247:
            heading = "SW"
        if degrees > 247 and degrees <= 292:
            heading = "W "
        if degrees > 292 and degrees <= 337:
            heading = "NW"
        return heading

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

    rotated_needle = pygame.transform.rotate(compass_needle, 360 - data_packet["heading"])
    screen.blit(
        rotated_needle,
        (
            compass_center.center[0] - int(rotated_needle.get_width() / 2),
            compass_center.center[1] - int(rotated_needle.get_height() / 2)
        )
    )

    # print font
    screen.blit(
        FONT.render(
            f"{degrees_to_heading(data_packet['heading'])}: {data_packet['heading']}°", True, (255, 255, 255)
        ),
        (FONT_SIZE, FONT_SIZE)
    )



    print(data_packet)


    pygame.display.flip()
