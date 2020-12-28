import unittest
from Hasher import Hasher


class TestHasher(unittest.TestCase):
    def setUp(self):
        self.hasher = Hasher(words=3, delimiter=":")

    def test_hash(self):
        h = self.hasher.hash("hello word")
        print(h)
        assert h == "Imper:Beaverize:Agreer"


if __name__ == "__main__":
    unittest.main()
