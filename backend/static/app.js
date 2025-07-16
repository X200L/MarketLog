document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    let uploadedFileName = null; // Переменная для хранения имени загруженного файла
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(uploadForm);
            const responseDiv = document.getElementById('response');

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();

                if (result.error) {
                    responseDiv.className = 'error';
                    responseDiv.textContent = 'Ошибка: ' + result.error;
                } else {
                    // Сохраняем имя загруженного файла
                    const fileInput = document.getElementById('fileInput');
                    if (fileInput && fileInput.files.length > 0) {
                        uploadedFileName = fileInput.files[0].name;
                    }
                    
                    const sidebar = document.querySelector('.sidebar');
                    if (sidebar) {
                        sidebar.innerHTML = `
                            <div class="logotip">

                                <a href="templates/index.html"><img src="static/images/yandex_icon.svg.png" class="logo"></a>
                                <span class="title">Топология</span>
                            </div>
                            <div class="zones file-section">
                                <div class="inputs">
                                    <p>Операционная зона</p>
                                    <input type="number" placeholder=" " class="size">
                                    <p type="mult" style="margin: 0 4px 0 4px;">×</p>
                                    <input type="number" placeholder=" " class="size">
                                </div>
                            </div>
                            <div class="robot file-section">
                                <div class="inputs">
                                    <p>Размеры стелажа</p>
                                    <input type="number" placeholder=" " class="size">
                                </div>
                            </div>
                            <div class="zones file-section">
                            </div>
                            <button class="upload-btn build-btn" style="margin-top:24px;">Построить сетку</button>
                            <button class="upload-btn download-btn" style="background:#f2f2f2; color:#111;">Скачать файл</button>
                        `;
                        
                        // Добавляем обработчики для новых кнопок
                        const clearRobotBtn = sidebar.querySelector('#clearRobotBtn');
                        if (clearRobotBtn) {
                            clearRobotBtn.addEventListener('click', function() {
                                const robotInputs = sidebar.querySelectorAll('.robot .size');
                                robotInputs.forEach(input => input.value = '');
                            });
                        }
                        const buildBtn = sidebar.querySelector('.build-btn');
                        if (buildBtn) {
                            buildBtn.addEventListener('click', async function() {
                                if (!uploadedFileName) {
                                    alert('Сначала загрузите изображение');
                                    return;
                                }
                                // Получаем значения из input'ов
                                const inputs = sidebar.querySelectorAll('.size');
                                const operation_zone_x = inputs[0] ? parseInt(inputs[0].value) : 350;
                                const operation_zone_y = inputs[1] ? parseInt(inputs[1].value) : 150;
                                const robot_size = inputs[2] ? parseInt(inputs[2].value) : 30;

                                buildBtn.disabled = true;
                                buildBtn.textContent = 'Обработка...';
                                try {
                                    const response = await fetch('/build-grid', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                        body: JSON.stringify({
                                            filename: uploadedFileName,
                                            operation_zone_x: operation_zone_x,
                                            operation_zone_y: operation_zone_y,
                                            robot_size: robot_size
                                        })
                                    });
                                    const result = await response.json();
                                    if (result.error) {
                                        alert('Ошибка: ' + result.error);
                                    } else {
                                        if (result.images && Array.isArray(result.images)) {
                                            showImageGrid(result.images);
                                        } else if (result.processed_filename) {
                                            showProcessedImage(result.processed_filename);
                                        }
                                    }
                                } catch (error) {
                                    alert('Ошибка соединения при построении сетки');
                                } finally {
                                    buildBtn.disabled = false;
                                    buildBtn.textContent = 'Построить сетку';
                                }
                            });
                        }
                    }
                }
            } catch (error) {
                responseDiv.className = 'error';
                responseDiv.textContent = 'Ошибка соединения';
            }
        });
    }

    const fileInput = document.getElementById('fileInput');
    const fileNameSpan = document.getElementById('fileName');
    const fileBtn = document.getElementById('fileBtn');
    const clearFileBtn = document.getElementById('clearFileBtn');

    function updateClearBtnVisibility() {
        if (fileInput && clearFileBtn) {
            clearFileBtn.style.display = fileInput.files.length > 0 ? 'block' : 'none';
        }
    }

    if (fileInput && fileNameSpan) {
        fileInput.addEventListener('change', function() {
            if (fileInput.files.length > 0) {
                fileNameSpan.textContent = fileInput.files[0].name;
                showImagePreview(fileInput.files[0]);
            } else {
                fileNameSpan.textContent = 'Выберите файл';
                resetImagePreview();
            }
            updateClearBtnVisibility();
        });
    }

    if (fileBtn && fileInput) {
        fileBtn.addEventListener('click', function() {
            fileInput.click();
        });
    }

    if (clearFileBtn && fileInput && fileNameSpan) {
        clearFileBtn.addEventListener('click', function() {
            fileInput.value = '';
            fileNameSpan.textContent = 'Выберите файл';
            resetImagePreview();
            updateClearBtnVisibility();
        });
    }

    function showImagePreview(file) {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = function(e) {
            const mainDiv = document.querySelector('.main');
            if (mainDiv) {
                mainDiv.innerHTML = `
                    <div class=\"image-preview\">
                        <img src=\"${e.target.result}\" alt=\"Preview\" style=\"max-width:100%; max-height:100%; display:block; margin:auto;\">
                    </div>
                `;
            }
        };
        reader.readAsDataURL(file);
    }

    function resetImagePreview() {
        const mainDiv = document.querySelector('.main');
        if (mainDiv) {
            mainDiv.innerHTML = `
                <div class=\"fon\">
                    <img src=\"static/images/folder.png\" class=\"fon_folder\">
                    <p class=\"fon_text\">Загрузите изображение</p>
                </div>
            `;
        }
    }

    function showProcessedImage(filename) {
        const mainDiv = document.querySelector('.main');
        if (mainDiv) {
            mainDiv.innerHTML = `
                <div class="image-preview">
                    <img src="/uploads/${filename}" alt="Processed Image" style="max-width:100%; max-height:100%; display:block; margin:auto;">
                </div>
            `;
        }
    }

    function showImageGrid(images) {
        const mainDiv = document.querySelector('.main');
        if (mainDiv) {
            let html = '<div class="image-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;">';
            images.forEach((img, idx) => {
                html += `<div class="image-grid-item"><img src="${img}" alt="${img}" data-idx="${idx}" style="width:100%;border-radius:8px;box-shadow:0 2px 8px #0001; cursor:pointer;"></div>`;
            });
            html += '</div>';
            mainDiv.innerHTML = html;

            // Добавляем обработчик клика по изображениям
            const gridImages = mainDiv.querySelectorAll('.image-grid-item img');
            gridImages.forEach(imgEl => {
                imgEl.addEventListener('click', function() {
                    const idx = imgEl.getAttribute('data-idx');
                    openImageModal(images[idx], idx);
                });
            });
        }
    }

    // Модальное окно
    function openImageModal(imgSrc, idx) {
        const modal = document.getElementById('imageModal');
        const mainImg = document.getElementById('modalMainImg');
        const heatmapImg = document.getElementById('modalHeatmapImg');
        if (modal && mainImg && heatmapImg) {
            mainImg.src = imgSrc;
            heatmapImg.src = `/heatmaps/heatmap${idx}.png`;
            modal.style.display = 'flex';
        }
    }

    function closeImageModal() {
        const modal = document.getElementById('imageModal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    // Навешиваем обработчик на крестик закрытия модального окна
    const closeModalBtn = document.getElementById('closeModal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeImageModal);
    }
    // Закрытие по клику вне контента
    const imageModal = document.getElementById('imageModal');
    if (imageModal) {
        imageModal.addEventListener('click', function(e) {
            if (e.target === imageModal) {
                closeImageModal();
            }
        });
    }

    resetImagePreview();
    updateClearBtnVisibility();
});
