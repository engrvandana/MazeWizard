
import pygame
import time
import math
from pygame import mixer
import pygame, sys
from tkinter import *
from tkinter import messagebox
from button import Button
import splash_screen
import cv2
#import moviepy.editor

####################Help SCREEN###############################
            
SCREEN = pygame.display.set_mode((600, 600))

pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/bg_3.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Bangers-Regular.ttf", size)

class Help:
    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            BG = pygame.image.load("assets/bg_2.jpg")
            SCREEN.fill("#189AB4")

            MENU_TEXT = get_font(80).render("How to Play?", True, "#EBE0D0")
            MENU_RECT = MENU_TEXT.get_rect(center=(320, 100))
                  
            SCREEN.blit(MENU_TEXT, MENU_RECT)

            OPTIONS_TEXT = get_font(30).render("""
                * Left click ------> create barrier""", True, "#EBE0D0")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(150, 200))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            OPTIONS_TEXT = get_font(30).render("""
                * Right click ------> erase (reset to default)""", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(210, 250))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            OPTIONS_TEXT = get_font(30).render("""
                * Shift + click ----> set starting point""", True, "#EBE0D0")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(180, 300))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            OPTIONS_TEXT = get_font(30).render("""
                * Ctrl + click -----> set end point""", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(150, 350))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_TEXT = get_font(30).render("""
                * ENTER ------------> start A* ALGORITHM""", True, "#EBE0D0")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(190, 400))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_TEXT = get_font(30).render("""
                * Escape -----------> restart board""", True, "white")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(170, 450))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)


            OPTIONS_BACK = Button(image=None, pos=(300, 560), 
                                text_input="BACK", font=get_font(75), base_color="white",
                                  hovering_color="#EBE0D0")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()

            pygame.display.update()



class Node:
    def __init__(self, row, col, width, rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.state = "Normal"
        self.color = self.get_color()
        self.width = width
        self.rows = rows
        self.G = 99999
        self.H = 99999

    def get_color(self):
        if self.state == "Normal":
            return NORMAL
        elif self.state == "Barrier":
            return BARRIER
        elif self.state == "Start":
            return START
        elif self.state == "End":
            return END
        elif self.state == "Border":
            return BORDER
        elif self.state == "Visited":
            return VISITED
        elif self.state == "Path":
            return PATH

    def get_width(self):
        return self.width

    def set_state(self, state):
        self.state = state
        self.color = self.get_color()

    def get_state(self):
        return self.state

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, nodes):
        self.neighbours = []
        # Get UP, DOWN, LEFT, RIGHT neighbours (Barriers not allowed):
        if self.row != 0 and nodes[self.row - 1][self.col].get_state() != "Barrier": # UP
            self.neighbours.append(nodes[self.row - 1][self.col]) 
        if self.row < self.rows - 1 and nodes[self.row + 1][self.col].get_state() != "Barrier": # DOWN
            self.neighbours.append(nodes[self.row + 1][self.col]) 
        if self.col != 0 and nodes[self.row][self.col - 1].get_state() != "Barrier": # LEFT
            self.neighbours.append(nodes[self.row][self.col - 1]) 
        if self.col < self.rows - 1 and nodes[self.row][self.col + 1].get_state() != "Barrier": # RIGHT
            self.neighbours.append(nodes[self.row][self.col + 1])

    def set_parent(self, node):
        self.parent = node

    def restart_G(self):
        self.G = 0

    def set_G(self):
        self.G = self.parent.G + self.distance_to(self.parent)

    def set_H(self, node):
        self.H = self.distance_to(node) 

    def set_F(self):
        self.F = self.G + self.H

    def distance_to(self, node):
        x2, y2 = node.get_coords()
        return (abs(self.x - x2) + abs(self.y - y2)) 

    def get_coords(self):
        return self.x, self.y

class A_star:
    
    def a_star(draw, start_node, end_node, nodes):
        borders = []
        visited = []
        finished = False
        start_node.set_parent(start_node)
        start_node.restart_G()
        start_node.set_H(end_node)
        start_node.set_F()
        borders.append(start_node)
        iteration = 0
        while len(borders) != 0 and not finished:
            draw()
            iteration += 1
            borders.sort(key = lambda x: x.F, reverse=True)
            node = borders.pop()
            visited.append(node)
            node.set_state("Visited")
            print("Iteration:", iteration)
            print("Node G:", node.G)
            print("Node H:", node.H)
            print("Node F:", node.F)
            print("")
            result=0
            if node == end_node:
                finished = True
                result=1
                #draw backwards path
                A_star.draw_path(end_node, start_node)
            else:
                node.update_neighbours(nodes)
                for neighbour in node.neighbours:
                    if neighbour not in visited and neighbour not in borders:
                        neighbour.set_parent(node)
                        neighbour.set_G()
                        neighbour.set_H(end_node)
                        neighbour.set_F()
                        neighbour.set_state("Border")
                        borders.append(neighbour)
            draw()

        if not finished:
            result=0
            start_node.set_state("Start")
            end_node.set_state("End")
            pygame.time.wait(800)
            draw()
            print("No solution found")
            A_star.playmusic('lost.mp3')
            messagebox.showwarning("Maze Wizard","No Solution found")

        if result==1:
             A_star.playmusic('success.mp3')
             messagebox.showinfo("Maze Wizard","Solution found")


    def draw_path(end_node, start_node):
        not_found = True
        node = end_node.parent
        end_node.set_state("End")

        while not_found:
            if node == start_node:
                print("found start_node")
                not_found = False
                node.set_state("Start")
            else:
                node.set_state("Path")
                node = node.parent



    def make_nodes(rows, width):
        nodes = []
        size = width // rows
        for y in range(rows):
            nodes.append([])
            for x in range(rows):
                node = Node(y, x, size, rows)
                nodes[y].append(node)
        return nodes


    def restart_nodes_state(state, nodes):
        for row_of_nodes in nodes:
            for node in row_of_nodes:
                if node.get_state() == state:
                    node.set_state("Normal")                    


    def draw_board(win, rows, width):
        gap = width // rows
        for x in range(1, rows):
            pygame.draw.line(win, LINE_COLOR, (gap*x, 0), (gap*x, width), 2) # Last item == line.weight = 1 by default
        for y in range(1, rows):
            pygame.draw.line(win, LINE_COLOR, (0, gap*y), (width, gap*y), 2)


    def draw_nodes(win, nodes):
        for row_of_nodes in nodes:
            for node in row_of_nodes:
                    node.draw(win)


    def get_pos(posXY, width, rows):
        pos_x, pos_y = posXY
        node_width = width // rows
        x = pos_x // node_width
        y = pos_y // node_width
        return x, y

    def draw(win, rows, width, nodes):
       A_star.draw_nodes(win, nodes)
       A_star.draw_board(win, rows, width)
       pygame.display.update()
    def playmusic(music):
       mixer.init()  
    # Loading the song
       mixer.music.load(music)
    # Setting the volume
       mixer.music.set_volume(0.7)
    # Start playing the song
       mixer.music.play()
       pygame.time.wait(1500)
       mixer.music.stop()
    def main(win, width, rows):
        # List of nodes
        nodes = A_star.make_nodes(rows, width)
        running = True
        nodes[0][0].set_state('Start')
        start = nodes[0][0]
        nodes[9][9].set_state('End')
        end = nodes[9][9]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_ESCAPE: # ESCAPE --> RESTART BOARD
                         nodes = A_star.make_nodes(rows, width)
                         nodes[0][0].set_state('Start')
                         start = nodes[0][0]
                         nodes[9][9].set_state('End')
                         end = nodes[9][9]
                    if event.key == pygame.K_HOME:
                          main_menu()
                         
                        

                    if event.key == pygame.K_RETURN: # ENTER --> START A* ALGORITHM
                        print("Enter pressed")
                        A_star.a_star(lambda: A_star.draw(win, rows, width, nodes), start, end, nodes)
                     

                elif pygame.mouse.get_pressed()[0]: # click  --> BARRIERS
                        x, y = A_star.get_pos(pygame.mouse.get_pos(), width, rows)
                        if nodes[y][x] != nodes[0][0] and nodes[y][x] != nodes[9][9]:
                            state = "Barrier"
                            nodes[y][x].set_state(state)
                elif pygame.mouse.get_pressed()[2]: # RIGHT click --> ERASER
                    x, y = A_star.get_pos(pygame.mouse.get_pos(), width, rows)
                    state = "Normal"
                    # Extends eraser surface
                    for i in range (-1, 2):
                        for j in range (-1 ,2):
                            try:
                                nodes[y+i][x+j].set_state(state)
                            except:
                                nodes[y][x].set_state(state)
         
            # DRAWING
            A_star.draw(win, rows, width, nodes)



def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))


        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("Main Menu", True, "#D4F1F4")
        MENU_RECT = MENU_TEXT.get_rect(center=(320, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(320, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#75E6DA",
                             hovering_color="#EBE0D0")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(320, 400), 
                            text_input="HELP", font=get_font(60), base_color="#75E6DA",
                                hovering_color="#EBE0D0")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(320, 550), 
                            text_input="QUIT", font=get_font(60), base_color="#75E6DA",
                             hovering_color="#EBE0D0")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                   
                    A_star.main (WIN, WIDTH, ROWS)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    h = Help()
                    h.options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


pygame.init()
SPLASH= (8, 95, 99)
SPLASHtxt=(250, 207, 90)
WHITE=(255,255,255)

### ENVIRONMENT
WIDTH = 600
HEIGHT = WIDTH
ROWS = 10

### PYGAME WINDOW
WIN = pygame.display.set_mode(( WIDTH, HEIGHT))
pygame.display.set_caption("A* from scratch")

# COLORS
LINE_COLOR = (100, 100, 100)
NORMAL = (250,  250, 240) 
BARRIER = (20, 20, 20)
START = (250,0,0)
END = (255,170,0)
BORDER = (87,135,90)
VISITED = (110,175,85)
PATH = (186, 205, 0)
WIN.fill(END)





    
sp=splash_screen.Sp_Screen()
sp.show_splash_screen()
main_menu()
