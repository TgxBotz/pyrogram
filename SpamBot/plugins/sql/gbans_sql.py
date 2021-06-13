from sqlalchemy import Column, String
from SpamBot.plugins.sql import BASE, SESSION


class Gban(BASE):
    __tablename__ = "gban"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


Gban.__table__.create(checkfirst=True)


def is_gbanned(sender_id):
    try:
        return SESSION.query(Gban).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gban(sender):
    adder = Gban(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def ungban(sender):
    rem = SESSION.query(Gban).get((str(sender)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def all_gbanned():
    rem = SESSION.query(Gban).all()
    SESSION.close()
    return rem
