""" Работа с giphy """

import chess
import requests
from gifpgn import CreateGifFromPGN
from typing import Optional


def get_pgn_from_board(board: chess.Board) -> str:
    """ Returns PGN notation from chess.Board object """
    game = chess.pgn.Game()
    node = game
    for move in board.move_stack:
        node = node.add_main_variation(move)
    pgn = game.__str__()
    return pgn


def generate_gif(board) -> Optional[str]:
    """ Generates and uploads to giphy chessmatch-gif, returns link """
    upload_url = "https://upload.giphy.com/v1/gifs"
    api_key = "lm2tU6LZ6qNaktKrdCtCTtC4WTUtC90u"
    gif = CreateGifFromPGN(get_pgn_from_board(board))
    gif.generate("output_gif.gif")
    params = {
        "api_key": api_key,
    }

    with open("output_gif.gif", "rb") as file:
        files = {
            "file": file
        }

        response = requests.post(upload_url, params=params, files=files)

    if response.status_code == 200:
        data = response.json()
        gif_id = data["data"]["id"]
        return f"https://media.giphy.com/media/{gif_id}/giphy.gif"
    return None