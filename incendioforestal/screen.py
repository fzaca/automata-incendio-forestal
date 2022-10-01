import sys
import pygame as pg
import pygame_gui as pg_gui
from pygame.locals import QUIT
from automata import Automata

WIDTH = 1000
HEIGHT = 400
FPS = 60

#Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY1 = (68,68,68)
GRAY2 = (38,38,38)
GRAY3 = (100, 100, 100)
LBLUE = (95,203,255)
RPINK = (254,44,84)
GREEN = (0,255,128)

class Game_Screen:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.manager = pg_gui.UIManager((WIDTH, HEIGHT), 'data/theme.json')
        pg.display.set_caption(" ")

        self.automata = Automata()
        self.setup_gui()

        self.delay = 0
        self.is_running = False

    def run(self):
        clock = pg.time.Clock()
        run = True
        while run:
            self.screen.fill(GRAY1)
            time_delta = clock.tick(60)/1000.0
            for event in pg.event.get():
                if event.type == QUIT:
                    run = False

                if event.type == pg_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.play_button:
                        if self.is_running:
                            self.is_running = False 
                            self.play_button.set_text('Play')
                        else:
                            self.is_running = True
                            self.play_button.set_text('Stop')
                    if event.ui_element == self.clear_button: self.automata.clear_grid()
                    if event.ui_element == self.random_button: self.automata.noise_grid()
                    if event.ui_element == self.step_button: self.automata.update_generation()
                if event.type == pg_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.delay_slider:  self.delay = int(event.value)
                    if event.ui_element == self.burn_slider: self.automata.burn_prob = event.value
                    if event.ui_element == self.points_slider:
                        self.automata.points_of_fire = event.value
                        self.automata.noise_grid()
                if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.size_dropdown: 
                        self.automata.setSize(self.size_dropdown.selected_option)
                
                self.manager.process_events(event)
            self.manager.update(time_delta)

            self.setup_interfaze()
            if self.is_running:
                self.automata.update_generation()

            self.manager.draw_ui(self.screen) # Dibuja elementos de la gui
            pg.display.flip()
            # clock.tick(FPS) # De moment
            pg.time.delay(self.delay)

        pg.quit()

    def setup_gui(self):
        #Botones
        self.play_button = pg_gui.elements.UIButton(
            relative_rect=pg.Rect((25, 350), (250, 35)),
            text='Play', manager=self.manager)
        self.random_button = pg_gui.elements.UIButton(
            relative_rect=pg.Rect((25, 315), (100, 35)),
            text='Randomise', manager=self.manager)
        self.step_button = pg_gui.elements.UIButton(
            relative_rect=pg.Rect((130, 315), (70, 35)),
            text='+Step', manager=self.manager)
        self.clear_button = pg_gui.elements.UIButton(
            relative_rect=pg.Rect((205, 315), (70, 35)),
            text='Clear', manager=self.manager)
        
        #Grid size drow menu
        self.size_dropdown = pg_gui.elements.UIDropDownMenu(
            self.automata.options_size, self.automata.options_size[2], 
            relative_rect=pg.Rect(115, 225, 160, 35),
            manager=self.manager, expansion_height_limit=100)

        # Speed scroll bar
        self.delay_slider = pg_gui.elements.UIHorizontalSlider(
            relative_rect=pg.Rect(115, 270, 160, 25), start_value=38.0, 
            value_range=(0.0, 85.0), manager=self.manager)

        # Probabilidad de quemarse scroll bar
        self.burn_slider = pg_gui.elements.UIHorizontalSlider(
            relative_rect=pg.Rect(115, 190, 160, 25), start_value=self.automata.burn_prob, 
            value_range=(0.0, 0.99), manager=self.manager)

       # Probabilidad de que aparesca fuego scroll bar
        self.points_slider = pg_gui.elements.UIHorizontalSlider(
            relative_rect=pg.Rect(115, 155, 160, 25), start_value=self.automata.points_of_fire, 
            value_range=(0.0, 0.99), manager=self.manager) 

        # Caja de texto
        self.manager.add_font_paths("Montserrat",
                            "data/fonts/Montserrat-Regular.ttf",
                            "data/fonts/Montserrat-Bold.ttf",
                            "data/fonts/Montserrat-Italic.ttf",
                            "data/fonts/Montserrat-BoldItalic.ttf")
        self.manager.preload_fonts([
                            {'name': 'Montserrat', 'html_size': 4.5, 'style': 'bold'},
                            {'name': 'Montserrat', 'html_size': 4.5, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 2, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 2, 'style': 'italic'},
                            {'name': 'Montserrat', 'html_size': 6, 'style': 'bold'},
                            {'name': 'Montserrat', 'html_size': 6, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 6, 'style': 'bold_italic'},
                            {'name': 'Montserrat', 'html_size': 4, 'style': 'bold'},
                            {'name': 'Montserrat', 'html_size': 4, 'style': 'regular'},
                            {'name': 'Montserrat', 'html_size': 4, 'style': 'italic'}
        ])
        self.hmtl_text_1 = pg_gui.elements.UITextBox(
            '<font face=Montserrat color=regular_text><font color=#E784A2 size=4.5>'
            '<br><b><u><effect id=spin_me>Incendio Forestal</effect></u><br><br>'
            '<font color=#FFFFFF size=4.5>'
            'Automata celular aplicado a incendio forestales<br><br>'
            'Este programa utiliza la </font>'
            '<font color=#236845 size=4.5>'
            '<b><a href="https://es.wikipedia.org/wiki/Vecindad_de_Moore">vecindad de moore</a></b>'
            '</font><font color=#FFFFFF size=4.5>'
            ', Este autómata trata de forma muy simplificada la evolución de un bosque ' 
            'en el que se producen incendios, '
            'podemos observar en verde a los arboles, en rojo los puntos de fuego y en gris las cenizas.'
            '<br><br>Si un arbol tiene un punto de fuego en alguna de sus 8  celdas vecinas '
            'Tiene una probabilidad (30% por defecto) de prenderse fuego, los puntos encendidos a su '
            'vez se convierten en ceniza.'
            '<br><br></font></font>',
            pg.Rect(700, 0, 300, 400),
            manager=self.manager,
            object_id='#text_box_1')
        
        #Textos
        font1 = pg.font.SysFont('data/fonts/Montserrat-Regular.ttf', 24)
        font2 = pg.font.SysFont('data/fonts/Montserrat-Bold.ttf', 30)
        self.text2 = font1.render('Map size:', True, GRAY2)
        self.text2Rect = self.text2.get_rect()
        self.text2Rect.center = (65, 243)
        self.text3 = font1.render('Speed:', True, GRAY2)
        self.text3Rect = self.text2.get_rect()
        self.text3Rect.center = (65, 283)
        self.title1 = font2.render('Controls', True, GRAY2)
        self.title1Rect = self.text2.get_rect()
        self.title1Rect.center = (146, 44)
        self.text4 = font1.render('% Burn:', True, GRAY2)
        self.text4Rect = self.text2.get_rect()
        self.text4Rect.center = (65, 203)
        self.text5 = font1.render('% Points:', True, GRAY2)
        self.text5Rect = self.text2.get_rect()
        self.text5Rect.center = (65, 168)

    def setup_interfaze(self):
        self.draw_grid(self.automata.grid)
        pg.draw.rect(self.screen, GRAY2, (0, 0, 300, 400), 0, 0)
        pg.draw.rect(self.screen, WHITE, (10, 10, 280, 380), 0, 10)
        pg.draw.rect(self.screen, GRAY1, (25, 310, 250, 2), 0, 10) # separador
        pg.draw.rect(self.screen, GRAY1, (25, 80, 250, 2), 0, 10) # separador
        self.screen.blit(self.text2, self.text2Rect)
        self.screen.blit(self.text3, self.text3Rect)
        self.screen.blit(self.text4, self.text4Rect)
        self.screen.blit(self.text5, self.text5Rect)
        self.screen.blit(self.title1, self.title1Rect)

    def draw_grid(self, grid):
        width, height = 400, 400
        ix, iy = 300, 0
        x, y = ix, iy
        sx = width / len(grid[0])
        sy = height / len(grid)
        for row in grid:
            for col in row:
                if col == 1: pg.draw.rect(self.screen, GREEN, (x, y, sx, sy), 0, 8)
                if col == 2: pg.draw.rect(self.screen, RPINK, (x, y, sx, sy), 0, 8)
                if col == 3: pg.draw.rect(self.screen, GRAY3, (x, y, sx, sy), 0, 8)
                x += sx
            x = ix
            y += sy 