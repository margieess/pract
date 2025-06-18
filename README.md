## Встановлення та запуск
1. Клонувати репозиторій
2. Створити та активувати віртуальне середовище:

      python -m venv venv
      venv\Scripts\activate

3. Встановити залежності:
    pip install -r requirements.txt

4. Запустити сервер:
    uvicorn main:app --reload
   
## Вимоги
- Python 3.11   
- FastAPI  
- SQLAlchemy  
- Pydantic  
- Uvicorn  
## Документація API
Після запуску сервера доступна автоматична документація:

- Swagger UI: `http://localhost:8000/docs`  
- ReDoc: `http://localhost:8000/redoc`  

## Тестування
Для тестування API можна використати колекцію Postman, що знаходиться у папці postman
