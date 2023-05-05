import re


def lines_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            yield line


def clean_line(line: str) -> list[str]:
    pattern = r"""[^\w\s]"""
    words = re.sub(pattern, "", line.strip())
    words = re.sub(r"\s{2,}", " ", words).lower().split()
    return words


def count_words(file_path) -> list[tuple[str, int]]:
    gen = lines_generator(file_path)
    words_count = {}
    for line in gen:
        words = clean_line(line)
        if words is not []:
            for word in words:
                if words_count.get(word) is not None:
                    words_count[word] = words_count[word] + 1
                else:
                    words_count[word] = 1
    return sorted(words_count.items(), key=lambda x: x[1], reverse=True)


def get_items_from_ordered_list(words_list: list[tuple[str, int]], num: int) -> list[tuple[str, int]]:
    try:
        word_count = words_list[num - 1][1]
        lst = []
        for item in words_list:
            if item[1] >= word_count:
                lst.append(item)
            else:
                break
        return lst
    except IndexError as err:
        print("There are not that many different words in this book")


def get_n_gram(file_path, n: int) -> list[tuple[str, int]]:
    gen = lines_generator(file_path)
    n_gram = {}
    current_line = []
    try:
        while True:
            if len(current_line) < n:
                current_line += clean_line(next(gen))
            else:
                phrase = " ".join(current_line[:n])
                if n_gram.get(phrase) is not None:
                    n_gram[phrase] += 1
                else:
                    n_gram[phrase] = 1
                current_line.pop(0)
    except StopIteration:
        return sorted(n_gram.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    place_no = int(input("How many words do you wish to see?: "))
    count_words_list = count_words('potop.txt')
    words_lst = get_items_from_ordered_list(count_words_list, place_no)
    print(f"Top {place_no} word counts: {words_lst}")
    print("Printing bigram and trigram")
    bigram_no = int(input("How many words of the bigram do you wish to see?: "))
    print(f"Bigram: {get_items_from_ordered_list(get_n_gram('potop.txt', 2), bigram_no)}")
    trigram_no = int(input("How many words of the trigram do you wish to see?: "))
    print(f"Trigram: {get_items_from_ordered_list(get_n_gram('potop.txt', 3), trigram_no)}")
