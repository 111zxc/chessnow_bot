import unittest
from modules.session import Session
from modules.session_manager import SessionManager


class TestSessionManager(unittest.TestCase):
    def test_add_session(self):
        session_manager = SessionManager()
        session = Session("p1_name", "p1_id", "session_id")
        session_manager.add_session(session)
        self.assertIn(session, session_manager._SessionManager__sessions)

    def test_delete_session(self):
        session_manager = SessionManager()
        session = Session("p1_name", "p1_id", "session_id")
        session_manager.add_session(session)
        result = session_manager.delete_session("session_id")
        self.assertEqual(result, 0)
        self.assertNotIn(session, session_manager._SessionManager__sessions)

    def test_delete_session_nonexistent(self):
        session_manager = SessionManager()
        result = session_manager.delete_session("nonexistent_id")
        self.assertEqual(result, 1)

    def test_find_session(self):
        session_manager = SessionManager()
        session = Session("p1_name", "p1_id", "session_id")
        session_manager.add_session(session)
        result = session_manager.find_session("session_id")
        self.assertEqual(result, session)

    def test_find_session_nonexistent(self):
        session_manager = SessionManager()
        result = session_manager.find_session("nonexistent_id")
        self.assertEqual(result, 1)

if __name__ == '__main__':
    unittest.main()
