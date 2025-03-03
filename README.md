# IMEICheckBot
Бэкенд-система для проверки IMEI устройств, 
которая интегрирована с Telegram-ботом и предоставляет API для внешних запросов.

Функционал:

Доступ: 
- Реализован белый список для доступа к функционалу Telegram-бота:
    ID пользователей добавляются в .env, проверка работает.

Авторизация через API: 
- Реализована авторизация по токену для доступа к API:
    доступ к API /api/check-imei только по токену.

Telegram-бот:
- Пользователь отправляет боту IMEI: 
    бот принимает IMEI.    
- Бот проверяет IMEI на валидность: 
    если не 15 цифр, бот запрашивает корректный IMEI.
- Бот отправляет в ответ информацию о IMEI: 
    бот делает запрос к API и возвращает ответ пользователю.

Запросы API (пример)
Запрос на получение информации:
Метод: POST /api/check-imei
Параметры запроса:
imei (строка, обязательный) — IMEI устройства.
token (строка, обязательный) — токен авторизации.
    Реализован, принимает параметры:
    imei (обязательный)
    token (обязательный)

Ответ:
JSON с информацией о IMEI:
    реализовано, ответ от IMEICheck API корректно передается.

Сервис:
https://imeicheck.net/

url = "https://api.imeicheck.net/v1/checks"
тестовый IMEI: 356735111052198, 490154203237518
тестовый (успешный) serviceId: 12
Ограничение: 
Sandbox-режим возвращает случайные данные в ответе (это особенность сервиса, а не ошибка).



# Документация проекта IMEICheckBot

## 🔹 Описание проекта
IMEICheckBot — это бэкенд-система для проверки IMEI устройств, интегрированная с Telegram-ботом и 
предоставляющая API для внешних запросов. 
В рамках задания реализована работа с сервисом [IMEICheck](https://imeicheck.net/).

---

## 📌 1. API

### 🔹 `POST /api/check-imei`
Метод для проверки IMEI через API.

#### 🔹 **Параметры запроса:**
| Параметр | Тип | Обязательный | Описание |
|----------|------|--------------|-----------|
| `imei` | `string` | ✅ | 15-значный IMEI устройства |
| `token` | `string` | ✅ | API-токен для авторизации |

#### 🔹 **Пример запроса:**
```bash
curl -X POST "http://127.0.0.1:8000/api/check-imei" \
     -H "Content-Type: application/json" \
     -d '{"imei": "356735111052198", "token": "ВАШ_API_ТОКЕН"}'
```

#### 🔹 **Пример ответа:**
```json
{
    "message": "IMEI 356735111052198 обработан",
    "deviceName": "iPhone 12",
    "serial": "7XJ1NB30F5CZK",
    "warrantyStatus": "Out Of Warranty"
}
```

#### 🔹 **Ошибки:**
| Код | Описание |
|------|-----------|
| 401 | Неверный API-токен |
| 422 | Некорректный IMEI |

---

## 📌 2. Запуск сервера

### 🔹 **Требования**
- Установленный Python 3.12
- [Poetry](https://python-poetry.org/docs/)
- Файл `.env` с необходимыми настройками, по примеру.

### 🔹 **Запуск**
1. **Активировать виртуальное окружение:**
   ```bash
   poetry shell
   ```
2. **Запустить сервер:**
   ```bash
   poetry run python -m app.main
   ```
3. Сервер будет доступен по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📌 3. Запуск Telegram-бота

### 🔹 **Требования**
- Установленный Python 3.12
- Файл `.env` с `TELEGRAM_BOT_TOKEN`
- Telegram-бот создан в `@BotFather`

### 🔹 **Запуск**
1. **Активировать виртуальное окружение:**
   ```bash
   poetry shell
   ```
2. **Запустить бота:**
   ```bash
   poetry run python -m app.bot
   ```
3. Бот начнет работать и обрабатывать сообщения пользователей.

---

## 📌 4. Добавление пользователей в белый список

1. Запустите бота и отправьте ему любое сообщение.
2. Бот ответит с вашим `user_id`.
3. Добавьте `user_id` в `.env`:
   ```env
   WHITE_LIST=123456789
   ```
4. Перезапустите бота для применения изменений.

Только пользователи из белого списка могут пользоваться ботом.

---

📌 **Готово!** Теперь IMEICheckBot полностью функционирует.
