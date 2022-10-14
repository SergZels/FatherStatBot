from aiogram_broadcaster import TextBroadcaster
from bd.bd import botBD
import asyncio
import conf

messageText="Нагадування - запишіть вашу виручку!"
Token = conf.TOKEN
botBD = botBD()
Users = botBD.getUserId()

async def main():

    broadcaster = TextBroadcaster(Users, messageText, bot_token=Token)
    try:
        await broadcaster.run()
    finally:
        await broadcaster.close_bot()

if __name__ == '__main__':
    asyncio.run(main())