import unittest
from modules.session import Session

class TestSession(unittest.TestCase):
    def test_create_session(self):
        session = Session("player1_id", "player1_name", "session_id")
        self.assertEqual(session.player1_id, "player1_id")
        self.assertEqual(session.player1_name, "player1_name")
        self.assertEqual(session.get_session_id(), "session_id")
        self.assertIsNone(session.player2_id)
        self.assertIsNone(session.player2_name)
        self.assertIsNone(session.board)
        self.assertEqual(session.move_num, 0)

    def test_add_player(self):
        session = Session("player1_id", "player1_name", "session_id")
        result = session.add_player("player2_id", "player2_name")
        self.assertEqual(result, 0)
        self.assertEqual(session.player2_id, "player2_id")
        self.assertEqual(session.player2_name, "player2_name")

    def test_add_player_error(self):
        session = Session("player1_id", "player1_name", "session_id")
        session.add_player("player2_id", "player2_name")
        result = session.add_player("player3_id", "player3_name")
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
