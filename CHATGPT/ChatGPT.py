import tkinter as tk
from tkinter import scrolledtext
import messagebox
import openai
import pickle

# Установка  API-ключа OpenAI
openai.api_key = ' '

# Создание главного окна приложения
root = tk.Tk()
root.title("ChatGPT")
root.geometry("800x600")

# Создание текстового поля для отображения сообщений
output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

# Создание текстового поля для ввода сообщений
input_text = tk.Text(root, width=80, height=5)
input_text.pack(padx=10, pady=10)


# Функция для отправки сообщения и получения ответа от ChatGPT
def send_message():
    # Получение введенного сообщения
    message = input_text.get("1.0", tk.END).strip()
    input_text.delete("1.0", tk.END)

    # Отправка сообщения в OpenAI API и получение ответа
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        max_tokens=1000,
        temperature=0.7,
        n=1,
        stop=None,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Получение ответа от ChatGPT
    reply = response.choices[0].text.strip()

    # Отображение ответа в текстовом поле
    output_text.insert(tk.END, "User: " + message + "\n")
    output_text.insert(tk.END, "ChatGPT: " + reply + "\n")
    output_text.insert(tk.END, "-" * 50 + "\n")
    output_text.see(tk.END)


# Создание кнопки "Отправить"
send_button = tk.Button(root, text="Отправить", command=send_message)
send_button.pack()

try:
    with open("saved_data.pickle", "rb") as file:
        saved_data = pickle.load(file)
        output_text.insert("end", saved_data)
except FileNotFoundError:
    pass


def save_data():
    data = output_text.get("1.0", "end-1c")  # Получаем текст из текстового поля
    with open("saved_data.pickle", "wb") as file:
        pickle.dump(data, file)  # Сериализуем данные и сохраняем их в файл


root.protocol("WM_DELETE_WINDOW", save_data)



root.mainloop()
