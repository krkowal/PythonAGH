import re
from typing import List


def lines_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            yield line


def count_words(file_path) -> list[str]:
    gen = lines_generator(file_path)
    words_count = {}
    for line in gen:
        pattern = r"""[^\w\s]"""
        words = re.sub(pattern, "", line.strip())
        words = re.sub(r"\s{2,}", " ", words).lower().split()
        for word in words:
            if words is not []:
                if words_count.get(word) is not None:
                    words_count[word] = words_count[word] + 1
                else:
                    words_count[word] = 1
    return sorted(words_count.items(), key=lambda x: x[1], reverse=True)


def get_items_from_ordered_list(words_dict: list[tuple[str, int]], num: int):
    try:
        word_count = words_dict[num - 1][1]
        lst = []
        for item in words_dict:
            if item[1] >= word_count:
                lst.append(item)
            else:
                break
        return lst
    except IndexError as err:
        print("There are not that many different words in this book")


# def get_n_gram(n:int):


if __name__ == '__main__':
    place_no = int(input("How many words do you wish to see?: "))
    count_words_list = count_words('potop.txt')
    lst = get_items_from_ordered_list(count_words_list, place_no)
    print(lst)
