from collections import Counter


def find_words_with_three_identical_letters(text):
    words = devide_text_by_word(text)
    ans = []
    result_set = set()
    for word in words:
        letters = [char for char in word if char.isalpha()]
        if letters:
            counter = Counter(letters)
            if max(counter.values()) >= 3:
                if word not in result_set:
                    result_set.add(word)
                    ans.append(word)

    # Шаг 3: Преобразуем множество в список
    return ans


def devide_text_by_word(text):
    words = []
    current_word = ""
    for char in text:
        if char.isalnum():
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""
    if current_word:
        words.append(current_word)
    return words


with open('input.txt', 'r') as file:
    textAfterEdit = file.read()

inputText = textAfterEdit

textAfterEdit = find_words_with_three_identical_letters(inputText)
with open('output.txt', 'w') as file:
    for i in range(len(textAfterEdit)):
        if i == 0:
            file.write(textAfterEdit[i])
        else:
            file.write(" " + textAfterEdit[i])



