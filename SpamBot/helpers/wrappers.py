import functools

def cb_wrapper(func):
    @functools.wraps(func)
    async def callb(client, cb):
      user = cb.from_user.id
      if cb.from_user.id != user:
          await cb.answer("This Menu Wasn't Opened By You!")
      else:
          await func(client, cb)
    return callb
