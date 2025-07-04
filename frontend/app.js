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
});
document.getElementById('fileBtn').onclick = function() {
    document.getElementById('fileInput').click();
};
document.getElementById('fileInput').onchange = function() {
    const file = this.files[0];
    document.getElementById('fileName').textContent = file ? file.name : 'Выберите файл';
};