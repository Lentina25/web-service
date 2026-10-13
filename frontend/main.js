const BACKEND_URL = 'http://localhost:8000/api';

// Кнопка 1: Запрос рекомендаций от Web-сервиса через бэк + сохранение в БД
document.getElementById('btnRecommend').addEventListener('click', async () => {
    const client_name = document.getElementById('clientName').value;
    const skin_type = document.getElementById('skinType').value;
    const preferred_notes = document.getElementById('notes').value;

    const output = document.getElementById('output');
    output.innerHTML = "Загрузка рекомендаций...";

    try {
        const response = await fetch(`${BACKEND_URL}/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_name, skin_type, preferred_notes })
        });
        const result = await response.json();
        
        if(result.status === "success") {
            let html = `<h3>✨ Рекомендованные товары для вас:</h3>`;
            result.data.forEach(item => {
                html += `<div class="card"><strong>${item.name}</strong> (${item.type})<br>Подходит для: ${item.skin_type} кожа | Ноты: ${item.notes}</div>`;
            });
            output.innerHTML = html;
        } else {
            output.innerHTML = JSON.stringify(result, null, 2);
        }
    } catch (error) {
        output.innerHTML = `Ошибка соединения с бэкендом: ${error.message}`;
    }
});

// Кнопка 2: Запрос истории предпочтений напрямую из Базы Данных через бэк
document.getElementById('btnHistory').addEventListener('click', async () => {
    const output = document.getElementById('output');
    output.innerHTML = "Загрузка истории из БД...";

    try {
        const response = await fetch(`${BACKEND_URL}/preferences`);
        const data = await response.json();
        
        if (data.length === 0) {
            output.innerHTML = "История пуста.";
            return;
        }

        let html = `<h3>📋 Предпочтения:</h3>`;
        data.forEach(row => {
            html += `<div class="card">👤 <b>${row.client_name}</b> | Тип кожи: ${row.skin_type} | Ноты: ${row.preferred_notes} <small style="color:gray;">(${row.date})</small></div>`;
        });
        output.innerHTML = html;
    } catch (error) {
        output.innerHTML = `Ошибка соединения с бэкендом: ${error.message}`;
    }
});
