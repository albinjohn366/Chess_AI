from ai_opponent import *
import pygame
import time
import datetime
import sys


# Displaying the game position
def game_controller(text, line, color):
    control_text = medium_font.render(text, True, color)
    control_text_rect = control_text.get_rect()
    control_text_rect.center = (width * (3 / 4) + 80, height * (2 / 3) - 100 +
                                line)
    screen.blit(control_text, control_text_rect)


# Setting pieces in position
def positions():
    if Chess.player == black:
        for num, i in enumerate(range(56, 64)):
            Chess.board[i] = Black_pieces.pieces[num]
            Chess.board[i - 8] = Black_pieces.pawn
            Chess.board[num] = White_pieces.pieces[num]
            Chess.board[num + 8] = White_pieces.pawn
            Chess.enemy_kings = (4, 0)
            Chess.player_kings = (4, 7)
            Black_pieces.occupancy.append((num, 7))
            Black_pieces.occupancy.append((num, 6))
            White_pieces.occupancy.append((num, 0))
            White_pieces.occupancy.append((num, 1))
    if Chess.player == white:
        for num, i in enumerate(range(56, 64)):
            Chess.board[i] = White_pieces.pieces[num]
            Chess.board[i - 8] = White_pieces.pawn
            Chess.board[num] = Black_pieces.pieces[num]
            Chess.board[num + 8] = Black_pieces.pawn
            Chess.enemy_kings = (4, 0)
            Chess.player_kings = (4, 7)
            White_pieces.occupancy.append((num, 7))
            White_pieces.occupancy.append((num, 6))
            Black_pieces.occupancy.append((num, 0))
            Black_pieces.occupancy.append((num, 1))


# Colors
WHITE = (255, 255, 255)
IVORY = (255, 255, 240)
BLACK = (0, 0, 0)
GREY = (125, 125, 125)
CHOCOLATE = (210, 105, 30)

# Setting variables
cells = dict()
origin = 10
cell_size = (height - 20) / 8
player_option = True
hints = []

# Hint dot image
hint = pygame.transform.scale(pygame.image.load('hint.png'), (20, 20))

while True:

    # Setting bg color
    screen.fill(BLACK)

    # To end the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    if player_option:

        # Setting instruction text
        instruction_text = large_font.render('Play Chess', True, WHITE)
        instruction_text_rect = instruction_text.get_rect()
        instruction_text_rect.center = (width / 2, height / 4)
        screen.blit(instruction_text, instruction_text_rect)

        # Setting player button
        fp_sentence_x = medium_font.render('Play as White', True, BLACK)
        fp_sentence_0 = medium_font.render('Play as Black', True, BLACK)
        fp_sentence_x_rect = fp_sentence_x.get_rect()
        fp_sentence_0_rect = fp_sentence_0.get_rect()
        fp_sentence_x_box = pygame.Rect(70, height * (2 / 4), 200, 70)
        fp_sentence_0_box = pygame.Rect(width - 270, height * (2 / 4), 200, 70)
        fp_sentence_x_rect.center = fp_sentence_x_box.center
        fp_sentence_0_rect.center = fp_sentence_0_box.center

        pygame.draw.rect(screen, WHITE, fp_sentence_x_box)
        pygame.draw.rect(screen, WHITE, fp_sentence_0_box)
        screen.blit(fp_sentence_x, fp_sentence_x_rect)
        screen.blit(fp_sentence_0, fp_sentence_0_rect)

        # Checking if buttons are pressed
        mouse = pygame.mouse.get_pressed()
        left, _, _ = mouse

        # Checking which button is pressed
        if left == 1:
            position = pygame.mouse.get_pos()
            if fp_sentence_0_box.collidepoint(position[0], position[1]):
                Chess.player = black
                player_option = False
                positions()
                time.sleep(0.3)
            elif fp_sentence_x_box.collidepoint(position[0], position[1]):
                Chess.player = white
                Chess.player_turn = True
                player_option = False
                positions()
                time.sleep(0.3)
        pygame.display.update()
        continue

    # Drawing the border
    outline = pygame.Rect(5, 5, height - 10, height - 10)
    pygame.draw.rect(screen, (51, 25, 0), outline, 10)

    # Drawing the cells
    if Chess.player == white:
        color = (255, 176, 102)
        non_color = (102, 51, 0)
    else:
        color = (102, 51, 0)
        non_color = (255, 176, 102)

    for x in range(0, 64):
        i = x % 8
        j = int(x / 8)
        if (i + j) % 2 == 0:
            cells[(i, j)] = pygame.Rect(origin + (i * cell_size), origin +
                                        (j * cell_size), cell_size,
                                        cell_size)
            pygame.draw.rect(screen, color, cells[(i, j)])
            if (i, j) == Chess.last_player or (i, j) == Chess.last_move:
                pygame.draw.rect(screen, (255, 0, 0), cells[(i, j)], 3)
            if Chess.board[x]:
                screen.blit(Chess.board[x], cells[(i, j)])
            if (i, j) in hints:
                hint_rect = hint.get_rect()
                hint_rect.center = cells[(i, j)].center
                screen.blit(hint, hint_rect)
        else:
            cells[(i, j)] = pygame.Rect(origin + (i * cell_size), origin +
                                        (j * cell_size), cell_size,
                                        cell_size)
            pygame.draw.rect(screen, non_color, cells[(i, j)])
            if (i, j) == Chess.last_player or (i, j) == Chess.last_move:
                pygame.draw.rect(screen, (255, 0, 0), cells[(i, j)], 3)
            if Chess.board[x]:
                screen.blit(Chess.board[x], cells[(i, j)])
            if (i, j) in hints:
                hint_rect = hint.get_rect()
                hint_rect.center = cells[(i, j)].center
                screen.blit(hint, hint_rect)

    # Checking if it is the players turn
    position = pygame.mouse.get_pos()
    # Checking if the player is white or black and allotting the pieces
    if Chess.player == white:
        player_occupancy = White_pieces.occupancy
        enemy_occupancy = Black_pieces.occupancy
    else:
        player_occupancy = Black_pieces.occupancy
        enemy_occupancy = White_pieces.occupancy

    if Chess.over:
        if Chess.check:
            if Chess.player_turn:
                check_poster('CHECK', 70)
                check_poster('MATE', 100)
                check_poster('YOU', 170)
                check_poster('LOST', 200)
            else:
                check_poster('CHECK', 70)
                check_poster('MATE', 100)
                check_poster('YOU', 170)
                check_poster('WON', 200)
        else:
            check_poster('TIE', 100)
        pygame.display.update()

    elif Chess.check:
        check_poster('CHECK', -100)

    if Chess.player_turn:
        # Finding the moves available for each player
        Chess.moves = []
        for player in player_occupancy:
            moves = []
            for item in actions(player, player_occupancy, enemy_occupancy):
                moves += item
            if not moves:
                continue
            if Chess.check and player != Chess.player_kings:
                Chess.check_path.append(Chess.check)
                moves = set.intersection(set(moves), set(Chess.check_path))

            moves = safe_spaces(player_occupancy, enemy_occupancy,
                                moves, Chess.player_kings, player)

            for move in moves:
                Chess.moves.append((player, move))

        game_controller('Your Turn', 10, WHITE)
        if not Chess.moves and Chess.check:
            Chess.over = True

        if not Chess.moves and not Chess.check:
            Chess.over = True

        # Checking if a piece is selected to move
        available_moves = []
        left, _, _ = pygame.mouse.get_pressed()
        if left == 1:
            hints = []
            for piece in player_occupancy:
                if cells[piece].collidepoint(position[0], position[1]):
                    Chess.current_piece = piece

            # Checking which move is selected for the particular piece
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                position = pygame.mouse.get_pos()

                for player_move in Chess.moves:
                    if player_move[0] == Chess.current_piece:
                        hints.append(player_move[1])

                x, y = Chess.current_piece
                z = x + (y * 8)
                for cell in hints:
                    if cells[cell].collidepoint(position[0], position[1]):
                        a, b = cell
                        c = a + (b * 8)
                        if (x, y) == Chess.player_kings:
                            Chess.player_kings = cell
                        elif Chess.board[z] == Black_pieces.pawn:
                            if Chess.current_piece[1] == 1:
                                Chess.board[c] = Black_pieces.queen
                        elif Chess.board[z] == White_pieces.pawn:
                            if Chess.current_piece[1] == 1:
                                Chess.board[c] = White_pieces.queen
                        player_occupancy.append(cell)
                        if cell in enemy_occupancy:
                            enemy_occupancy.remove(cell)
                        player_occupancy.remove(Chess.current_piece)
                        Chess.last_player = Chess.current_piece
                        Chess.last_move = cell
                        Chess.board[c] = Chess.board[z]
                        Chess.board[z] = EMPTY
                        hints.clear()
                        time.sleep(0.1)
                        Chess.check = checking_checks(player_occupancy,
                                                      Chess.enemy_kings,
                                                      enemy_occupancy)
                        Chess.player_turn = False
    else:
        if Chess.wait < 4:
            Chess.wait += 1
            game_controller('Computer', 10, WHITE)
            game_controller('Thinking...', 50, WHITE)
        else:
            (player, move) = find_best_move(enemy_occupancy,
                                            player_occupancy)
            if (player == 100 and move == 100) or (player == 101 and move ==
                                                   100):
                Chess.over = True
                continue
            if player == Chess.enemy_kings:
                Chess.enemy_kings = move
            enemy_occupancy.append(move)
            if move in player_occupancy:
                player_occupancy.remove(move)
            x, y = move
            a, b = player
            z = x + (y * 8)
            c =a + (b * 8)
            enemy_occupancy.remove(player)
            Chess.board[z] = Chess.board[c]
            Chess.board[c] = EMPTY
            time.sleep(0.1)
            Chess.check = checking_checks(enemy_occupancy,
                                          Chess.player_kings,
                                          player_occupancy)
            Chess.player_turn = True
            Chess.last_player = player
            Chess.last_move = move
            Chess.wait = 0

    pygame.display.update()
