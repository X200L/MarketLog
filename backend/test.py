import cv2
import numpy as np
import os

# Папка для загрузки и сохранения файлов
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class ImageProcessor:
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def process_image(self, img):
        """Обработка изображения - выделение контуров и заливка областей"""
        # Преобразование в оттенки серого
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Бинаризация
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        
        # Поиск контуров
        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # Создание результата
        result = np.ones((gray.shape[0], gray.shape[1], 3), dtype=np.uint8) * 255
        
        # Создание маски для заливки
        fill_mask = np.zeros_like(gray)
        
        # Заливка всех замкнутых областей синим цветом
        for cnt in contours:
            cv2.drawContours(fill_mask, [cnt], -1, 255, -1)
        
        # Применение синей заливки
        result[fill_mask == 255] = [255, 0, 0]  
        
        # Применение красных контуров
        result[binary == 255] = [0, 0, 255] 
        
        return result
    
    def process_file(self, filename):
        """Обработка файла по имени из папки uploads"""
        # Полный путь к входному файлу
        input_path = os.path.join(self.upload_folder, filename)
        
        # Проверка существования файла
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Файл {filename} не найден в папке {self.upload_folder}")
        
        # Чтение изображения
        img = cv2.imread(input_path)
        if img is None:
            raise ValueError(f"Не удалось прочитать изображение {filename}")
        
        # Обработка изображения
        result = self.process_image(img)
        
        # Создание имени для обработанного файла
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_processed{ext}"
        output_path = os.path.join(self.upload_folder, output_filename)
        
        # Сохранение результата
        success = cv2.imwrite(output_path, result)
        if not success:
            raise RuntimeError(f"Не удалось сохранить обработанное изображение {output_filename}")
        
        return output_filename

# Пример использования
if __name__ == '__main__':
    # Создание экземпляра процессора
    processor = ImageProcessor(UPLOAD_FOLDER)
    
    # Пример обработки файла
    try:
        # Замените 'example.jpg' на реальное имя файла в папке uploads
        processed_filename = processor.process_file('example.jpg')
        print(f"Файл успешно обработан: {processed_filename}")
    except Exception as e:
        print(f"Ошибка: {e}")