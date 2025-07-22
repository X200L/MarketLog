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
bot_token = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = telebot.TeleBot(bot_token)
import threading
import threading
import queue

# Очередь запросов и блокировка
request_queue = queue.Queue()
processing_lock = threading.Lock()
current_processing = None


processing_lock = threading.Lock()
current_processing = None
user_in_queue = set()  # Множество для отслеживания пользователей в очереди

def process_queue():
    global current_processing
    while True:
        # Получаем запрос из очереди
        task = request_queue.get()
        chat_id, shelf_size, op_x, op_y, img_path = task

        # Уведомляем пользователя о начале обработки
        bot.send_message(chat_id, "🔔 Ваш запрос взят в обработку.")

        # Помечаем текущий обрабатываемый запрос
        with processing_lock:
            current_processing = chat_id
            # Удаляем пользователя из множества ожидающих
            if chat_id in user_in_queue:
                user_in_queue.remove(chat_id)

        # Выполняем обработку
        try:
            build_grid(chat_id, shelf_size, op_x, op_y, img_path)
        except Exception as e:
            logger.error(f"Ошибка обработки для {chat_id}: {e}")
            bot.send_message(chat_id, "❌ Произошла ошибка при обработке")

        # Очищаем текущий запрос
        with processing_lock:
            current_processing = None

        # Помечаем задачу как выполненную
        request_queue.task_done()

# Запускаем обработчик очереди в отдельном потоке
threading.Thread(target=process_queue, daemon=True).start()
# Глобальная блокировка для системы очередей
build_grid_lock = threading.Lock()


def build_grid(chat_id, shelf_size, operation_zone_x, operation_zone_y, image_path):
    try:
        # Оригинальная обработка
        filename = image_path.replace('\\', '/')
        robot_size = shelf_size
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file_path = '/'.join(filename.split('/')[:-1])
        image_name = filename.split('/')[-1]

        processor = ImageProcessor(app.config['UPLOAD_FOLDER'])
        processed_filename = processor.process_file(file_path, image_name)
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)

        starter(
            processed_path,
            operation_zone_x,
            operation_zone_y,
            robot_size,
            chat_id,
            temp_upload_folder=app.config['TEMP_UPLOAD_FOLDER']
        )

        # Подготовка медиагруппы
        temp_dir = app.config['TEMP_UPLOAD_FOLDER']
        media_group = []
        sent_files = 0
        file_objects = []  # To keep track of open file objects

        try:
            for i in range(6):
                img_path = os.path.join(temp_dir, f'warehouse_roads{i}.png')
                if os.path.exists(img_path):
                    img_file = open(img_path, 'rb')  # Open the file
                    file_objects.append(img_file)  # Keep track of it

                    # Добавляем фото в медиагруппу
                    if i == 0:
                        media_group.append(types.InputMediaPhoto(img_file, caption=f"✅ Готово! Варианты карт склада\nКоординаты: X={operation_zone_x}, Y={operation_zone_y}\nРазмер стеллажа: {shelf_size}"))

                    else:
                        media_group.append(types.InputMediaPhoto(img_file))

                    sent_files += 1

            if media_group:
                # Отправляем все картинки одним сообщением
                bot.send_media_group(chat_id, media_group)

                # Если нужно добавить дополнительное сообщение
                if sent_files == 6:
                    bot.send_message(chat_id, "Выберите наиболее подходящий вариант из предложенных!", reply_markup=create_reply_keyboard())
            else:
                bot.send_message(chat_id, "❌ Не удалось сгенерировать карты дорог.", reply_markup=create_reply_keyboard())
        finally:
            # Close all file objects when done
            for file_obj in file_objects:
                try:
                    file_obj.close()
                except:
                    pass

    except Exception as e:
        logger.error(f"Ошибка в build_grid: {e}")
        with processing_lock:
            if chat_id in user_in_queue:
                user_in_queue.remove(chat_id)
        bot.send_message(chat_id, "❌ Ошибка обработки. Проверьте входные данные или Вы отправили картинку, которую невозможно обработать.", reply_markup=create_reply_keyboard())
logger = logging.getLogger(__name__)



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
    btn4 = types.KeyboardButton('Посмотреть примеры')  # Новая кнопка
    markup.add(btn1, btn2, btn3, btn4)
    return markup
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

# Добавляем обработчик для отправки последнего загруженного файла
# Добавляем обработчик для отправки примеров с кнопками
@bot.message_handler(func=lambda message: message.text == 'Посмотреть примеры')
def send_example_file(message):
    try:
        chat_id = message.chat.id
        example_dir = 'Example'

        # Пример 1
        example_file1 = 'Zavod3.png'
        example_path1 = os.path.join(example_dir, example_file1)
        # Пример 2
        example_file2 = 'Zavod2.png'
        example_path2 = os.path.join(example_dir, example_file2)

        if not os.path.exists(example_path1) or not os.path.exists(example_path2):
            bot.reply_to(message, "Примеры файлов не найдены", reply_markup=create_reply_keyboard())
            return



        markup2 = types.InlineKeyboardMarkup()
        btn_use2 = types.InlineKeyboardButton(
            "Использовать этот пример",
            callback_data=f"use_example:{example_file2}:500:500:20"
        )
        markup2.add(btn_use2)

        # Отправляем примеры с кнопками


        with open(example_path2, 'rb') as file:
            bot.send_photo(
                chat_id,
                file,
                caption="Пример склада: X=500, Y=500, Размер стеллажа=20",
                reply_markup=markup2
            )

    except Exception as e:
        logger.error(f"Ошибка при отправке примеров: {e}")
        bot.reply_to(message, "Произошла ошибка при отправке примеров", reply_markup=create_reply_keyboard())


# Обработчик нажатия на кнопку использования примера
@bot.callback_query_handler(func=lambda call: call.data.startswith('use_example'))
def handle_use_example(call):
    try:
        chat_id = call.message.chat.id

        # Проверяем, не находится ли пользователь уже в очереди
        with processing_lock:
            if chat_id in user_in_queue or chat_id == current_processing:
                bot.answer_callback_query(
                    call.id,
                    "⏳ Ваш предыдущий запрос уже в обработке. Дождитесь его завершения.",
                    show_alert=True
                )
                return

            # Добавляем пользователя в множество ожидающих
            user_in_queue.add(chat_id)

        _, filename, op_x, op_y, shelf_size = call.data.split(':')

        # Полный путь к файлу примера
        example_path = os.path.join('Example', filename)

        # Конвертируем в PNG если нужно
        png_path = convert_to_png(example_path)

        # Копируем файл в папку загрузок
        new_filename = f"example_{chat_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        new_path = os.path.join(UPLOAD_FOLDER, new_filename)

        # Создаем папку если не существует
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        # Копируем файл
        with open(png_path, 'rb') as src, open(new_path, 'wb') as dst:
            dst.write(src.read())

        # Добавляем запрос в очередь как обычный запрос
        request_queue.put((chat_id, int(shelf_size), int(op_x), int(op_y), new_path))

        # Уведомляем пользователя
        bot.answer_callback_query(call.id, "✅ Пример добавлен в очередь обработки!")

        # Сообщаем о позиции в очереди
        with processing_lock:
            queue_size = request_queue.qsize()
            if current_processing:
                # Показываем queue_size-1, так как один элемент уже в обработке
                position = max(1, queue_size - 1)
                bot.send_message(
                    chat_id,
                    f"⏳ Ваш запрос добавлен в очередь. Сейчас обрабатывается запрос другого пользователя. "
                    f"Ваше место в очереди: {position}"
                )
            else:
                bot.send_message(chat_id, "⏳ Ваш запрос принят. Ожидайте...")

    except Exception as e:
        logger.error(f"Ошибка обработки примера: {e}")
        with processing_lock:
            if chat_id in user_in_queue:
                user_in_queue.remove(chat_id)
        bot.answer_callback_query(call.id, "❌ Ошибка обработки примера!")
        bot.send_message(chat_id, "Произошла ошибка при обработке примера")

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


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('waiting_for_coords', False))
def handle_coords_input(message):
    chat_id = message.chat.id
    coords = message.text.strip()

    try:
        # Разбиваем координаты на отдельные значения
        coord_parts = [part.strip() for part in coords.split(',')]

        # Проверяем, что у нас ровно 2 координаты и они числа
        if len(coord_parts) != 2 or not all(part.isdigit() for part in coord_parts):
            raise ValueError("Неверный формат координат")

        # Преобразуем в числа
        operation_zone_x = int(coord_parts[0])
        operation_zone_y = int(coord_parts[1])

        # Проверяем, что координаты положительные
        if operation_zone_x < 0 or operation_zone_y < 0:
            raise ValueError("Координаты не могут быть отрицательными")

        # Сохраняем координаты
        user_states[chat_id]['operation_zone_x'] = operation_zone_x
        user_states[chat_id]['operation_zone_y'] = operation_zone_y
        user_states[chat_id]['waiting_for_coords'] = False
        user_states[chat_id]['waiting_for_shelf_size'] = True

        bot.send_message(
            chat_id,
            "✅ Координаты приняты!\n\n"
            "Теперь введите размер стеллажа в пикселях (одно число):",
            reply_markup=types.ReplyKeyboardRemove(selective=True)
        )

    except Exception as e:
        logger.error(f"Ошибка при обработке координат: {e}")
        # Оставляем состояние waiting_for_coords = True
        user_states[chat_id]['waiting_for_coords'] = True

        bot.send_message(
            chat_id,
            "❌ Неправильный формат координат!\n\n"
            "Пожалуйста, введите координаты операционной зоны в пикселях в формате:\n"
            "<b>X,Y</b>\n"
            "Например: <b>100,200</b>\n\n"
            "Убедитесь, что:\n"
            "1. Используете запятую как разделитель\n"
            "2. Вводите только числа\n"
            "3. Координаты не отрицательные",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке координат: {e}")
        # Оставляем состояние waiting_for_coords = True
        user_states[chat_id]['waiting_for_coords'] = True

        bot.send_message(
            chat_id,
            "❌ Неправильный формат координат!\n\n"
            "Пожалуйста, введите координаты операционной зоны в пикселях в формате:\n"
            "<b>X,Y</b>\n"
            "Например: <b>100,200</b>\n\n"
            "Убедитесь, что:\n"
            "1. Используете запятую как разделитель\n"
            "2. Вводите только числа\n"
            "3. Координаты не отрицательные",
            parse_mode='HTML'
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

def allowed_file(filename):
    """Проверяет, что расширение файла разрешено"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('waiting_for_shelf_size', False))
def handle_shelf_size_input(message):
    try:
        chat_id = message.chat.id

        # Проверяем, не находится ли пользователь уже в очереди
        with processing_lock:
            if chat_id in user_in_queue or chat_id == current_processing:
                bot.send_message(
                    chat_id,
                    "⏳ Ваш предыдущий запрос уже в обработке или ожидает в очереди. "
                    "Пожалуйста, дождитесь его завершения."
                )
                return

            # Добавляем пользователя в множество ожидающих
            user_in_queue.add(chat_id)

        try:
            shelf_size = int(message.text.strip())
            user_states[chat_id]['shelf_size'] = shelf_size
            user_states[chat_id]['waiting_for_shelf_size'] = False

            # Получаем все сохраненные данные
            image_path = user_states[chat_id]['image_path']
            operation_zone_x = user_states[chat_id]['operation_zone_x']
            operation_zone_y = user_states[chat_id]['operation_zone_y']

            # Добавляем запрос в очередь
            request_queue.put((chat_id, shelf_size, operation_zone_x, operation_zone_y, image_path))

            # Сообщаем пользователю о постановке в очередь
            with processing_lock:
                queue_size = request_queue.qsize()
                if current_processing:
                    # Показываем queue_size-1, так как один элемент уже в обработке
                    position = max(1, queue_size - 1)
                    bot.send_message(
                        chat_id,
                        f"⏳ Ваш запрос добавлен в очередь. Сейчас обрабатывается запрос другого пользователя. "
                        f"Ваше место в очереди: {position}"
                    )
                else:
                    bot.send_message(chat_id, "⏳ Ваш запрос принят. Ожидайте...")

        except ValueError:
            raise ValueError("Неправильный формат размера")
        except Exception as e:
            raise Exception("Ошибка при обработке запроса")

    except ValueError as e:
        with processing_lock:
            if chat_id in user_in_queue:
                user_in_queue.remove(chat_id)
        bot.reply_to(
            message,
            "Неправильный формат размера. Пожалуйста, введите одно число (размер стеллажа в пикселях)."
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке размера стеллажа: {e}")
        with processing_lock:
            if chat_id in user_in_queue:
                user_in_queue.remove(chat_id)
        bot.reply_to(
            message,
            "Произошла ошибка. Пожалуйста, попробуйте еще раз."
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

