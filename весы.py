import json

# Загрузка вашей JSON-модели (замените на путь к вашей модели)
model_path = "GPT-B.json"

with open(model_path, 'r', encoding='utf-8') as json_file:
    model_data = json.load(json_file)

# Оценка количества элементов (вопросов и ответов) в модели
num_entries = len(model_data)
print(f"Количество элементов (вопросов и ответов) в вашей модели: {num_entries}")
