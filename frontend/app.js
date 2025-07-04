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
                    responseDiv.className = 'success';
                    responseDiv.textContent = 'Успешно: ' + result.message;
                }
            } catch (error) {
                responseDiv.className = 'error';
                responseDiv.textContent = 'Ошибка соединения';
            }
        });
    }
ы
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
