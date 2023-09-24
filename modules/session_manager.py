from modules.session import Session

class SessionManager:
    """ Used to manage sessions """

    def __init__(self) -> None:
        """
        Creates a new instance of a session manager, creates empty sessions list
        """
        self.__sessions: list = list()

    def add_session(self, session: Session) -> None:
        """
        Adds a session object to __sessions
        :param session: object of a session
        :return: None
        """
        self.__sessions.append(session)

    def delete_session(self, session_id: str) -> int:
        """
        Deletes a session from __sessions.
        Game is either finished or dismissed before starting.
        :param session_id: session query.inline_message_id, universal ID
        :rels
        turn: int
        """
        for session in self.__sessions:
            if session.get_session_id() == session_id:
                self.__sessions.remove(session)
                return 0
        return 1

    def find_session(self, session_id: str) -> Session | int:
        """
        Returns an existing session object by its query.inline_message_id
        :param session_id: query.inline_message_id, universal ID
        :return: Session object; 1 in case session doesn't exist
        """
        for session in self.__sessions:
            if session.get_session_id() == session_id:
                return session
        return 1