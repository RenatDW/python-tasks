from collections import Counter
import os


def is_word_char(c):
    """Проверяет, является ли символ буквой или цифрой"""
    return c.isalpha() or c.isdigit()


def find_words_with_three_identical_letters(text):
    """Находит слова с 3+ одинаковыми буквами"""
    words = []
    current_word = []

    for char in text:
        if is_word_char(char):
            current_word.append(char)
        else:
            if current_word:
                words.append(''.join(current_word))
                current_word = []
    # Добавляем последнее слово, если текст не заканчивается разделителем
    if current_word:
        words.append(''.join(current_word))

    result = []
    for word in words:
        letter_counts = Counter(char.lower() for char in word if char.isalpha())
        if any(count >= 3 for count in letter_counts.values()):
            result.append(word)

    seen = set()
    unique_result = []
    for word in result:
        lower_word = word.lower()
        if lower_word not in seen:
            seen.add(lower_word)
            unique_result.append(word)

    return unique_result


def process_text_file(input_path, output_path):
    """Обрабатывает файл и записывает результат"""
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words = find_words_with_three_identical_letters(text)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write("Слова с 3+ одинаковыми буквами:\n")
            file.write("---------------------------\n")
            for i, word in enumerate(words, 1):
                file.write(f"{i}. {word}\n")

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
        print("Пример содержимого input.txt:")
        print("ааабввв коооордината тееест привет аааа 123ааа456\nШшшабв Гооород тест 111222333")
        return

    success = process_text_file(input_file, output_file)

    if success:
        print("\nСодержимое выходного файла:")
        with open(output_file, 'r', encoding='utf-8') as file:
            print(file.read())


if __name__ == "__main__":
    main()