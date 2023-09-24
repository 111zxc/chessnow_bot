from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""
Keyboard Markups
"""

# JOIN KEYBOARD
join_keyboard = InlineKeyboardMarkup(row_width=1)
join_button = InlineKeyboardButton(text="Присоединиться", callback_data="join")
join_keyboard.add(join_button)

# START KEYBOARD
start_keyboard = InlineKeyboardMarkup(row_width=1)
start_button = InlineKeyboardButton(text="Начать игру", callback_data="start")
start_keyboard.add(start_button)

ascii_to_unicode = {
    'k': '♔',
    'K': '♚',
    'q': '♕',
    'Q': '♛',
    'r': '♖',
    'R': '♜',
    'b': '♗',
    'B': '♝',
    'n': '♘',
    'N': '♞',
    'p': '♙',
    'P': '♟︎',
    '.': '.'
}


def fen_to_matrix(fen: str) -> list:
    """ Generating 8x8 matrix from FEN notation """
    fen = fen.split()[0]
    matrix = [['.'] * 8 for _ in range(8)]
    rows = fen.split('/')

    for row_idx, row in enumerate(rows):
        col_idx = 0
        for char in row:
            if char.isdigit():
                col_idx += int(char)
            else:
                matrix[row_idx][col_idx] = char
                col_idx += 1
    return matrix


def matrix_to_keyboard(matrix: list, surr_button=True, reverse=False) -> InlineKeyboardMarkup:
    """ Generating chessboard-keyboard by 8x8 matrix """
    buttons = []
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=8)

    if not reverse:
        for i in range(8):
            for j in range(8):
                button = InlineKeyboardButton(text=matrix[i][j],
                                              callback_data=chr(97 + j) + str(8 - i))
                buttons.append(button)
        keyboard.add(*buttons)

    if reverse:
        for i in range(8):
            for j in range(8):
                button = InlineKeyboardButton(text=matrix[7-i][7-j],
                                              callback_data=chr(104 - j) + str(i+1))
                buttons.append(button)
        keyboard.add(*buttons)

    if surr_button:
        surrender_button = InlineKeyboardButton(text='Сдаться',
                                                callback_data='surrender')
        keyboard.add(surrender_button)
    return keyboard