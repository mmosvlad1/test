from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import aiohttp
import ssl

money = []

TOKEN_API = "6427297581:AAE5kzDDCn6hhVyc0n_x46BKTua69JA_mgk"
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Successful start")


@dp.message_handler(commands=['addresses'])
async def help_command(message: types.Message):
    await message.answer(text="send addresses")
    dp.register_message_handler(addresses_comp, content_types=types.ContentTypes.TEXT)


async def fetch_page(url):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        async with session.get(url) as response:
            return await response.text()


async def addresses_comp(message: types.Message):
    addresses = message.text + "\n"
    with open('addresses.txt', 'w') as file_loc:
        file_loc.writelines(addresses)

    money_c = []
    with open('addresses.txt', 'r') as file_loc:
        addresses = file_loc.readlines()

    for addres in addresses:
        url = f"https://etherscan.io/address/{addres[:-1]}"
        response_after_search = await fetch_page(url)

        soup_after_search = BeautifulSoup(response_after_search, 'html.parser')
        info_div = soup_after_search.find_all('h4', {'class': 'text-cap mb-1'})
        value = info_div[1].parent
        value = str(value)

        numb = 50
        money_count = []
        while value[numb:]:
            if value[numb] == '.':
                break

            money_count.append(value[numb])
            numb += 1

        money_c.append("".join(money_count))

    with open('money.txt', 'w') as file_loc:
        file_loc.writelines("\n".join(money_c))

    with open('addresses.txt', 'r') as file_loc:
        addresses = file_loc.readlines()

    with open('money.txt', 'r') as file_loc:
        money_list = file_loc.readlines()

    answer = ""
    for address, money_c in zip(addresses, money_list):
        answer += address + " - " + money_c + "\n"

    await message.answer(text=answer)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
