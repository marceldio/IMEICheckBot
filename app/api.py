import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.config import config

router = APIRouter()


# Данные запроса
class IMEIRequest(BaseModel):
    imei: str
    token: str


# Данные ответа
class IMEIResponse(BaseModel):
    imei: str
    brand: str
    model: str
    status: str


async def check_imei_service(imei: str):
    """Отправка запроса в IMEICheck API"""

    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        "Authorization": f"Bearer {config.API_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "deviceId": imei,
        # "serviceId": 1  # для live-режима
        "serviceId": 12,  # для тестового режима 12(успех), 13, 14, 15
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Ошибка при запросе к IMEICheck API",
        )

    return response.json()  # Возвращаем ответ от API


@router.post("/api/check-imei")
async def check_imei(data: dict):
    # Проверка токена
    if data.get("token") != config.API_TOKEN:
        raise HTTPException(status_code=401, detail="Неверный API-токен")

    # Логика проверки IMEI
    imei = data.get("imei")
    # Здесь отправляется запрос к внешнему API или проверяется локально
    return {"message": f"IMEI {imei} обработан"}
