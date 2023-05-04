def lines_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            yield line


def count_words(file_path):
    gen = lines_generator(file_path)
    words_count = {}
    for line in gen:
        words = line.strip().split()
        print(words)
        for word in words:
            if words is not []:
                if words_count.get(word) is not None:
                    words_count[word] = words_count[word] + 1
                else:
                    words_count[word] = 1


if __name__ == '__main__':
    print(count_words('potop.txt'))
