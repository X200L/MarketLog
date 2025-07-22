import os
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('Agg')
from matplotlib import colors
from matplotlib.patches import Circle, Rectangle
from flask import Flask, render_template, jsonify
import numpy as np
import time
import threading
import queue

app = Flask(__name__)

# Конфигурация для уменьшения размера изображений
mpl.rcParams['savefig.dpi'] = 72
mpl.rcParams['figure.figsize'] = (8, 6)
mpl.rcParams['font.size'] = 10

# Глобальное состояние для потоковой обработки
file_processor = None
file_lock = threading.Lock()

class FileProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.mtime = os.path.getmtime(filename)
        self.matrices = []
        self.robots_positions = []
        self.numeric_matrices = []
        self.total_frames = 0
        self.processing_complete = False
        self.queue = queue.Queue()
        self.frame_queue = queue.Queue(maxsize=20)
        self.stop_event = threading.Event()
        
        self.thread = threading.Thread(target=self.process_file)
        self.thread.daemon = True
        self.thread.start()
        
        self.generator_thread = threading.Thread(target=self.frame_generator)
        self.generator_thread.daemon = True
        self.generator_thread.start()
    
    def process_file(self):
        """Потоковая обработка файла"""
        try:
            with open(self.filename, 'r') as file:
                content = file.read()
            
            matrix_blocks = content.split("- "*33 + "\n")[:-1]
            
            for block in matrix_blocks:
                if self.stop_event.is_set():
                    return
                
                lines = block.strip().split('\n')
                matrix = []
                robots_pos = []
                for i, line in enumerate(lines):
                    row = line.split()
                    matrix.append(row)
                    for j, char in enumerate(row):
                        if char in ['R', 'S']:  # Обрабатываем оба типа роботов
                            robots_pos.append((i, j, char))
                
                self.queue.put((matrix, robots_pos))
            
            self.processing_complete = True
        except Exception as e:
            print(f"Ошибка обработки файла: {str(e)}")
    
    def frame_generator(self):
        """Генерация кадров в фоновом режиме"""
        frame_idx = 0
        while not self.stop_event.is_set():
            try:
                matrix, robots_pos = self.queue.get(timeout=0.5)
                
                # Создаем числовую матрицу
                char_to_num = {'0':0, '1':1, '2':2, '%':3, 'R':0, 'S':0}
                numeric_matrix = np.array(
                    [[char_to_num[char] for char in row] for row in matrix],
                    dtype=np.uint8
                )
                
                # Генерируем кадр
                frame_data = self.generate_frame(numeric_matrix, robots_pos, frame_idx)
                
                # Сохраняем данные
                self.matrices.append(matrix)
                self.robots_positions.append(robots_pos)
                self.numeric_matrices.append(numeric_matrix)
                self.total_frames += 1
                frame_idx += 1
                
                self.frame_queue.put((frame_idx, frame_data))
            except queue.Empty:
                if self.processing_complete:
                    break
            except Exception as e:
                print(f"Ошибка генерации кадра: {str(e)}")
    
    def generate_frame(self, numeric_matrix, robots_pos, frame_idx):
        """Генерация одного кадра"""
        fig, ax = plt.subplots()
        
        # Цветовая карта
        cmap = colors.ListedColormap(['white', 'black', 'brown', 'yellow'])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        
        img = ax.imshow(numeric_matrix, cmap=cmap, norm=norm)
        ax.set_xlim(-0.5, numeric_matrix.shape[1] - 0.5)
        ax.set_ylim(numeric_matrix.shape[0] - 0.5, -0.5)
        
        # Отрисовка роботов
        for i, j, char in robots_pos:
            if char == 'R':
                # Обычный робот - синий круг
                circle = Circle((j, i), 0.3, fill=True, color='blue')
                ax.add_patch(circle)
            elif char == 'S':
                # Робот со стеллажом - коричневый квадрат
                rect = Rectangle(
                    (j - 0.2, i - 0.2),  # Позиция (центрированная)
                    0.4, 0.4,             # Размер
                    fill=True, 
                    color='brown',        # Цвет стеллажа
                    edgecolor='none'      # Без границы
                )
                ax.add_patch(rect)
        
        plt.title(f'Кадр {frame_idx + 1}', fontsize=10)
        
        # Сохраняем изображение
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.05)
        plt.close(fig)
        
        return base64.b64encode(buf.getvalue()).decode('utf-8')
    
    def get_ready_frames(self):
        """Получение готовых кадров"""
        frames = {}
        while not self.frame_queue.empty():
            frame_idx, frame_data = self.frame_queue.get()
            frames[frame_idx] = frame_data
        return frames
    
    def stop(self):
        """Остановка обработки"""
        self.stop_event.set()
        self.thread.join(timeout=1.0)
        self.generator_thread.join(timeout=1.0)

def get_file_processor():
    """Получение или создание обработчика файла"""
    global file_processor
    with file_lock:
        filename = "out.txt"
        if not os.path.exists(filename):
            return None
        
        mtime = os.path.getmtime(filename)
        
        if file_processor is None or file_processor.mtime != mtime:
            if file_processor:
                file_processor.stop()
            file_processor = FileProcessor(filename)
        
        return file_processor

@app.route('/')
def animation():
    try:
        processor = get_file_processor()
        if not processor:
            return "Ошибка: файл 'out.txt' не найден"
        
        # Ждем первый кадр
        start_time = time.time()
        while processor.total_frames == 0 and time.time() - start_time < 5.0:
            time.sleep(0.1)
        
        if processor.total_frames == 0:
            return "Ошибка: не удалось загрузить кадры"
        
        return render_template('animation.html', 
                              interval=250,
                              batch_size=5)
    
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

@app.route('/ready_frames')
def get_ready_frames():
    try:
        processor = get_file_processor()
        if not processor:
            return jsonify({"error": "File processor not available"}), 503
        
        frames = processor.get_ready_frames()
        return jsonify({
            "frames": frames,
            "total_frames": processor.total_frames,
            "complete": processor.processing_complete
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/frame/<int:frame_index>')
def get_frame(frame_index):
    try:
        processor = get_file_processor()
        if not processor:
            return jsonify({"error": "File processor not available"}), 503
        
        if frame_index < 0 or frame_index >= processor.total_frames:
            return jsonify({"error": "Invalid frame index"}), 404
        
        # Если кадр уже сгенерирован
        if frame_index < len(processor.numeric_matrices):
            frame_data = processor.generate_frame(
                processor.numeric_matrices[frame_index],
                processor.robots_positions[frame_index],
                frame_index
            )
            return jsonify({
                "image": frame_data,
                "frame": frame_index + 1,
                "total": processor.total_frames
            })
        
        return jsonify({"error": "Frame not ready"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=True, port=5001)
    finally:
        if file_processor:
            file_processor.stop()