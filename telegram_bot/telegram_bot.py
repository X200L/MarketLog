import telebot
from telebot import types
import logging
import os
from datetime import datetime
from PIL import Image
from backend.main2 import starter
from cv import yanlog
from backend.yanlog import ImageProcessor
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ''
app.config['TEMP_UPLOAD_FOLDER'] = 'temp_uploads'

def build_grid(chat_id, shelf_size, operation_zone_x, operation_zone_y, image_path):
    filename = image_path.replace('\\', '/')
    robot_size = shelf_size
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file_path = '/'.join(filename.split('/')[:-1])
    image_name = filename.split('/')[-1]

    processor = ImageProcessor(app.config['UPLOAD_FOLDER'])
    processed_filename = processor.process_file(file_path, image_name)
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    print(processed_path)
    starter(processed_path, operation_zone_x, operation_zone_y, robot_size, temp_upload_folder=app.config['TEMP_UPLOAD_FOLDER'])



# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

bot_token = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = telebot.TeleBot(bot_token)

# Папка для сохранения загруженных изображений
UPLOAD_FOLDER = '../Mesher/outline_of_warehouse'
# Создаем папку, если она не существует
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Разрешенные расширения файлов
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Словарь для хранения состояний пользователей
user_states = {}

# В обработчике handle_image, после сохранения файла, добавляем:



# Добавляем новую кнопку в клавиатуру
def create_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Что делает этот бот?')
    btn2 = types.KeyboardButton('Создать топологию склада')
    btn3 = types.KeyboardButton('Требования к файлу')
    btn4 = types.KeyboardButton('Получить мой файл')  # Новая кнопка
    btn5 = types.KeyboardButton('/start')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


# Добавляем обработчик для отправки последнего загруженного файла
@bot.message_handler(func=lambda message: message.text == 'Получить мой файл')
def send_last_uploaded_file(message):
    try:
        chat_id = message.chat.id

        # Проверяем, есть ли сохраненный файл для этого пользователя
        if 'last_uploaded_file' not in user_states.get(chat_id, {}):
            bot.reply_to(message, "Вы еще не загружали файлов или он еще не прошел обработку", reply_markup=create_reply_keyboard())
            return

        file_path = user_states[chat_id]['last_uploaded_file']

        # Проверяем существование файла
        if not os.path.exists(file_path):
            bot.reply_to(message, "Файл не найден или он еще не прошел обработку", reply_markup=create_reply_keyboard())
            return

        # Отправляем файл
        with open(file_path, 'rb') as file:
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                bot.send_photo(chat_id, file, reply_markup=create_reply_keyboard())
            else:
                bot.send_document(chat_id, file, reply_markup=create_reply_keyboard())

        logger.info(f"Пользователю {chat_id} отправлен его файл: {file_path}")

    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        bot.reply_to(message, "Произошла ошибка при отправке файла", reply_markup=create_reply_keyboard())


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_to_png(image_path):
    """Конвертирует изображение в PNG и сохраняет с новым расширением"""
    try:
        # Открываем изображение
        img = Image.open(image_path)

        # Создаем новое имя файла с расширением .png
        png_path = os.path.splitext(image_path)[0] + '.png'

        # Сохраняем в формате PNG
        img.save(png_path, 'PNG')

        # Удаляем оригинальный файл, если он не PNG
        if not image_path.lower().endswith('.png'):
            os.remove(image_path)

        return png_path
    except Exception as e:
        logger.error(f"Ошибка при конвертации в PNG: {e}")
        return image_path


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_states[message.chat.id] = {
        'waiting_for_image': False,
        'waiting_for_coords': False,
        'waiting_for_shelf_size': False
    }
    bot.send_message(
        message.chat.id,
        f"Привет, {user.first_name}! Я бот для создания топологии склада.",
        reply_markup=create_reply_keyboard()
    )

@bot.message_handler(func=lambda message: message.text == 'Создать топологию склада')
def request_image(message):
    user_states[message.chat.id] = {
        'waiting_for_image': True,
        'waiting_for_coords': False,
        'waiting_for_shelf_size': False
    }
    bot.send_message(
        message.chat.id,
        "Пожалуйста, загрузите изображение склада в формате JPG или PNG:",
        reply_markup=types.ReplyKeyboardRemove(selective=True)
    )


@bot.message_handler(content_types=['photo', 'document'])
def handle_image(message):
    try:
        chat_id = message.chat.id

        if not user_states.get(chat_id, {}).get('waiting_for_image', False):
            bot.reply_to(message, "Пожалуйста, нажмите 'Создать топологию склада' для загрузки изображения.",
                         reply_markup=create_reply_keyboard())
            return

        file_info = None
        file_name = ""
        file_extension = ""

        if message.photo:
            file_info = bot.get_file(message.photo[-1].file_id)
            file_extension = "jpg"
            file_name = f"Topology_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"


        elif message.document:
            if not allowed_file(message.document.file_name):
                bot.reply_to(message, "Извините, я принимаю только изображения в формате JPG или PNG.")
                return
            file_info = bot.get_file(message.document.file_id)
            file_extension = message.document.file_name.split('.')[-1].lower()
            file_name = f"Topology_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"

        if file_info:
            downloaded_file = bot.download_file(file_info.file_path)
            temp_file_path = os.path.join(UPLOAD_FOLDER, file_name)

            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

            with open(temp_file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
             # Добавляем эту строку
            png_file_path = convert_to_png(temp_file_path)

            user_states[chat_id] = {
                'waiting_for_image': False,
                'waiting_for_coords': True,
                'waiting_for_shelf_size': False,
                'image_path': png_file_path
            }
            user_states[chat_id]['last_uploaded_file'] = png_file_path  # ОТПРАВЛЯЕМ ФАЙЛ ТОЛЬКО ЧТО ОТправлЕННЫЙ




            bot.reply_to(
                message,
                "✅ Изображение успешно сохранено в формате PNG\n\n"
                "Теперь введите координаты операционной зоны в пикселях в формате:\n"
                "X1,Y1\n"
                "Например: 100,200 ",

                reply_markup=types.ReplyKeyboardRemove(selective=True)
            )
            logger.info(f"Пользователь {message.from_user.id} загрузил изображение: {png_file_path}")
        else:
            bot.reply_to(message, "Не удалось обработать изображение. Попробуйте еще раз.",
                         reply_markup=create_reply_keyboard())

    except Exception as e:
        logger.error(f"Ошибка при загрузке изображения: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке изображения. Попробуйте еще раз.",
                     reply_markup=create_reply_keyboard())


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('waiting_for_coords', False))
def handle_coords_input(message):
    try:
        chat_id = message.chat.id
        coords = message.text.strip()

        # Разбиваем координаты на отдельные значения
        coord_parts = [part.strip() for part in coords.split(',')]

        # Проверяем, что у нас ровно 2 координаты и они числа
        if len(coord_parts) != 2 or not all(part.isdigit() for part in coord_parts):
            raise ValueError("Неверный формат координат")

        # Преобразуем в числа и сохраняем отдельно X и Y
        operation_zone_x = int(coord_parts[0])
        operation_zone_y = int(coord_parts[1])

        user_states[chat_id]['operation_zone_x'] = operation_zone_x
        user_states[chat_id]['operation_zone_y'] = operation_zone_y
        user_states[chat_id]['waiting_for_coords'] = False
        user_states[chat_id]['waiting_for_shelf_size'] = True

        bot.send_message(
            chat_id,
            "Отлично! Теперь введите размер стеллажа в пикселях (одно число):",
            reply_markup=types.ReplyKeyboardRemove(selective=True)
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке координат: {e}")
        bot.reply_to(
            message,
            "Неправильный формат координат. Пожалуйста, введите координаты в формате:\n"
            "X1,Y1\n"
            "Например: 100,200"
        )




@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('waiting_for_shelf_size', False))
def handle_shelf_size_input(message):
    try:
        chat_id = message.chat.id
        shelf_size = int(message.text.strip())

        user_states[chat_id]['shelf_size'] = shelf_size
        user_states[chat_id]['waiting_for_shelf_size'] = False

        # Получаем все сохраненные данные
        image_path = user_states[chat_id]['image_path']
        operation_zone_x = user_states[chat_id]['operation_zone_x']
        operation_zone_y = user_states[chat_id]['operation_zone_y']

        bot.send_message(
            chat_id,
            "✅ Все данные получены! Начинаю создание топологии склада... Что бы получить файл нажмите кнопку: Получить мой файл",
            reply_markup=create_reply_keyboard()
        )

        # Формируем сообщение с результатами
        result_message = (
            "Полученные данные:\n"
            f"Координаты операционной зоны:\n"
            f"X: {operation_zone_x}\n"
            f"Y: {operation_zone_y}\n"
            f"Размер стеллажа: {shelf_size} пикселей"
        )

        bot.send_message(chat_id, result_message)
        build_grid(chat_id, shelf_size, operation_zone_x, operation_zone_y, image_path)


    except Exception as e:
        logger.error(f"Ошибка при обработке размера стеллажа: {e}")
        bot.reply_to(
            message,
            "Неправильный формат размера. Пожалуйста, введите одно число (размер стеллажа в пикселях):"
        )


@bot.message_handler(func=lambda message: message.text in ['Что делает этот бот?', 'Требования к файлу'])
def handle_hints(message):
    if message.text == 'Что делает этот бот?':
        response = """Я - бот от Яндекса. Я принимаю и создаю топологию склада для наиболее оптимальной работы роботизированного склада."""
    elif message.text == 'Требования к файлу':
        response = """Требования к изображению:
- Формат: JPG или PNG (будет сохранено как PNG)
- Размер: не более 10 МБ
- Минимальное разрешение: 1280x720
- Удалите лишние детали"""

    bot.send_message(message.chat.id, response, reply_markup=create_reply_keyboard())


if __name__ == '__main__':
    logger.info("Бот запущен")
    bot.polling(none_stop=True)
