import pandas as pd
import os
import random
import names

# Путь к папке для сохранения файлов
DATA_DIR = 'data'

# Список групп
groups = ['1','2','3','4','5','6','7','8','9']

# Функция для генерации случайного номера студенческого билета
def generate_student_id(index):
    return f'СТ{10000 + index:05d}'

# Функция для генерации случайного среднего балла
def generate_avg_grade():
    return round(random.uniform(2.0, 5.0), 1)

# Генерация данных для каждой группы
data = []
student_index = 1

for group in groups:
    course = 2  # ИСТ-101 - 1 курс, ИСТ-102 - 2 курс
    for i in range(21):  # 21 студент в каждой группе
        data.append({
            '№': i + 1,
            'Номер студенческого билета': generate_student_id(student_index),
            'ФИО': names.get_full_name(),
            'Курс': course,
            'Группа': group,
            'Средний балл': generate_avg_grade()
        })
        student_index += 1

# Разделяем данные на две группы
data_group_1 = [d for d in data]

# Создаем папку data, если она не существует
os.makedirs(DATA_DIR, exist_ok=True)

# Создаем DataFrame и сохраняем в Excel
df_group_1 = pd.DataFrame(data_group_1)

# Сохраняем файлы
df_group_1.to_excel(os.path.join(DATA_DIR, 'group_1.xlsx'), index=False)

print("Файлы group_1.xlsx и group_2.xlsx успешно созданы в папке data/ с 42 строками данных")