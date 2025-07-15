import cv2
import numpy as np
from flask import Flask, request, send_file, render_template_string
import os
from io import BytesIO
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
 # увеличение толщины линии если она слишклм тонкая
def thicken_and_color_image(img, max_distance=3, thickness=2):
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    kernel_size = max_distance * 2 + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    connected = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    
    if thickness > 1:
        thick_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness, thickness))
        connected = cv2.dilate(connected, thick_kernel, iterations=1)
    
 
    # заливка контуров и полостей соответствующими цветаами
    contours, _ = cv2.findContours(connected, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    result = np.ones((gray.shape[0], gray.shape[1], 3), dtype=np.uint8) * 255
    fill_mask = np.zeros_like(connected)
    
    for cnt in contours:
        cv2.drawContours(fill_mask, [cnt], -1, 255, -1)
    
    result[fill_mask == 255] = [255, 0, 0]
    result[connected == 255] = [0, 0, 255]
    
    return result


 
 # для проверки работы, можно удалять
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Файл не выбран", 400
            
        file = request.files['file']
        if file.filename == '':
            return "Файл не выбран", 400
 
        try:
            img_bytes = file.read()
            img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
            result = thicken_and_color_image(img, max_distance=3, thickness=2)
            
            is_success, buffer = cv2.imencode(".jpg", result)
            if not is_success:
                return "Ошибка обработки изображения", 500
                
            mem_file = BytesIO(buffer)
            mem_file.seek(0)
            
            return send_file(
                mem_file,
                mimetype='image/jpg',
                as_attachment=True,
                download_name='processed_image.jpg'
            )
            
        except Exception as e:
            return f"Ошибка обработки: {str(e)}", 500





 
 # для меня чтобы я могла проверить работу модели
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Обработка контуров</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }
            .upload-box {
                border: 2px dashed #ccc;
                padding: 30px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .btn {
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
                transition: background-color 0.3s;
            }
            .btn:hover {
                background-color: #45a049;
            }
            .instructions {
                text-align: left;
                margin: 20px 0;
                padding: 20px;
                background-color: #f8f9fa;
                border-radius: 5px;
            }
            .color-legend {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 15px 0;
                flex-wrap: wrap;
            }
            .color-item {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .color-box {
                width: 20px;
                height: 20px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
        </style>
    </head>
    <body>
        <h1>Обработка контуров</h1>
        <p>Загрузите изображение с черными линиями</p>
        
        <div class="upload-box">
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*" required
                       style="margin-bottom: 15px; width: 100%; max-width: 300px;">
                <br>
                <button type="submit" class="btn">Обработать изображение</button>
            </form>
        </div>
        
        <div class="instructions">
            <h3>Инструкция:</h3>
            <ol>
                <li>Загрузите изображение с черными линиями</li>
                <li>Нажмите кнопку "Обработать изображение"</li>
                <li>Скачайте результат:
                    <ul>
                        <li>Линии станут толще и красными</li>
                        <li>Замкнутые области зальются синим</li>
                        <li>Фон останется белым</li>
                    </ul>
                </li>
            </ol>
            
            <div class="color-legend">
                <div class="color-item">
                    <div class="color-box" style="background-color: red;"></div>
                    <span>Линии (станут красными)</span>
                </div>
                <div class="color-item">
                    <div class="color-box" style="background-color: blue;"></div>
                    <span>Заливка областей</span>
                </div>
                <div class="color-item">
                    <div class="color-box" style="background-color: white; border: 1px solid black;"></div>
                    <span>Фон</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    ''')
 
if __name__ == '__main__':
    app.run(debug=True)