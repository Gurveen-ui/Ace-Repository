# importing modules and creating display
import pygame
pygame.init()
Screen = pygame.display.set_mode((1280,720))

# dialogue producing method, adds letters and lines to a dilogue list over time
def dialogue_producer(Box_class, Text_constant, Letter_Speed):
    if Box_class.display_box == True:
        if Box_class.dialogue[int(Box_class.line_counter)] == Text_constant[int(Box_class.line_counter)]:
            Box_class.line_counter += 1
            Box_class.text_counter = 0
            if Box_class.line_counter >= len(Box_class.dialogue):
                Box_class.text_paused = True
        if Box_class.text_counter % 10 == 0:
            if Box_class.line_counter <= len(Box_class.dialogue) - 1:
                Box_class.dialogue[Box_class.line_counter] += Text_constant[Box_class.line_counter][int(Box_class.text_counter // 10)]
        Box_class.text_counter += Letter_Speed

# display dialogue method, displays a dialogue list with gaps between lines
def Display_Dialogue(Box_class, X_Distance, Y_Distance, Line_Spacing, Font, Box_Rect_Seperate = None):
    line_count = 0
    for line in Box_class.dialogue:
        text = Font.render(line, False, (0,0,0))
        for i in Box_class.dialogue:
            if line != Box_class.dialogue[line_count]:
                line_count += 1
        if Box_Rect_Seperate == None: Screen.blit(text,(Box_class.rect.left + X_Distance , Box_class.rect.top + Y_Distance + (line_count* Line_Spacing)))
        else: Screen.blit(text,(Box_Rect_Seperate.left + X_Distance , Box_Rect_Seperate.top + Y_Distance + (line_count* Line_Spacing)))
        line_count = 0
    if Box_class.text_paused == True:
        Box_class.pause_timer += 0.1

# fonts
Royal_Font = pygame.font.Font("Game Attempts\\Font\\citadel_of_blackrose\\Citadel of Blackrose.ttf", 30)
Royal_Font_Small = pygame.font.Font("Game Attempts\\Font\\citadel_of_blackrose\\Citadel of Blackrose.ttf", 20)
Royal_Font_X_Small = pygame.font.Font("Game Attempts\\Font\\citadel_of_blackrose\\Citadel of Blackrose.ttf", 15)
