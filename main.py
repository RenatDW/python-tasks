# import sys
def count_arguments(*args, **kwargs):
    positional_count = len(args)
    keyword_count = len(kwargs)
    return (positional_count, keyword_count)
result1 = count_arguments(1, 2, 3, a=4, b=5)
print(result1)  # Вывод: (3, 2)

result2 = count_arguments(10, 20)
print(result2)  # Вывод: (2, 0)

result3 = count_arguments()
print(result3)  # Вывод: (0, 0)

result4 = count_arguments(x=1, y=2, z=3)
print(result4)  # Вывод: (0, 3)
# def main ():
#    a = parse_file()
#    change_row_position(a)
#    save_in_file(a)


# def change_row_position(a):
#     index_min = 0
#     index_max = 0
#     value_min = sys.maxsize
#     value_max = -sys.maxsize - 1
#     for i in range(len(a)):
#         val = get_row_sum(a, i)
#         if value_min > val:
#             index_min = i
#             value_min = val
#         if value_max < val:
#             index_max = i
#             value_max = val
#     temp = [0]*len(a)

#     for i in range(len(a)):
#         temp[i] = a[i][index_max]

#     for i in range(len(a)):
#         a[i][index_max] = a[i][index_min]

#     for i in range(len(a)):
#         a[i][index_min] = temp[i]


# def get_row_sum(a, i):
#     sum = 0
#     for j in range(len(a)):
#         sum += a[j][i]
#     return sum

# def parse_file():
#     with open('input.txt') as f:
#         s = f.readlines()
#         a = [[]] * len(s)
#         for i in range(len(s)):
#             line = s[i].split(" ")
#             k = [0] * len(line)
#             for j in range(len(line)):
#                 k[j] = int(line[j])
#             a[i] = k
#     return a
   
# def save_in_file(c):
#     ans = ""
#     for i in range(len(c)):
#         for j in range(len(c[0])):
#             if j == 0:
#                 ans += str(c[i][j])
#             else:
#                 ans += " " + str(c[i][j])
#         ans += "\n"
        

#     with open("output.txt", "w") as file:
#         file.write(ans)

    
# if __name__ == '__main__':
#     main()