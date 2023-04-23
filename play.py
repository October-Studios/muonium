""" Play Logic

This script spins up a web interface on the local machine at port 5000 that
allows the user to interact with the AI.
"""
import chess
import chess.svg
import chess.polyglot
import time
import traceback
import chess.pgn
import chess.engine
from flask import Flask, Response, request
import webbrowser

# Evaluating the board
pawn_table = [0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 10, -20, -20, 10, 10, 5, 5, -5,
              -10, 0, 0, -10, -5, 5, 0, 0, 0, 20, 20, 0,
              0, 0, 5, 5, 10, 25, 25, 10, 5, 5, 10, 10, 20, 30, 30, 20, 10, 10,
              50, 50, 50, 50, 50, 50, 50, 50, 0, 0, 0,
              0, 0, 0, 0, 0]

knights_table = [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20, 0, 5, 5, 0,
                 -20, -40, -30, 5, 10, 15, 15, 10, 5, -30,
                 -30, 0, 15, 20, 20, 15, 0, -30, -30, 5, 15, 20, 20, 15, 5, -30,
                 -30, 0, 10, 15, 15, 10, 0, -30, -40,
                 -20, 0, 0, 0, 0, -20, -40, -50, -40, -30, -30, -30, -30, -40,
                 -50]

bishops_table = [-20, -10, -10, -10, -10, -10, -10, -20, -10, 5, 0, 0, 0, 0, 5,
                 -10, -10, 10, 10, 10, 10, 10, 10, -10,
                 -10, 0, 10, 10, 10, 10, 0, -10, -10, 5, 5, 10, 10, 5, 5, -10,
                 -10, 0, 5, 10, 10, 5, 0, -10, -10, 0, 0,
                 0, 0, 0, 0, -10, -20, -10, -10, -10, -10, -10, -10, -20]

rooks_table = [0, 0, 0, 5, 5, 0, 0, 0, -5, 0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0,
               0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, -5,
               0, 0, 0, 0, 0, 0, -5, -5, 0, 0, 0, 0, 0, 0, -5, 5, 10, 10, 10,
               10, 10, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0]

queens_table = [-20, -10, -10, -5, -5, -10, -10, -20, -10, 0, 0, 0, 0, 0, 0,
                -10, -10, 5, 5, 5, 5, 5, 0, -10, 0, 0, 5, 5,
                5, 5, 0, -5, -5, 0, 5, 5, 5, 5, 0, -5, -10, 0, 5, 5, 5, 5, 0,
                -10, -10, 0, 0, 0, 0, 0, 0, -10, -20, -10,
                -10, -5, -5, -10, -10, -20]

kings_table = [20, 30, 10, 0, 0, 10, 30, 20, 20, 20, 0, 0, 0, 0, 20, 20, -10,
               -20, -20, -20, -20, -20, -20, -10, -20,
               -30, -30, -40, -40, -30, -30, -20, -30, -40, -40, -50, -50, -40,
               -40, -30, -30, -40, -40, -50, -50, -40,
               -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40,
               -50, -50, -40, -40, -30]


def evaluate_board():
    """Evaluates the current position of the board

    """
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (
                wr - br) + 900 * (wq - bq)

    pawnsq = sum([pawn_table[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawn_table[chess.square_mirror(i)] for i in
                           board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum(
        [knights_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knights_table[chess.square_mirror(i)] for i in
                               board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum(
        [bishops_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishops_table[chess.square_mirror(i)] for i in
                               board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum(
        [rooks_table[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rooks_table[chess.square_mirror(i)] for i in
                           board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum(
        [queens_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queens_table[chess.square_mirror(i)] for i in
                             board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum(
        [kings_table[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kings_table[chess.square_mirror(i)] for i in
                           board.pieces(chess.KING, chess.BLACK)])

    assessment = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return assessment
    else:
        return -assessment


def alphabeta(alpha, beta, depth_left):
    """Searches for the best move using minimax and alphabeta

    Parameters
    ----------
    alpha : int

    beta : int

    depth_left : int
        Depth of the left branch of the minimax tree
    Returns
    -------
    int
        The calculated 'best score' for determining a move
    """
    best_score = -9999
    if depth_left == 0:
        return quiesce(alpha, beta)
    for legal_move in board.legal_moves:
        board.push(legal_move)
        score = -alphabeta(-beta, -alpha, depth_left - 1)
        board.pop()
        if score >= beta:
            return score
        if score > best_score:
            best_score = score
        if score > alpha:
            alpha = score
    return best_score


def quiesce(alpha, beta):
    """Performs a quiescence search for the minimax tree

    Parameters
    ----------
    alpha : int

    beta : int

    Returns
    -------
    int
        The estimated value of the children of the node
    """
    stand_pat = evaluate_board()
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for legal_move in board.legal_moves:
        if board.is_capture(legal_move):
            board.push(legal_move)
            score = -quiesce(-beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
    return alpha


def select_move(depth):
    """

    """
    try:
        legal_move = chess.polyglot.MemoryMappedReader(
            "C:/Users/your_path/books/human.bin").weighted_choice(board).move
        return legal_move
    except:
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -100000
        beta = 100000
        for legal_move in board.legal_moves:
            board.push(legal_move)
            board_value = -alphabeta(-beta, -alpha, depth - 1)
            if board_value > best_value:
                best_value = board_value
                best_move = legal_move
            if board_value > alpha:
                alpha = board_value
            board.pop()
        return best_move


def muonium_move():
    """Prompts the muonium bot to make a move
    """
    move = select_move(3)
    board.push(move)


app = Flask(__name__)


@app.route("/")
def main():
    global count, board
    if count == 1:
        count += 1
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" ' \
           'type="text"></input></form>'
    ret += '<form action="/muonium/" method="post"><button name="Comp Move" type="submit">Make Muonium ' \
           'Move</button></form>'
    if board.is_stalemate():
        print("Its a draw by stalemate")
    elif board.is_checkmate():
        print("Checkmate")
    elif board.is_insufficient_material():
        print("Its a draw by insufficient material")
    elif board.is_check():
        print("Check")
    return ret


@app.route("/board.svg/")
def board():
    """Displays the static board

    Returns
    -------
    """
    return Response(chess.svg.board(board=board, size=700),
                    mimetype='image/svg+xml')


# Human Move
@app.route("/move/")
def move():
    """Method for a human movement

    Returns
    -------
    str
        HTML string for the Flask web application
    """
    try:
        human_move = request.args.get('move', default="")
        print(human_move)
        board.push_san(human_move)
    except Exception:
        traceback.print_exc()
        raise
    return main()


@app.route("/muonium/", methods=['POST'])
def muonium():
    """Prompts the engine to make a move, if possible

    Returns
    -------
    str
        HTML string for the Flask web application
    """
    try:
        muonium_move()
    except Exception:
        traceback.print_exc()
    return main()


@app.route("/game/", methods=['POST'])
def game():
    """Begin a new game

    Returns
    -------
    str
        HTML string for the Flask web application
    """
    print("Board Reset, Best of Luck for the next game.")
    board.reset()
    return main()


@app.route("/undo/", methods=['POST'])
def undo():
    """Undo a move, if possible

    Returns
    -------
    str
        HTML string for the Flask web application
    """
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
        print("Nothing to undo")
        raise
    return main()


# Main Function
if __name__ == '__main__':
    count = 1
    board = chess.Board()
    webbrowser.open("http://localhost:5000/")
    app.run()
