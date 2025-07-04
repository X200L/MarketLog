document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
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
                    const sidebar = document.querySelector('.sidebar');
                    if (sidebar) {
                        sidebar.innerHTML = `
                            <div class="logotip">
                                <img src="static/images/yandex_icon.svg.png" class="logo">
                                <span class="title">Топология</span>
                            </div>
                            <div class="zones file-section">
                                <div class="inputs">
                                    <p>Операционные зоны</p>
                                    <input type="number" placeholder=" " class="size">
                                </div>
                            </div>
                            <div class="robot file-section">
                                <div class="inputs">
                                    <p>Размеры робота</p>
                                    <input type="number" placeholder=" " class="size">
                                    <button type="button" id="clearRobotBtn" style="margin: 0 4px 0 4px;">×</button>
                                    <input type="number" placeholder=" " class="size">
                                </div>
                            </div>
                            <button class="upload-btn build-btn" style="margin-top:24px;">Построить сетку</button>
                            <button class="upload-btn download-btn" style="background:#f2f2f2; color:#111;">Скачать файл</button>
                        `;
                        const clearRobotBtn = sidebar.querySelector('#clearRobotBtn');
                        if (clearRobotBtn) {
                            clearRobotBtn.addEventListener('click', function() {
                                const robotInputs = sidebar.querySelectorAll('.robot .size');
                                robotInputs.forEach(input => input.value = '');
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

    resetImagePreview();
    updateClearBtnVisibility();
});
