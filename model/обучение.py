import json
import emoji  # Добавляем импорт emoji для работы со смайлами

def load_model_from_json(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as f:
            model = json.load(f)
        return model
    except FileNotFoundError:
        print("Файл не найден или не удалось прочитать его.")
        return {}

def save_model_to_json(model, file_path):
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(model, f, ensure_ascii=False, indent=4)

def display_model_data(model_data):
    print("Содержимое JSON-файла:")
    for query, response in model_data.items():
        print(f"{query} = {response}")

file_path = 'GPT-B.json'
model_data = load_model_from_json(file_path)

while True:
    user_query = input("Введите запрос (или 'q' для выхода): ")
    if user_query.lower() == 'q':
        break

    user_response = input("Введите ответ: ")
    
    model_data[user_query] = user_response

    save_model_to_json(model_data, file_path)
    print(f"Запрос '{user_query}' и ответ '{user_response}' добавлены в JSON-файл.")
    
    # Отображение содержимого JSON-файла после изменений
    display_model_data(model_data)
