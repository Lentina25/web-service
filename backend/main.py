import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Разрешаем CORS, чтобы Frontend мог делать запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
WEB_SERVICE_URL = os.getenv("WEB_SERVICE_URL")

class PreferenceSchema(BaseModel):
    client_name: str
    skin_type: str
    preferred_notes: str

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# Кнопка 1: Получение истории запросов из БД
@app.get("/api/preferences")
def get_preferences():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, client_name, skin_type, preferred_notes, created_at FROM client_preferences ORDER BY id DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        result = []
        for r in rows:
            result.append({
                "id": r[0], "client_name": r[1], "skin_type": r[2], "preferred_notes": r[3], "date": str(r[4])
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Кнопка 2: Отправка данных на внешний сервис + сохранение лога в БД
@app.post("/api/recommend")
def get_recommendation_and_save(data: PreferenceSchema):
    try:
        # 1. Сохраняем в нашу локальную БД
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO client_preferences (client_name, skin_type, preferred_notes) VALUES (%s, %s, %s);",
            (data.client_name, data.skin_type, data.preferred_notes)
        )
        conn.commit()
        cur.close()
        conn.close()

        # 2. Делаем запрос к специализированному Web-сервису подбора
        response = requests.post(
            f"{WEB_SERVICE_URL}/predict",
            json={"skin_type": data.skin_type, "notes": data.preferred_notes}
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
