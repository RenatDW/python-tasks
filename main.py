def main ():
    a = []
    c = []
    
    parse_file(a, c)
    result = find_matching_elements(a, c)
    
    save_in_file(result)
    
    
def find_matching_elements(list1, list2):
    matching_elements = []
    
    min_length = min(len(list1), len(list2))
    
    for i in range(min_length):
        if list1[i] == list2[i]:
            matching_elements.append(list1[i])
    
    return matching_elements

def parse_file(a, b):
    try:
        with open('input.txt', 'r') as f:
            lines = f.readlines()

            # Проверяем, что файл содержит ровно две строки
            if len(lines) != 2:
                raise ValueError("Файл должен содержать ровно две строки.")

            # Обрабатываем первую строку
            first_line = lines[0].strip()
            if not first_line:
                raise ValueError("Первая строка пустая.")
            
            first_numbers = first_line.split(",")
            try:
                a.extend(int(el.strip()) for el in first_numbers)
            except ValueError as e:
                raise ValueError(f"Ошибка в первой строке: {e}")

            # Обрабатываем вторую строку
            second_line = lines[1].strip()
            if not second_line:
                raise ValueError("Вторая строка пустая.")
            
            second_numbers = second_line.split(",")
            try:
                b.extend(int(el.strip()) for el in second_numbers)
            except ValueError as e:
                raise ValueError(f"Ошибка во второй строке: {e}")

    except FileNotFoundError:
        print("Ошибка: Файл 'input2.txt' не найден.")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")

# def parse_file(a, b):
#    with open('input2.txt', 'r') as f:
#         lines = f.readlines()
#         if len(lines) == 2:
#             first_line = lines[0].strip() 
#             first_numbers = first_line.split(",")  
#             if len(first_numbers) == 0:
#                 print("Первый массив пустой")
#                 return

#             for el in first_numbers:
#                 a.append(int(el.strip()))
            
#             second_line = lines[1].strip()  
#             second_numbers = second_line.split(",")  
#             if len(second_numbers) == 0:
#                 print("Второй массив пустой")
#                 return
#             for el in second_numbers:
#                 b.append(int(el.strip()))
#         else:
#             print("Невернные входные данные")
        
def save_in_file(c):
    ans = ""
    for i in range(len(c)):
        if i == 0:
            ans += str(c[i])
        else:
            ans += ", " + str(c[i])

    with open("output.txt", "w") as file:
        file.write(ans)

    
if __name__ == '__main__':
    main()