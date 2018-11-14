# done, tested

import vk_api


def auth():

    def tfa_handler():
        code = input("[!] 2FA detected! Please enter code you've just received: ")
        return code, 0

    while True:
        print("[?] Do you want to authorize using login/pass or token?")
        des = input("[?] P/ass/word for login/pass, T/oken for token auth: ")
        if des.startswith("P"):
            session = vk_api.VkApi(login=input("[?] Enter your login: "),
                                   password=input("[?] Enter you password: "),
                                   auth_handler=tfa_handler)
            session.auth()
            vk = session.get_api()
            if vk.users.get(user_ids='1')[0]['id'] == 1:
                return vk
            else:
                input("[-] Some error occurred, try again or Ctrl-C")

        elif des.startswith("T"):
            session = vk_api.VkApi(token=input("[?] Enter your token: "))
            session.auth()
            vk = session.get_api()
            if vk.users.get(user_ids='1')[0]['id'] == 1:
                return vk
            else:
                input("[-] Some error occurred, try again (Enter) or exit (Ctrl-C)")
