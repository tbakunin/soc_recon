import vk_api
import os
import cache

def get_all_info(session=None, target=None):
    # do not need to check whether data is given since all checks are done before
    os.chdir("resources")
    scope = open("full_info", "r").read()
    os.chdir("..")
    return session.users.get(user_id=target, fields=scope)


def get_friends(session=None, target=None):
    starget = str(target)
    if cache.contains(starget):
        return cache.get(starget)
    else:
        try:
            friends = session.friends.get(user_id=target)["items"]
        except vk_api.exceptions.ApiError:
            print("[!] ID " + str(target) + " is private. Skipping")
            return -1
        cache.add(starget, friends)
        return friends


def get_groups(session=None, target=None):
    pass

