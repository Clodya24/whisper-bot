from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import whisper
from pydub import AudioSegment
import os

# Загружаем модель Whisper один раз
model = whisper.load_model("tiny")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋\nОтправь мне голосовое сообщение, и я расшифрую его в текст."
    )

# Обработчик голосовых сообщений
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    file = await context.bot.get_file(update.message.voice.file_id)
    file_path = f"{user.id}.ogg"
    wav_path = f"{user.id}.wav"

    await file.download_to_drive(file_path)

    # Конвертация ogg → wav
    audio = AudioSegment.from_ogg(file_path)
    audio.export(wav_path, format="wav")

    # Распознавание речи
    result = model.transcribe(wav_path)
    await update.message.reply_text(result["text"])

    os.remove(file_path)
    os.remove(wav_path)

# Запуск бота
app = ApplicationBuilder().token("7160687291:AAExGY5mlfJNVJ-rfQyJjjQXMsoPfd6lUSI").build()

# Добавляем обработчики
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

# Запуск
app.run_polling()