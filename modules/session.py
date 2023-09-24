import chess
from typing import Optional


class Session:
    """ Sessions (lobbies, started and ongoing games)

    Attributes:
        player1_id      telegram id of host player
        player2_id      telegram id of connected player
        player1_name    telegram first_name of host player
        player2_name    telegram first_name of connected player
        session_id      query.inline_message_id, universal identifier
        board           Chess board from pychess
    """

    def __init__(self, player1_id: str, player1_name: str, session_id: str):
        """
        Session is created whenever host player starts the game
        :param player1_id: host player telegram id
        :param player1_name: host player first_name
        :param session_id: query.inline_message_id, universal identifier
        """
        self.__player1_id: str = player1_id
        self.__player1_name: str = player1_name
        self.__player2_id: Optional[str] = None
        self.__player2_name: Optional[str] = None
        self.__session_id: str = session_id
        self.__board: Optional[chess.Board] = None
        self.__move_count: int = 0
        self.side_to_move: Optional[str] = None
        self.move_buf: list = list()

    @property
    def player1_id(self) -> str:
        return self.__player1_id

    @property
    def player2_id(self) -> str:
        return self.__player2_id

    @property
    def player1_name(self) -> str:
        return self.__player1_name

    @property
    def player2_name(self) -> str:
        return self.__player2_name

    def add_player(self, user_id: str, user_name: str) -> int:
        """
        Adds connected player to session, when he joins
        :param user_id: connected player telegram id
        :param user_name: connected player telegram first_name
        :return: 0; 1 in case if error occurs
        """
        if self.__player2_id is not None:
            return 1
        self.__player2_id: str = user_id
        self.__player2_name: str = user_name
        return 0

    def get_session_id(self) -> str:
        return self.__session_id

    @property
    def board(self) -> chess.Board:
        return self.__board

    @board.setter
    def board(self, board) -> None:
        self.__board = board

    def incr_move_count(self) -> int:
        self.__move_count += 1
        return self.__move_count

    @property
    def move_num(self) -> int:
        return self.__move_count