import vk_api
import os


def auth(check_saved=1):
    def tfa_handler():
        code = input("[!] 2FA detected! Please enter code you've just received: ")
        return code, 0

    def inner_auth(login=None, password=None, tfa=tfa_handler):
        session = vk_api.VkApi(login=login,
                               password=password,
                               auth_handler=tfa)

        session.auth()
        vk = session.get_api()
        if vk.users.get(user_ids='1')[0]['id'] == 1:
            return vk
        else:
            print("[-] Some error occurred, try again or Ctrl-C")
            return -1

    if "creds" in os.listdir("resources") and check_saved:
        with open("resources/creds.log", "r") as f:
            lines = f.readlines()
            if len(lines) == 2:
                res = inner_auth(login=lines[0], password=lines[1])
            else:
                print("[!] Auth using saved creds failed, login manually!")
                return auth(0)

            if res == -1:
                print("[!] Auth using saved creds failed, login manually!")
                auth(0)
            else:
                return res
    else:
        login = input("[?] Enter your login: ")
        password = input("[?] Enter you password: ")
        if input("Do you want to save your creds? They WONT be encrypted [Y/es, N/o] ").upper().startswith("Y"):
            with open("resources/creds.log", "w") as f:
                f.write("\n".join((login, password)))
        print("[+] Auth succeeded!")
        return inner_auth(login=login, password=password)
