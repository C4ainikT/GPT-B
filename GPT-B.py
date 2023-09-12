import json
import disnake
from disnake.ext import commands
import nltk
import string  # Добавим импорт модуля string
import asyncio
from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz

# Загрузка модели из файла JSON
def load_model_from_json(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            model = json.load(f)
        return model
    except FileNotFoundError:
        print("Файл не найден или не удалось прочитать его.")
        return {}

# Загрузка модели из файла JSON
model_data = load_model_from_json('GPT-B.json')

# Инициализация библиотеки nltk
nltk.download('punkt')

bot = commands.Bot(command_prefix="*", intents=disnake.Intents.all())

# Функция для очистки текста от ненужных символов
def clean_text(text):
    # Удаляем символы "! ? . ,", но оставляем символы "/ \ | : ) ("
    cleaned_text = ''.join([char if char not in "!?., " else ' ' for char in text])
    return cleaned_text


@bot.event
async def on_ready():
    print("Бот готов к работе!")

@bot.slash_command(description="Информация о Боте.")
async def help(ctx: disnake.AppCmdInter):
    await ctx.response.send_message("Ваш текст справки")

@bot.slash_command(description="Генерирует ответ на вопрос с использованием вашей модели JSON.")
async def chat(interaction: disnake.AppCmdInter):
    await interaction.send("**Введите ваш вопрос, и я постараюсь на него ответить.**")
    try:
        # Ожидание сообщения от пользователя в течение 60 секунд
        response = await bot.wait_for("message", timeout=60, check=lambda m: m.author == interaction.author)
        user_question = response.content.lower()  # Преобразуем весь текст в нижний регистр
        user_question = clean_text(user_question)  # Очищаем текст от символов "! ? . ,"

        # Токенизация вопроса пользователя
        user_tokens = word_tokenize(user_question)

        # Поиск ближайшего совпадения вопроса пользователя с ключами модели JSON (по токенам)
        closest_match = None
        highest_score = 0
        for key in model_data.keys():
            key_tokens = word_tokenize(key.lower())  # Преобразуем ключ в нижний регистр и токенизируем
            score = fuzz.ratio(user_tokens, key_tokens)  # Сравниваем токены
            if score > highest_score:
                highest_score = score
                closest_match = key

        if closest_match and highest_score >= 57:  # Устанавливаем порог совпадения в 70 (можете изменить)
            response_text = model_data[closest_match]
        else:
            response_text = "Извините, я не знаю ответа на этот вопрос."

        await interaction.send(response_text)

    except asyncio.TimeoutError:
        await interaction.send("**Вы не ввели вопрос вовремя. Попробуйте снова командой /chat.**")

bot.run("ваш токен")
