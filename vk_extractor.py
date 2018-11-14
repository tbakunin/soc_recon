import vk_api
import os


def extractor(session=None, target=None):
    os.chdir("resources")
    scope = open("full_info", "r").read()
    os.chdir("..")
    return session.users.get(user_id=target, fields=scope)
