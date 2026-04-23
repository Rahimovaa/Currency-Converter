import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

# --- НАСТРОЙКИ ---
API_KEY = 'ВАШ_API_КЛЮЧ'  # ЗАМЕНИТЕ ЭТУ СТРОКУ НА СВОЙ КЛЮЧ!
HISTORY_FILE = 'history.json'
# ------------------

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        try:
            return [json.loads(line) for line in f if line.strip()]
        except json.JSONDecodeError:
            return []

def save_history(entry):
    with open(HISTORY_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def get_currencies():
    if not API_KEY or API_KEY == 'ВАШ_API_КЛЮЧ':
        messagebox.showerror('Ошибка', 'API-ключ не указан. Вставьте свой ключ в переменную API_KEY.')
        return []
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    try:
        response = requests.get(url).json()
        if response.get('result') != 'success':
            messagebox.showerror('Ошибка API', response.get('error-type', 'Неизвестная ошибка.'))
            return []
        return list(response['conversion_rates'].keys())
    except Exception as e:
        messagebox.showerror('Ошибка сети', str(e))
        return []

def convert():
    source = from_currency.get()
    dest = to_currency.get()
    amount_str
