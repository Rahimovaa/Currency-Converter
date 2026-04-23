# Currency-Converter

# Currency Converter

## Автор: Сиротин Константин

## Описание
Простое GUI-приложение для конвертации валют с использованием Tkinter и ExchangeRate-API. История операций сохраняется в JSON.

## Установка и запуск

1. Установите Python 3.8+
2. Клонируйте репозиторий:
   git clone https://github.com/ваш_логин/currency_converter.git
3. Перейдите в папку проекта.
4. Создайте виртуальное окружение и установите зависимости:
   python -m venv env
   source env/bin/activate  # Linux/macOS
   .\env\Scripts\activate   # Windows
   pip install -r requirements.txt
5. Получите API-ключ на exchangerate-api.com и вставьте его в переменную API_KEY в currency_converter.py.
6. Запустите приложение:
   python currency_converter.py

## Использование

- Выберите валюты «Из» и «В».
- Введите сумму (только положительное число).
- Нажмите «Конвертировать».
- Результат появится под кнопкой.
- История операций отображается в таблице и сохраняется в history.json.
