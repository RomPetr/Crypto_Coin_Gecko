import tkinter as tk
from tkinter import ttk
import requests


# Функция для получения списка криптовалют
def get_crypto_list():
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    response.raise_for_status()
    get_coins = response.json()
    return get_coins


# Создаем интерфейс
window = tk.Tk()
window.title("Курс криптовалют")
window.geometry("300x200")

# Получаем список криптовалют
coins = get_crypto_list()
print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com

# Запуск интерфейса
window.mainloop()