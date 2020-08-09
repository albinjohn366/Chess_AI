import pygame

white = 'white'
black = 'black'
EMPTY = None
pygame.init()


class Chess:
    player = white
    board = []
    player_turn = False
    player_kings = None
    enemy_kings = None
    check = False
    check_path = None
    current_piece = None
    moves = []
    last_player = None
    last_move = None
    wait = 0
    over = False
    for i in range(0, 64):
        board.append(EMPTY)


# Setting screen, name and icon
size = (width, height) = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')


# Setting pieces
class Black_pieces:
    rook = pygame.image.load('black_rook.png')
    pawn = pygame.image.load('black_pawn.png')
    knight = pygame.image.load('black_knight.png')
    bishop = pygame.image.load('black_bishop.png')
    queen = pygame.image.load('black_queen.png')
    king = pygame.image.load('black_king.png')
    pieces = [rook, knight, bishop, queen, king, bishop, knight, rook]
    occupancy = []


class White_pieces:
    rook = pygame.image.load('white_rook.png')
    pawn = pygame.image.load('white_pawn.png')
    knight = pygame.image.load('white_knight.png')
    bishop = pygame.image.load('white_bishop.png')
    queen = pygame.image.load('white_queen.png')
    king = pygame.image.load('white_king.png')
    pieces = [rook, knight, bishop, queen, king, bishop, knight, rook]
    occupancy = []


# Defining actions for each pieces
def actions(coordinate, player, enemy):
    x, y = coordinate
    z = x + (y * 8)
    if Chess.board[z] == Black_pieces.rook or Chess.board[z] == \
            White_pieces.rook:
        return show_actions('rook', coordinate, player, enemy)
    elif Chess.board[z] == Black_pieces.knight or Chess.board[z] \
            == White_pieces.knight:
        return show_actions('knight', coordinate, player, enemy)
    elif Chess.board[z] == Black_pieces.bishop or Chess.board[z] == \
            White_pieces.bishop:
        return show_actions('bishop', coordinate, player, enemy)
    elif Chess.board[z] == Black_pieces.queen or Chess.board[z] == \
            White_pieces.queen:
        return show_actions('queen', coordinate, player, enemy)
    elif Chess.board[z] == Black_pieces.pawn or Chess.board[z] == \
            White_pieces.pawn:
        return show_actions('pawn', coordinate, player, enemy)
    elif Chess.board[z] == Black_pieces.king or Chess.board[z] == \
            White_pieces.king:
        return show_actions('king', coordinate, player, enemy)


# Setting Font
my_font = 'OpenSans-Regular.ttf'
small_font = pygame.font.Font(my_font, 20)
medium_font = pygame.font.Font(my_font, 28)
large_font = pygame.font.Font(my_font, 30)


# Informing the player when there is a check call
def check_poster(text, line):
    check_text = large_font.render(text, True, (255, 0, 0))
    check_text_rect = check_text.get_rect()
    check_text_rect.center = (width * (3 / 4) + 80, height * (2 / 3) - 100 +
                              line)
    screen.blit(check_text, check_text_rect)


# Checking if there is a check call
def checking_checks(coordinates, kings, enimies):
    for coordinate in coordinates:
        moves = actions(coordinate, coordinates, enimies)
        if moves:
            for move in moves:
                if kings in move:
                    Chess.check_path = move
                    return coordinate
    return 0


# Checking if a move is valid in terms of check call
def safe_spaces(players, enimies, avail_moves, kings, cell):
    moves_copy = avail_moves.copy()

    def find_diagonals(coordinate):
        i, j = coordinate
        diagonals = [(i + 1, j + 1), (i - 1, j - 1), (i + 1, j - 1), (i - 1,
                                                                      j + 1)]
        for dia in diagonals:
            x, y = dia
            z = x + (y * 8)
            if dia in enimies and (Chess.board[z] == White_pieces.pawn or
                                   Chess.board[z] == Black_pieces.pawn):
                return 1

    for move in moves_copy:
        kings_copy = kings
        if kings == cell:
            kings_copy = move
            if find_diagonals(kings_copy):
                avail_moves.remove(move)

        players_copy = players.copy()
        enimies_copy = enimies.copy()
        players_copy.remove(cell)
        players_copy.append(move)
        if move in enimies_copy:
            enimies_copy.remove(move)

        if checking_checks(enimies_copy, kings_copy, players_copy) and move \
                in avail_moves:
            avail_moves.remove(move)

    return avail_moves


def show_actions(piece, coordinate, players, enemies):
    (i, j) = coordinate
    direction_1 = []
    direction_2 = []
    direction_3 = []
    direction_4 = []
    direction_5 = []
    direction_6 = []
    direction_7 = []
    direction_8 = []
    directions = [direction_1, direction_2, direction_3, direction_4,
                  direction_5, direction_6, direction_7, direction_8]

    if piece == 'rook':
        for x in range(i + 1, 8):
            if (x, j) in players:
                break
            elif (x, j) in enemies:
                direction_1.append((x, j))
                break
            else:
                direction_1.append((x, j))
        for x in range(i - 1, -1, -1):
            if (x, j) in players:
                break
            elif (x, j) in enemies:
                direction_2.append((x, j))
                break
            else:
                direction_2.append((x, j))
        for y in range(j + 1, 8):
            if (i, y) in players:
                break
            elif (i, y) in enemies:
                direction_3.append((i, y))
                break
            else:
                direction_3.append((i, y))
        for y in range(j - 1, -1, -1):
            if (i, y) in players:
                break
            elif (i, y) in enemies:
                direction_4.append((i, y))
                break
            else:
                direction_4.append((i, y))

    if piece == 'pawn':
        if Chess.player_turn:
            if (i, j - 1) not in players and (i, j - 1) not in enemies:
                direction_1.append((i, j - 1))
                if j == 6:
                    if (i, j - 2) not in players and (i, j - 2) not in enemies:
                        direction_1.append((i, j - 2))
            if (i + 1, j - 1) in enemies:
                direction_2.append((i + 1, j - 1))
            if (i - 1, j - 1) in enemies:
                direction_3.append((i - 1, j - 1))
        else:
            if (i, j + 1) not in players and (i, j + 1) not in enemies:
                direction_1.append((i, j + 1))
                if j == 1:
                    if (i, j + 2) not in players and (i, j + 2) not in enemies:
                        direction_1.append((i, j + 2))
            if (i + 1, j + 1) in enemies:
                direction_2.append((i + 1, j + 1))
            if (i - 1, j + 1) in enemies:
                direction_3.append((i - 1, j + 1))

    if piece == 'knight':
        moves = [((i - 1), (j - 2)), ((i + 1), (j - 2)), ((i - 1), (j + 2)),
                 ((i + 1), (j + 2)), ((i - 2), (j - 1)), ((i + 2), (j - 1)),
                 ((i - 2), (j + 1)), ((i + 2), (j + 1))]
        count = 0
        for move in moves:
            x, y = move
            if 0 <= x <= 7 and 0 <= y <= 7:
                if Chess.board[x + (y * 8)] == EMPTY or move in enemies:
                    directions[count] = [(x, y)]
                    count += 1

    if piece == 'bishop':
        for x in range(1, 13):
            if 0 <= i + x < 8 and 0 <= j + x < 8:
                if (i + x, j + x) in players:
                    break
                elif (i + x, j + x) in enemies:
                    direction_1.append((i + x, j + x))
                    break
                else:
                    direction_1.append((i + x, j + x))
        for x in range(1, 13):
            if 0 <= i - x < 8 and 0 <= j - x < 8:
                if (i - x, j - x) in players:
                    break
                elif (i - x, j - x) in enemies:
                    direction_2.append((i - x, j - x))
                    break
                else:
                    direction_2.append((i - x, j - x))
        for x in range(1, 13):
            if 0 <= i - x < 8 and 0 <= j + x < 8:
                if (i - x, j + x) in players:
                    break
                elif (i - x, j + x) in enemies:
                    direction_3.append((i - x, j + x))
                    break
                else:
                    direction_3.append((i - x, j + x))
        for x in range(1, 13):
            if 0 <= i + x < 8 and 0 <= j - x < 8:
                if (i + x, j - x) in players:
                    break
                elif (i + x, j - x) in enemies:
                    direction_4.append((i + x, j - x))
                    break
                else:
                    direction_4.append((i + x, j - x))

    if piece == 'queen':
        for x in range(1, 13):
            if 0 <= i + x < 8 and 0 <= j + x < 8:
                if (i + x, j + x) in players:
                    break
                elif (i + x, j + x) in enemies:
                    direction_1.append((i + x, j + x))
                    break
                else:
                    direction_1.append((i + x, j + x))
        for x in range(1, 13):
            if 0 <= i - x < 8 and 0 <= j - x < 8:
                if (i - x, j - x) in players:
                    break
                elif (i - x, j - x) in enemies:
                    direction_2.append((i - x, j - x))
                    break
                else:
                    direction_2.append((i - x, j - x))
        for x in range(1, 13):
            if 0 <= i - x < 8 and 0 <= j + x < 8:
                if (i - x, j + x) in players:
                    break
                elif (i - x, j + x) in enemies:
                    direction_3.append((i - x, j + x))
                    break
                else:
                    direction_3.append((i - x, j + x))
        for x in range(1, 13):
            if 0 <= i + x < 8 and 0 <= j - x < 8:
                if (i + x, j - x) in players:
                    break
                elif (i + x, j - x) in enemies:
                    direction_4.append((i + x, j - x))
                    break
                else:
                    direction_4.append((i + x, j - x))

        for x in range(i + 1, 8):
            if (x, j) in players:
                break
            elif (x, j) in enemies:
                direction_5.append((x, j))
                break
            else:
                direction_5.append((x, j))
        for x in range(i - 1, -1, -1):
            if (x, j) in players:
                break
            elif (x, j) in enemies:
                direction_6.append((x, j))
                break
            else:
                direction_6.append((x, j))
        for y in range(j + 1, 8):
            if (i, y) in players:
                break
            elif (i, y) in enemies:
                direction_7.append((i, y))
                break
            else:
                direction_7.append((i, y))
        for y in range(j - 1, -1, -1):
            if (i, y) in players:
                break
            elif (i, y) in enemies:
                direction_8.append((i, y))
                break
            else:
                direction_8.append((i, y))

    if piece == 'king':
        moves = []
        for row in range(i - 1, i + 2):
            for column in range(j - 1, j + 2):
                if row == (i, j):
                    continue
                moves.append((row, column))

        for move in moves:
            x, y = move
            if 0 <= x <= 7 and 0 <= y <= 7 or move in enemies:
                if Chess.board[x + (y * 8)] == EMPTY or (x, y) in enemies:
                    direction_1.append(move)

    return directions
