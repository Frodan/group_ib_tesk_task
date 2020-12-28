import vk_api
import requests
import json
from abc import ABCMeta, abstractmethod


"""
Знаю, что оставлять в коде ключи, а тем более выкладывать на гитхаб - плохая идея, но оставлю их, 
так как вам так проверять работоспособность будет проще, а я их деактивирую сразу после проверки.
"""

VK_SERVICE_KEY = "ff0af646ff0af646ff0af64632ff6c8662fff0aff0af646a4b233a7a591f75518c7a6ea"
VK_APP_ID = "6713380"

STEAM_KEY = "7AD3CEDF4B4C81FF23D9CC92081DB818"

PROXIES = {
    "http": "http://177.4.173.226:80"
}


class SocialNetworksConnector(metaclass=ABCMeta):
    @abstractmethod
    def get_profile(self, user):
        pass

    @abstractmethod
    def get_friends(self, user):
        pass

    @abstractmethod
    def get_wall(self, user):
        pass


class VkConnector(SocialNetworksConnector):
    def __init__(self, app_id, key, proxies=None):
        if proxies:
            proxy_session = requests.session()
            proxy_session.proxies.update(proxies)
            self.session = vk_api.VkApi(token=key, app_id=app_id, session=proxy_session)
        else:
            self.session = vk_api.VkApi(token=key, app_id=app_id)
        self.api = self.session.get_api()

    def _get_user_id(self, user):
        if str(user).isnumeric():
            return user
        else:
            user_data = self.api.utils.resolveScreenName(screen_name=user)
            if user_data:
                return user_data['object_id']
            else:
                print(f"No such user: {user}")
                return None

    def get_profile(self, user):
        user_id = self._get_user_id(user)
        if not user_id:
            return None
        fields = 'nickname, screen_name, bdate, mobile_phone, home_phone, connections, site, relation, relatives'
        return self.api.users.get(user_ids=user_id, fields=fields)

    def get_friends(self, user):
        user_id = self._get_user_id(user)
        if not user_id:
            return None
        user_info = self.api.friends.get(user_id=user_id, count=5000)
        count = user_info['count']
        user_friends = user_info['items']
        if count > 5000:
            new_user_info = self.api.friends.get(user_id=user_id, count=5000, offset=5000)
            user_friends += new_user_info['items']
        return user_friends

    """
    def get_followers(self, user):
        user_id = self._get_user_id(user)
        if not user_id:
            return None
        user_info = self.api.users.getFollowers(user_id=user_id, count = 1000)
        count = user_info['count']
        user_followers = user_info['items']
        if count > 1000:
            for i in range(1000, count, 1000):
                new_user_info = self.api.users.getFollowers(user_id=user_id, count=1000, offset=i)
                user_followers += new_user_info['items']
        return user_followers
    """

    def get_wall(self, user):
        user_id = self._get_user_id(user)
        user_info = self.api.wall.get(owner_id=user_id, count=100)
        count = user_info['count']
        user_posts = user_info['items']
        if count > 100:
            for i in range(100, count, 100):
                new_user_info = self.api.wall.get(owner_id=user_id, count=100, offset=i)
                user_posts += new_user_info['items']
        return user_posts


class SteamConnector(SocialNetworksConnector):
    def __init__(self, key, proxies=None):
        self.key = key
        self.session = requests.session()
        if proxies:
            self.session.proxies.update(proxies)

    def get_steam_id(self, user):
        if user.isnumeric():
            return user
        else:
            request_data = self.session.get(f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={self.key}&vanityurl={user}")
            user_data = json.loads(request_data.text)
            if user_data['response']['success'] == 1:
                return user_data['response']['steamid']
            else:
                print(f"No such user: {user}")
                return None

    def get_profile(self, user):
        steam_id = self.get_steam_id(user)
        if not steam_id:
            return None
        request_data = self.session.get(
            f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={self.key}&steamids={steam_id}")
        user_data = json.loads(request_data.text)
        return user_data['response']['players'][0]

    def get_friends(self, user):
        steam_id = self.get_steam_id(user)
        if not steam_id:
            return None
        request_data = self.session.get(
            f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={self.key}&steamid={steam_id}")
        user_data = json.loads(request_data.text)
        return user_data['friendslist']['friends']

    def get_wall(self, user):
        # No such API
        return None


if __name__ == "__main__":
    vk_test = VkConnector(VK_APP_ID, VK_SERVICE_KEY, proxies=PROXIES)
    steam_test = SteamConnector(STEAM_KEY, proxies=PROXIES)
    print(steam_test.get_profile("frodan"))
    print(steam_test.get_friends("frodan"))
    print(vk_test.get_profile("144785889"))
    print(vk_test.get_friends("frodan"))
    print(vk_test.get_wall("frodan"))
    # print(vk_test.get_followers("frodan"))
