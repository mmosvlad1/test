from aiogram import Bot, Dispatcher, executor, types
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
money = []


TOKEN_API = "6427297581:AAE5kzDDCn6hhVyc0n_x46BKTua69JA_mgk"

HELP_COMMAND = """
/help - список команд
/start - почати роботу з ботом
"""


bot = Bot(TOKEN_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print("Successful start")


@dp.message_handler(commands=['start'])
async def help_command(message: types.Message):
    await message.answer(text="Welcome", parse_mode="HTML")
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)


@dp.message_handler(commands=['give'])
async def help_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEJ4ztkyjaogxG1XyPFsrpVidMoGyK-WgAC7BMAAoOkQUj-3ifolu8jES8E")
    await message.delete()\

@dp.message_handler(commands=['addresses'])
async def help_command(message: types.Message):
    await message.answer(text="send addresses")
    dp.register_message_handler(addresses_comp, content_types=types.ContentTypes.TEXT)


async def addresses_comp(message: types.Message):
        addresses = message.text + "\n"
        with open('addresses.txt', 'w') as file_loc:
            file_loc.writelines(addresses)

        money = []

        with open('addresses.txt', 'r') as file_loc:
            addresses = file_loc.readlines()

        for addres in addresses:
            url = f"https://etherscan.io/address/{addres[:-1]}"

            driver_service = Service('chromedriver_mac_arm64/chromedriver')
            driver = webdriver.Chrome(service=driver_service)
            driver.get(url)

            driver.implicitly_wait(50)
            time.sleep(0.4)
            response_after_search = driver.page_source

            driver.quit()

            soup_after_search = BeautifulSoup(response_after_search, 'html.parser')
            info_div = soup_after_search.find_all('h4', {'class': 'text-cap mb-1'})
            value = info_div[1].parent
            value = str(value)

            numb = 50
            money_count = []
            while value[numb:]:
                if (value[numb] == '.'):
                    break

                money_count.append(value[numb])
                numb += 1

            money.append("".join(money_count))
            driver.quit()

        with open('money.txt', 'w') as file_loc:
            file_loc.writelines("\n".join(money))

        with open('addresses.txt', 'r') as file_loc:
            addresses = file_loc.readlines()

        with open('money.txt', 'r') as file_loc:
            money_list = file_loc.readlines()

        # merged_list = [(addresses[i], money[i]) for i in range(0, len(addresses))]
        answer = ""
        for address, money_c in zip(addresses, money_list):
            answer += address + " - " + money_c + "\n"

        await message.answer(text=answer)



@dp.message_handler(content_types=['sticker'])
async def send_sticker_id(message: types.Message):
    await message.answer(message.sticker.file_id)


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(text=message.text)

@dp.message_handler(content_types=[''])
async def echo(message: types.Message):
    await message.answer(text=message.text)@dp.message_handler(content_types=[''])
async def echo(message: types.Message):
    await message.answer(text=message.text)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
