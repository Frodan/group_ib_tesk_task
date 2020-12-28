"""
Для задания я использовал полиномиальное хэширование.
Получилось не очень удачно, так как с количеством слов > 1 просто используются делители
полиномиального хэша от всей строки.
Так же, такой обход файла в 4 мб явно не лучшая идея.
К сожалению, времени осталось мало, так что ничего лучше я уже не придумаю.

Mod выбран как простое число, удачно совпавшее с размером файла со словами.
p - простое число, большее, чем любой символ в алфавите.
max(a_i) < p < mod, gcd(p, mod) = 1
"""


class Hasher():
    def __init__(self, words=1, delimiter=''):
        self.words = words
        self.delimiter = delimiter
        self.mod = 370103
        self.p = 307

    def hash(self, obj):
        str_obj = str(obj)

        parts = []

        num_hash = self._hash_func(str_obj)
        number_delimiters = self._get_delimiters(num_hash)
        i = 0
        while i < self.words:
            for number_delimiter in number_delimiters:
                with open('words_alpha.txt') as words_file:
                    for j in range(0, number_delimiter + 1):
                        line = words_file.readline()
                    parts.append(line.strip().capitalize())
                    i += 1
                    if i == self.words:
                        break

        return self.delimiter.join(parts)

    @staticmethod
    def _get_delimiters(number):
        i = 1
        a = []
        while i ** 2 <= number:
            if number % i == 0:
                a.append(i)
                if i != number // i:
                    a.append(number // i)
            i += 1
        a.sort(reverse=True)
        return a

    # polynomial hash
    def _hash_func(self, part):
        h = 0
        power = 0
        for char in part:
            number = ord(char) * self.p ** power
            h += number
            power += 1
        return h % self.mod


if __name__ == "__main__":
    h = Hasher(words=3, delimiter='-')
    print(h.hash("hello word"))
    print(h.hash({1: "2", 3: "5"}))
