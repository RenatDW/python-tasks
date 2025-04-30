import re
from collections import Counter
import os


def find_words_with_three_identical_letters(text):
    """Находит слова с 3+ одинаковыми буквами"""
    words = re.findall(r'[A-Za-zА-Яа-я0-9]+', text)
    result = []
    for word in words:
        letter_counts = Counter(char.lower() for char in word if char.isalpha())
        if any(count >= 3 for count in letter_counts.values()):
            result.append(word)

    seen = set()
    unique_result = []
    for word in result:
        if word.lower() not in seen:
            seen.add(word.lower())
            unique_result.append(word)

    return unique_result


def process_text_file(input_path, output_path):
    """Обрабатывает файл и записывает результат"""
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words = find_words_with_three_identical_letters(text)

        with open(output_path, 'w', encoding='utf-8') as file:
            for word in words:
                file.write(word + "\n")

        print(f"Результат успешно записан в файл: {output_path}")
        return True

    except FileNotFoundError:
        print(f"Ошибка: файл {input_path} не найден")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def main():
    # Указываем пути к файлам прямо в коде
    input_file = "input.txt"  # Файл с исходным текстом
    output_file = "output.txt"  # Файл для записи результатов

    if not os.path.exists(input_file):
        print(f"Файл {input_file} не существует")
        print("Создайте файл input.txt в той же папке или укажите правильный путь")
        return

    success = process_text_file(input_file, output_file)

    if success:
        print("\nСодержимое выходного файла:")
        with open(output_file, 'r', encoding='utf-8') as file:
            print(file.read())


if __name__ == "__main__":
    main()