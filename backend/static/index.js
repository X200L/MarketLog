window.lcImages = JSON.parse(document.getElementById('lcImagesData').textContent);
window.lcHeatmaps = JSON.parse(document.getElementById('lcHeatmapsData').textContent);
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            window.location.href = '/logout';
        });
    }

    // Только для страницы с сеткой топологий
    const topologyGrid = document.querySelector('.topology-grid');
    if (!topologyGrid) return;
    // Получаем данные из data-атрибутов, если нужно, или из глобальных переменных, если шаблон их оставляет
    let images = window.lcImages || [];
    let heatmaps = window.lcHeatmaps || [];
    // Если переменных нет, пробуем собрать из DOM
    if (!images.length) {
        images = Array.from(document.querySelectorAll('.topology-grid-item img')).map(img => img.getAttribute('src'));
    }
    // Для heatmaps нужен серверный рендеринг, иначе оставить пустым
    // Навешиваем обработчики
    const gridImages = document.querySelectorAll('.topology-grid-item img');
    gridImages.forEach(function(imgEl) {
        imgEl.addEventListener('click', function() {
            const idx = imgEl.getAttribute('data-idx');
            openImageModal(images[idx], heatmaps[idx], idx);
        });
    });
    function openImageModal(imgSrc, heatmapSrc, idx) {
        const modal = document.getElementById('imageModal');
        const mainImg = document.getElementById('modalMainImg');
        const heatmapImg = document.getElementById('modalHeatmapImg');
        const downloadJsonBtn = document.getElementById('downloadJsonBtn');
        const runSimulationBtn = document.getElementById('runSimulationBtn');
        if (modal && mainImg && heatmapImg && downloadJsonBtn && runSimulationBtn) {
            mainImg.src = imgSrc;
            heatmapImg.src = heatmapSrc;
            let jsonPath = '';
            if (heatmapSrc && heatmapSrc.includes('heatmaps/heatmap')) {
                jsonPath = heatmapSrc.replace('heatmaps/heatmap', 'graph/graph').replace('.png', '.json');
            } else {
                jsonPath = `graph/graph${idx}.json`;
            }
            downloadJsonBtn.href = jsonPath;
            downloadJsonBtn.setAttribute('download', `graph${idx}.json`);
            runSimulationBtn.onclick = function() {
                // Здесь должна быть логика запуска симуляции
            };
            modal.style.display = 'flex';
        }
    }
    const closeModalBtn = document.getElementById('closeModal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            document.getElementById('imageModal').style.display = 'none';
        });
    }
    const imageModal = document.getElementById('imageModal');
    if (imageModal) {
        imageModal.addEventListener('click', function(e) {
            if (e.target === imageModal) {
                imageModal.style.display = 'none';
            }
        });
    }
});
