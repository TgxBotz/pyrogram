from sqlalchemy import Boolean, Column, String
from SpamBot.plugins.sql import BASE, SESSION


class Chats(BASE):
    __tablename__ = "chats"
    chat_id = Column(String(14), primary_key=True)

    def init(self, chat_id):
        self.chat_id = chat_id


Chats.__table__.create(checkfirst=True)


def add_chat(chat_id: str):
    nightmoddy = Chats(str(chat_id))
    SESSION.add(nightmoddy)
    SESSION.commit()


def rmchat(chat_id: str):
    rmnightmoddy = SESSION.query(Chats).get(str(chat_id))
    if rmnightmoddy:
        SESSION.delete(rmnightmoddy)
        SESSION.commit()


def get_all_chat_id():
    stark = SESSION.query(Chats).all()
    SESSION.close()
    return stark


def is_chat(chat_id: str):
    try:
        s__ = SESSION.query(Chats).get(str(chat_id))
        if s__:
            return str(s__.chat_id)
    finally:
        SESSION.close()
