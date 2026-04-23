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
    amount_str = amount_entry.get()

    # Проверка выбора валют
    if not source or not dest:
        messagebox.showerror('Ошибка', 'Пожалуйста, выберите обе валюты.')
        return

    # Проверка суммы
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Ошибка', 'Сумма должна быть положительным числом.')
        return

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{source}/{dest}/{amount}'
    try:
        response = requests.get(url).json()
        result = response['conversion_result']
        time = response['time_last_update_utc']
        
        result_label.config(text=f'{amount} {source} = {result} {dest}')
        time_label.config(text=f'Последнее обновление: {time}')
        
        entry = {
            'from': source,
            'to': dest,
            'amount': amount,
            'result': result,
            'time': time
        }
        save_history(entry)
        update_history_table()
    except Exception as e:
        messagebox.showerror('Ошибка конвертации', 'Не удалось выполнить запрос к API.')

def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)
    for entry in load_history():
        history_table.insert('', 'end', values=(
            entry['from'],
            entry['to'],
            f"{entry['amount']:.2f}",
            f"{entry['result']:.2f}",
            entry['time']
        ))

# --- СОЗДАНИЕ ОКНА ---
window = tk.Tk()
window.title('Currency Converter')
window.geometry('700x550')
window.resizable(False, False)
window.configure(bg='#f0f0f0')

# ВИДЖЕТЫ (grid)
tk.Label(window, text='Из:', font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=0, padx=10, pady=10, sticky='e')
tk.Label(window, text='В:', font=('Arial', 12), bg='#f0f0f0').grid(row=0, column=2, padx=10, pady=10, sticky='e')
tk.Label(window, text='Сумма:', font=('Arial', 12), bg='#f0f0f0').grid(row=1, column=0, padx=10, pady=10, sticky='e')

currencies = get_currencies()
if not currencies:
    window.quit() # Закрываем окно, если не удалось получить список валют

from_currency = ttk.Combobox(window, values=currencies, width=10, font=('Arial', 12))
to_currency = ttk.Combobox(window, values=currencies, width=10, font=('Arial', 12))
amount_entry = tk.Entry(window, font=('Arial', 12), width=15)

from_currency.grid(row=0, column=1, padx=5)
to_currency.grid(row=0, column=3, padx=5)
amount_entry.grid(row=1, column=1, columnspan=2, padx=5)

convert_btn = tk.Button(window, text='Конвертировать', font=('Arial', 12), command=convert)
convert_btn.grid(row=2, column=1, columnspan=2, pady=15)

result_label = tk.Label(window, text='', font=('Arial', 14), bg='#f0f0f0')
result_label.grid(row=3, column=0, columnspan=4, pady=5)
time_label = tk.Label(window, text='', font=('Arial', 9), bg='#f0f0f0')
time_label.grid(row=4, column=0, columnspan=4, pady=2)

# ТАБЛИЦА ИСТОРИИ (grid)
history_table = ttk.Treeview(window, columns=('Из', 'В', 'Сумма', 'Результат', 'Время'), show='headings')
for i, col in enumerate(('Из', 'В', 'Сумма', 'Результат', 'Время')):
    history_table.heading(col, text=col)
    history_table.column(col, width=110 if i < 2 else 90)
history_table.grid(row=5, column=0, columnspan=4, padx=10, pady=(5, 20))
update_history_table()

# --- ГЛАВНЫЙ ЦИКЛ ---
window.mainloop()
