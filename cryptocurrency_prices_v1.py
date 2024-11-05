from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


# Функция для получения списка криптовалют
def get_crypto_list():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        response.raise_for_status()
        get_coins = response.json()
        return get_coins
    except Exception as e:
        mb.showerror("Ошибка", f"Код ошибки: {e}")


# Создаем интерфейс
window = tk.Tk()
window.title("Курс криптовалют")
window.geometry("300x200")

# Получаем список криптовалют
coins = get_crypto_list()
print(len(coins)) # Сколько всего криптовалют публикуется на CionGecko.com

# Запуск интерфейса
window.mainloop()