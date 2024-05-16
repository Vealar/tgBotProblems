import asyncio
from aiogram import Bot, Dispatcher
from config.config_bot import ACCESS_TOKEN
from tgBot.registration.registration_handlers import router_registration
from tgBot.user.common_handlers import router_common
from tgBot.user.search_handlers import router_search
from tgBot.admin.admin_task import router_admin
from tgBot.registration.registration_admin import router_registration_admin
# making bot and dispatcher
bot = Bot(token=ACCESS_TOKEN)
dp = Dispatcher()


async def main():
    # connect with routers
    dp.include_router(router_registration_admin)
    dp.include_router(router_admin)
    dp.include_router(router_search)
    dp.include_router(router_common)
    dp.include_router(router_registration)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
