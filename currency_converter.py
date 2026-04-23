import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

API_KEY = 'ВАШ_API_КЛЮЧ'
HISTORY_FILE = 'history.json'

# Загрузка истории из файла
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        try:
            return [json.loads(line) for line in f]
        except:
            return []

# Сохранение истории в файл
def save_history(entry):
    with open(HISTORY_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')

# Получение списка валют
def get_currencies():
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
    response = requests.get(url).json()
    return list(response['conversion_rates'].keys())

# Конвертация валют
def convert():
    source = from_currency.get()
    dest = to_currency.get()
    amount_str = amount_entry.get()
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror('Ошибка', 'Сумма должна быть положительным числом!')
        return

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{source}/{dest}/{amount}'
    try:
        response = requests.get(url).json()
        result = response['conversion_result']
        time = response['time_last_update_utc']
        result_label.config(text=f'{amount} {source} = {result} {dest}')
        time_label.config(text=f'Последнее обновление: {time}')
        # Сохраняем в историю
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
        messagebox.showerror('Ошибка', 'Не удалось выполнить конвертацию.')

# Обновление таблицы истории
def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)
    for entry in load_history():
        history_table.insert('', 'end', values=(entry['from'], entry['to'], entry['amount'], entry['result'], entry['time']))

# Создание окна
window = tk.Tk()
window.title('Currency Converter')
window.geometry('600x500')
window.resizable(False, False)

# Виджеты
tk.Label(window, text='Из:', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=10)
tk.Label(window, text='В:', font=('Arial', 12)).grid(row=0, column=2, padx=10, pady=10)
tk.Label(window, text='Сумма:', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=10)

currencies = get_currencies()
from_currency = ttk.Combobox(window, values=currencies, width=10, font=('Arial', 12))
to_currency = ttk.Combobox(window, values=currencies, width=10, font=('Arial', 12))
amount_entry = tk.Entry(window, font=('Arial', 12), width=15)

from_currency.grid(row=0, column=1, padx=10, pady=10)
to_currency.grid(row=0, column=3, padx=10, pady=10)
amount_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

convert_btn = tk.Button(window, text='Конвертировать', font=('Arial', 12), command=convert)
convert_btn.grid(row=2, column=1, columnspan=2, pady=10)

result_label = tk.Label(window, text='', font=('Arial', 12))
result_label.grid(row=3, column=0, columnspan=4, pady=5)
time_label = tk.Label(window, text='', font=('Arial', 10))
time_label.grid(row=4, column=0, columnspan=4, pady=5)

# Таблица истории
history_table = ttk.Treeview(window, columns=('Из', 'В', 'Сумма', 'Результат', 'Время'), show='headings')
for col in ('Из', 'В', 'Сумма', 'Результат', 'Время'):
    history_table.heading(col, text=col)
