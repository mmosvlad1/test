from aiogram import Bot, Dispatcher, executor, types
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Your Telegram bot token
TOKEN_API = "6427297581:AAE5kzDDCn6hhVyc0n_x46BKTua69JA_mgk"

# Help command message
HELP_COMMAND = """
/help - list of commands
/start - start using the bot
"""

# Create the bot and dispatcher
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

# Function to fetch the HTML content of a web page using aiohttp
async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()

# Function to scrape the ETH value from a web page
async def scrape_address(address, session):
    url = f"https://etherscan.io/address/{address}"

    async with session.get(url) as response:
        html = await response.text()

    soup_after_search = BeautifulSoup(html, 'html.parser')
    info_div = soup_after_search.find_all('h4', {'class': 'text-cap mb-1'})
    value = info_div[1].parent
    value = str(value)

    # Use regular expression to find the ETH value in the text
    import re
    eth_value = re.search(r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?', value)
    if eth_value:
        return eth_value.group().replace('$', '').replace(',', '')
    else:
        return None

async def get_money_for_addresses(addresses):
    money = []

    async with aiohttp.ClientSession() as session:
        tasks = [scrape_address(address, session) for address in addresses]
        money = await asyncio.gather(*tasks)

    return money

# Start command handler
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text="Welcome", parse_mode="HTML")
    await message.delete()

# Help command handler
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP_COMMAND)

# Give command handler (example of sending a sticker)
@dp.message_handler(commands=['give'])
async def give_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="STICKER_FILE_ID")
    await message.delete()

# Addresses command handler
@dp.message_handler(commands=['addresses'])
async def addresses_command(message: types.Message):
    await message.answer(text="Send addresses separated by new lines.")
    dp.register_message_handler(process_addresses, content_types=types.ContentTypes.TEXT)

# Process the addresses sent by the user
async def process_addresses(message: types.Message):
    # Split the addresses by new lines and remove empty lines
    addresses = message.text.split("\n")
    addresses = [address.strip() for address in addresses if address.strip()]

    if not addresses:
        await message.answer("No valid addresses found.")
        return

    # Save addresses to a file
    with open('addresses.txt', 'w') as file_loc:
        file_loc.writelines("\n".join(addresses))

    # Scrape the ETH values for the addresses using aiohttp and BeautifulSoup
    money = await get_money_for_addresses(addresses)

    # Save the ETH values to a file
    with open('money.txt', 'w') as file_loc:
        file_loc.writelines("\n".join(money))

    # Format the response message with addresses and corresponding ETH values
    response = ""
    for address, eth_value in zip(addresses, money):
        response += f"{address} - {eth_value}\n"

    await message.answer(text=response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
