from chess_play import *


class Minmax:
    check = None
    last_score = None
    threshold = 0
    count = 0


def move_ordering(from_to, players, enimies):
    ordered_moves = []
    for player, move in from_to:
        players_copy = list(players)
        enimies_copy = list(enimies)
        board = list(Chess.board)

        p1, p2 = player
        m1, m2 = move
        m = m1 + (m2 * 8)
        p = p1 + (p2 * 8)
        players_copy.remove(player)
        players_copy.append(move)
        if move in enimies:
            enimies_copy.remove(move)
        Chess.board[m] = Chess.board[p]
        Chess.board[p] = EMPTY
        ordered_moves.append(
            (evaluate(players_copy, enimies_copy), (player, move)))
        Chess.board = list(board)
    ordered_moves = sorted(ordered_moves)
    ordered_moves.reverse()

    moves_in_order = []
    for item in ordered_moves:
        moves_in_order.append(item[1])
    return moves_in_order


def evaluate(players, enimies):
    # Defining values for each piece
    values = (('rook',
               (50.0, 50.0, 50.0, 50.5, 50.5, 50.0, 50.0, 50.0, 49.5, 50.0,
                50.0, 50.0, 50.0, 50.0, 50.0, 49.5, 49.5, 50.0, 50.0, 50.0,
                50.0, 50.0, 50.0, 49.5, 49.5, 50.0, 50.0, 50.0, 50.0, 50.0,
                50.0, 49.5, 49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5,
                49.5, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 49.5, 50.5, 51.0,
                51.0, 51.0, 51.0, 51.0, 51.0, 50.5, 50.0, 50.0, 50.0, 50.0,
                50.0, 50.0, 50.0, 50.0)),
              ('knight',
               (32.0, 33.0, 31.0, 30.0, 30.0, 31.0, 33.0, 32.0, 32.0, 32.0,
                30.0,
                30.0, 30.0, 30.0, 32.0, 32.0, 29.0, 28.0, 28.0, 28.0, 28.0,
                28.0,
                28.0, 29.0, 28.0, 27.0, 27.0, 26.0, 26.0, 27.0, 27.0, 28.0,
                27.0,
                26.0, 26.0, 25.0, 25.0, 26.0, 26.0, 27.0, 27.0, 26.0, 26.0,
                25.0,
                25.0, 26.0, 26.0, 27.0, 27.0, 26.0, 26.0, 25.0, 25.0, 26.0,
                26.0,
                27.0, 27.0, 26.0, 26.0, 25.0, 25.0, 26.0, 26.0, 27.0)),
              ('bishop',
               (
                   28.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0, 29.0, 30.5,
                   30.0,
                   30.0, 30.0, 30.0, 30.5, 29.0, 29.0, 31.0, 31.0, 31.0, 31.0,
                   31.0,
                   31.0, 29.0, 29.0, 30.0, 31.0, 31.0, 31.0, 31.0, 30.0, 29.0,
                   29.0,
                   30.5, 30.5, 31.0, 31.0, 30.5, 30.5, 29.0, 29.0, 30.0, 30.5,
                   31.0,
                   31.0, 30.5, 30.0, 29.0, 29.0, 30.0, 30.0, 30.0, 30.0, 30.0,
                   30.0,
                   29.0, 28.0, 29.0, 29.0, 29.0, 29.0, 29.0, 29.0, 28.0)),
              ('queen',
               (
                   88.0, 89.0, 89.0, 89.5, 89.5, 89.0, 89.0, 88.0, 89.0, 90.0,
                   90.0,
                   90.0, 90.0, 90.5, 90.0, 89.0, 89.0, 90.0, 90.5, 90.5, 90.5,
                   90.5,
                   90.5, 89.0, 89.5, 90.0, 90.5, 90.5, 90.5, 90.5, 90.0, 90.0,
                   89.5,
                   90.0, 90.5, 90.5, 90.5, 90.5, 90.0, 89.5, 89.0, 90.0, 90.5,
                   90.5,
                   90.5, 90.5, 90.0, 89.0, 89.0, 90.0, 90.0, 90.0, 90.0, 90.0,
                   90.0,
                   89.0, 88.0, 89.0, 89.0, 89.5, 89.5, 89.0, 89.0, 88.0)),
              ('king',
               (2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0, 2.0, 2.0, 0.0, 0.0, 0.0,
                0.0, 2.0, 2.0, -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
                -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0, -3.0, -4.0,
                -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, -3.0, -4.0, -4.0, -5.0,
                -5.0, -4.0, -4.0, -3.0, -3.0, -4.0, -4.0, -5.0, -5.0, -4.0,
                -4.0, -3.0, -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0)),
              ('pawn',
               (
                   10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.5, 11.0,
                   11.0,
                   8.0, 8.0, 11.0, 11.0, 10.5, 10.5, 9.5, 9.0, 10.0, 10.0, 9.0,
                   9.5,
                   10.5, 10.0, 10.0, 10.0, 12.0, 12.0, 10.0, 10.0, 10.0, 10.5,
                   10.5,
                   11.0, 12.5, 12.5, 11.0, 10.5, 10.5, 11.0, 11.0, 12.0, 13.0,
                   13.0,
                   12.0, 11.0, 11.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0,
                   15.0,
                   10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0)))

    player_score = 0
    enemy_score = 0
    annotations = {Black_pieces.rook: 'rook', White_pieces.rook: 'rook',
                   Black_pieces.knight: 'knight', White_pieces.knight: 'knight',
                   Black_pieces.bishop: 'bishop', White_pieces.bishop: 'bishop',
                   Black_pieces.queen: 'queen', White_pieces.queen: 'queen',
                   Black_pieces.king: 'king', White_pieces.king: 'king',
                   Black_pieces.pawn: 'pawn', White_pieces.pawn: 'pawn'}

    for player in players:
        x, y = player
        z = x + (y * 8)
        piece = Chess.board[z]
        text = annotations[piece]
        for item in values:
            if text in item:
                score = item[1][z]
                player_score += score
                break
    for enemy in enimies:
        x, y = enemy
        z = x + (y * 8)
        piece = Chess.board[z]
        text = annotations[piece]
        for item in values:
            if text in item:
                score = item[1][63 - z]
                enemy_score += score
                break
    return player_score - enemy_score


# Using minimax algorithm
def minimax(players, enimies, player_kings, enemy_kings, maximum,
            depth, alpha, beta, board):
    if depth == 0:
        result = evaluate(players, enimies)
        return result

    if maximum:
        best_score = -4000
        player_moves = []

        for player in players:
            moves = []
            for item in actions(player, players, enimies):
                moves += item
            if not moves:
                continue
            if Minmax.check and player != player_kings:
                Chess.check_path.append(Minmax.check)
                moves = set.intersection(set(moves), set(Chess.check_path))

            moves = safe_spaces(players, enimies,
                                moves, player_kings, player)

            for move in moves:
                player_moves.append((player, move))

        if not player_moves and Minmax.check:
            return -1000 - depth

        if not player_moves and not Minmax.check:
            return 0

        if len(enimies) == 1:
            if Minmax.check:
                return -500 - depth

        player_moves = move_ordering(player_moves, players, enimies)
        for player, move in player_moves:
            players_copy = list(players)
            enimies_copy = list(enimies)
            player_kings_copy = player_kings
            enemy_kings_copy = enemy_kings
            board_copy = list(board)

            if player == player_kings:
                player_kings_copy = move
            players_copy.append(move)
            players_copy.remove(player)
            if move in enimies:
                enimies_copy.remove(move)

            x, y = move
            a, b = player
            z = x + (y * 8)
            c = a + (b * 8)
            board_copy[z] = board_copy[c]
            board_copy[c] = EMPTY

            Chess.board = list(board_copy)
            Minmax.check = checking_checks(players_copy,
                                           enemy_kings_copy,
                                           enimies_copy)

            # Calling minimax function
            score = minimax(players_copy, enimies_copy,
                            player_kings_copy, enemy_kings_copy, False,
                            depth - 1,
                            alpha, beta, board_copy)

            Chess.board = list(board)

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break

        return best_score

    else:
        best_score = 4000
        enemy_moves = []

        for enemy in enimies:
            Chess.player_turn = True
            moves = []
            for item in actions(enemy, enimies, players):
                moves += item
            Chess.player_turn = False
            if not moves:
                continue
            if Minmax.check and enemy != enemy_kings:
                Chess.check_path.append(Minmax.check)
                moves = set.intersection(set(moves), set(Chess.check_path))
            moves = safe_spaces(enimies, players,
                                moves, enemy_kings, enemy)
            for move in moves:
                enemy_moves.append((enemy, move))

        if not enemy_moves and Minmax.check:
            return 1000 - depth

        if not enemy_moves and not Minmax.check:
            return 0

        if len(players) == 1:
            if Minmax.check:
                return 500 - depth

        enemy_moves = move_ordering(enemy_moves, enimies, players)
        for enemy, move in enemy_moves:
            players_copy = players.copy()
            enimies_copy = enimies.copy()
            player_kings_copy = player_kings
            enemy_kings_copy = enemy_kings
            board_copy = list(board)

            if enemy == enemy_kings:
                enemy_kings_copy = move
            enimies_copy.append(move)
            enimies_copy.remove(enemy)
            if move in players:
                players_copy.remove(move)

            x, y = move
            a, b = enemy
            z = x + (y * 8)
            c = a + (b * 8)

            board_copy[z] = board_copy[c]
            board_copy[c] = EMPTY

            Chess.board = list(board_copy)
            Chess.player_turn = True
            Minmax.check = checking_checks(enimies_copy,
                                           player_kings_copy,
                                           players_copy)
            Chess.player_turn = False

            # Calling minimax function
            score = minimax(players_copy, enimies_copy,
                            player_kings_copy, enemy_kings_copy, True,
                            depth - 1, alpha, beta, board_copy)
            Chess.board = list(board)

            best_score = min(best_score, score)
            beta = min(beta, score)

            if beta <= alpha:
                break

        return best_score


def find_best_move(players, enimies):
    Minmax.count += 1
    best_score = -4000
    best_player = (1, 1)
    best_move = (1, 2)
    player_kings = Chess.enemy_kings
    enemy_kings = Chess.player_kings
    alpha = -4000
    beta = 4000
    depth = 2
    board = list(Chess.board)

    player_moves = []
    for player in players:
        moves = []
        for item in actions(player, players, enimies):
            moves += item
        if not moves:
            continue
        if Chess.check and player != player_kings:
            Chess.check_path.append(Chess.check)
            moves = set.intersection(set(moves), set(Chess.check_path))

        moves = safe_spaces(players, enimies,
                            moves, player_kings, player)

        for move in moves:
            player_moves.append((player, move))

    if not player_moves and Chess.check:
        over = (100, 100)
        return over

    if not player_moves and not Chess.check:
        over = (101, 101)
        return over

    player_moves = move_ordering(player_moves, players, enimies)
    for num, (player, move) in enumerate(player_moves):
        players_copy = list(players)
        enimies_copy = list(enimies)
        player_kings_copy = player_kings
        enemy_kings_copy = enemy_kings
        board_copy = list(board)

        if player == player_kings:
            player_kings_copy = move
        players_copy.append(move)
        players_copy.remove(player)
        if move in enimies:
            enimies_copy.remove(move)

        x, y = move
        a, b = player
        c = a + (b * 8)
        z = x + (y * 8)
        board_copy[z] = board_copy[c]
        board_copy[c] = EMPTY

        Chess.board = list(board_copy)
        Minmax.check = checking_checks(players_copy,
                                       enemy_kings_copy,
                                       enimies_copy)

        if Minmax.count > 10:
            if num < 4:
                depth = 4
            elif num == 3:
                depth = 3
            else:
                depth = 2

        # Calling minimax function
        score = minimax(players_copy, enimies_copy,
                        player_kings_copy, enemy_kings_copy, False, depth,
                        alpha, beta, board_copy)

        Chess.board = list(board)

        if best_score < score:
            best_score = score
            best_player = player
            best_move = move
    result = (best_player, best_move)
    return result
