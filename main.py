def main():
    list1, list2 = parse_file('input5.txt')
    if not list1 or not list2:
        print("Один из списков пуст или файл содержит некорректные данные.")
        return

    matching_elements = find_matching_elements(list1, list2)

    save_in_file(matching_elements)

    print("Совпадающие элементы:", matching_elements)


def parse_file(filename):
    list1 = []
    list2 = []
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

            if len(lines) != 2:
                raise ValueError("Файл должен содержать ровно две строки.")

            first_line = lines[0].strip()
            if not first_line:
                raise ValueError("Первая строка пустая.")

            first_numbers = first_line.split(",")
            try:
                list1 = [int(el.strip()) for el in first_numbers]
            except ValueError as e:
                raise ValueError(f"Ошибка в первой строке: {e}")

            second_line = lines[1].strip()
            if not second_line:
                raise ValueError("Вторая строка пустая.")

            second_numbers = second_line.split(",")
            try:
                list2 = [int(el.strip()) for el in second_numbers]
            except ValueError as e:
                raise ValueError(f"Ошибка во второй строке: {e}")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

    return list1, list2


def find_matching_elements(list1, list2):
    matching_elements = []
    min_length = min(len(list1), len(list2))

    for i in range(min_length):
        if list1[i] == list2[i]:
            matching_elements.append(list1[i])

    return matching_elements


def save_in_file(elements):
    if not elements:
        print("Нет совпадающих элементов для сохранения.")
        return

    with open("output.txt", "w") as file:
        file.write(", ".join(map(str, elements)))


if __name__ == '__main__':
    main()