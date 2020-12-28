import unittest
from Connectors import VkConnector, SteamConnector

VK_SERVICE_KEY = "ff0af646ff0af646ff0af64632ff6c8662fff0aff0af646a4b233a7a591f75518c7a6ea"
VK_APP_ID = "6713380"

STEAM_KEY = "7AD3CEDF4B4C81FF23D9CC92081DB818"


class TestVkConnector(unittest.TestCase):
    def setUp(self):
        self.vkConnector = VkConnector(key=VK_SERVICE_KEY, app_id=VK_APP_ID)

    def test_api(self):
        user_info = self.vkConnector.get_profile(1)
        assert user_info[0]['id'] == 1


class TestSteamConnector(unittest.TestCase):
    def setUp(self):
        self.SteamConnector = SteamConnector(key=STEAM_KEY)

    def test_api(self):
        user_info = self.SteamConnector.get_profile("frodan")
        assert user_info['steamid'] == '76561198082315764'


if __name__ == "__main__":
    unittest.main()
