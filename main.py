import hashlib
import os
from typing import Optional, Tuple

import chess
import chess.pgn
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

from modules.gifs import generate_gif
from modules.keyboards import *
from modules.session import Session
from modules.session_manager import SessionManager

# TODO: draw offers?


def main() -> None:
    """Процесс работы бота"""
    print("Hello!")

    # Парс токена из .env
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    token = os.getenv("TOKEN")
    api_key = os.getenv("API_KEY")

    # Инициализация бота, диспатча и менеджера сессий
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot)
    session_manager = SessionManager()

    def perform_move(
        move: str, session_id: str
    ) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
        """Handles chess moves logic"""
        text = ""
        current_session = session_manager.find_session(session_id)
        current_board = current_session.board
        current_session.incr_move_count()
        current_board.push_uci(move)
        current_session.side_to_move = (
            "белые" if current_session.side_to_move == "чёрные" else "чёрные"
        )
        if current_board.is_checkmate():
            gif = generate_gif(current_board, api_key)
            text += "Игра окончена матом!\n"
            keyboard = None
            if current_session.side_to_move == "белые":
                text += f"{current_session.player2_name} (черные) победил!\n"
            else:
                text += f"{current_session.player1_name} (белые) победил!\n"
            session_manager.delete_session(session_id)
            text += gif
        elif current_board.is_stalemate():
            text += f"Игра окончена ничьей!\n{current_session.player1_name} 1 - 1 {current_session.player2_name}"
            gif = generate_gif(current_board, api_key)
            text += gif
            keyboard = None
            session_manager.delete_session(session_id)
        else:
            text = (
                f"Белые: {current_session.player1_name}\n"
                f"Чёрные: {current_session.player2_name}\n"
                f"Ход: {current_board.fullmove_number} ({current_session.side_to_move})\n"
            )
            if current_board.is_check():
                text += "Шах!\n"
            keyboard = matrix_to_keyboard(
                fen_to_matrix(current_board.fen()),
                surr_button=True,
                reverse=(current_session.side_to_move == "чёрные"),
            )
        return text, keyboard

    @dispatcher.inline_handler()
    async def inline_handler(query: types.InlineQuery) -> None:
        """
        Handles inline tag "@ChessNow_bot"
        :param query: inline callback from telegram
        :return: None
        """
        result_id = hashlib.md5(query.id.encode()).hexdigest()

        response = [
            types.InlineQueryResultArticle(
                id=result_id,
                title="Шахматы",
                input_message_content=types.InputTextMessageContent(
                    message_text="Начать игру?"
                ),
                reply_markup=start_keyboard,
            )
        ]
        await query.answer(response, cache_time=1, is_personal=True)

    @dispatcher.callback_query_handler(text="join")
    async def callback_query_handler(query: types.CallbackQuery) -> None:
        """
        Handles 'Join' button for player2
        :param query: callback from markup_keyboard by telegram
        :return: None
        """
        current_session: Session = session_manager.find_session(query.inline_message_id)
        current_session.add_player(
            user_id=query.from_user.id, user_name=query.from_user.first_name
        )
        current_session.board = chess.Board()
        new_keyboard = matrix_to_keyboard(fen_to_matrix(current_session.board.fen()))
        move_count = 0
        current_session.side_to_move = "белые"
        await bot.edit_message_text(
            text=f"Белые: {current_session.player1_name}\n"
            f"Чёрные: {current_session.player2_name}\n"
            f"Ход: {move_count} ({current_session.side_to_move})\n",
            inline_message_id=query.inline_message_id,
        )
        await bot.edit_message_reply_markup(
            inline_message_id=query.inline_message_id, reply_markup=new_keyboard
        )

    @dispatcher.callback_query_handler(text="start")
    async def callback_query_handler(query: types.CallbackQuery) -> None:
        """
        Handles 'Start' button for player1
        :param query: callback from markup_keyboard by telegram
        :return: None
        """
        session = Session(
            player1_id=query.from_user.id,
            player1_name=query.from_user.first_name,
            session_id=query.inline_message_id,
        )
        session_manager.add_session(session)
        await bot.edit_message_text(
            text=f"Белые: {query.from_user.first_name}\n" f"Чёрные: ожидаем",
            inline_message_id=query.inline_message_id,
        )
        await bot.edit_message_reply_markup(
            inline_message_id=query.inline_message_id, reply_markup=join_keyboard
        )

    @dispatcher.callback_query_handler(text="surrender")
    async def callback_query_handler(query: types.CallbackQuery) -> None:
        """
        Handles 'Surrender' button for both active players
        :param query: callback from markup_keyboard by telegram
        :return: None
        """
        if query.message:
            chat_id = query.message.chat.id
        else:
            chat_id = query.from_user.id
        current_session: Session = session_manager.find_session(query.inline_message_id)
        if query.from_user.id not in (
            current_session.player1_id,
            current_session.player2_id,
        ):
            pass
        else:
            board = current_session.board
            gif_url = generate_gif(board, api_key)
            move_count = board.fullmove_number
            surr_side = (
                "белые"
                if query.from_user.id == current_session.player1_id
                else "чёрные"
            )
            if query.from_user.id == current_session.player1_id:
                surr_playername = current_session.player1_name
            else:
                surr_playername = current_session.player2_name
            text = (
                f"Белые: {current_session.player1_name}\n"
                f"Чёрные: {current_session.player2_name}\n"
                f"Ход: {move_count}\n"
                f"Игра окончена: {surr_playername} ({surr_side}) сдался.\n"
                f"{gif_url}"
            )
            session_manager.delete_session(query.inline_message_id)
            await bot.edit_message_text(
                inline_message_id=query.inline_message_id, text=text
            )

    @dispatcher.callback_query_handler()
    async def callback_query_handler(query: types.CallbackQuery) -> None:
        """
        Handles all chess keyboard callbacks & performs moves
        :param query: CallbackQuery, universal ID of a session
        :return: None
        """
        current_session: Session = session_manager.find_session(query.inline_message_id)
        current_board: chess.Board = current_session.board
        if (
            current_session.side_to_move == "белые"
            and query.from_user.id == current_session.player1_id
        ) or (
            current_session.side_to_move == "чёрные"
            and query.from_user.id == current_session.player2_id
        ):
            current_session.move_buf.append(query.data)
            if len(current_session.move_buf) == 2:
                move = current_session.move_buf[0] + current_session.move_buf[1]
                # FIXME: queening is impossible (b2a1 wouldnt be in legal_moves; b2a1=Q or something similar would)
                if chess.Move.from_uci(move) in current_board.legal_moves:
                    text, new_keyboard = perform_move(move, query.inline_message_id)
                    await bot.edit_message_text(
                        text=text, inline_message_id=query.inline_message_id
                    )
                    await bot.edit_message_reply_markup(
                        inline_message_id=query.inline_message_id,
                        reply_markup=new_keyboard,
                    )
                current_session.move_buf = list()

    executor.start_polling(dispatcher, skip_updates=False)


if __name__ == "__main__":
    main()
