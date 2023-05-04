import re


def lines_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            yield line


def count_words(file_path):
    gen = lines_generator(file_path)
    words_count = {}
    for line in gen:
        pattern = r"""^\W|\W$"""
        words = line.strip().split()
        clean_words = list(map(lambda x: re.sub(pattern, "", x).lower(), words))
        for word in clean_words:
            if words is not []:
                if words_count.get(word) is not None:
                    words_count[word] = words_count[word] + 1
                else:
                    words_count[word] = 1
    return dict(sorted(words_count.items(), key=lambda x: x[1], reverse=True))


if __name__ == '__main__':
    print(count_words('potop_sample.txt'))
