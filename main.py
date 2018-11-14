import vk_api
from auth import auth
from vk_extractor import extractor

session = auth()

target = input("[?] Enter your target's ID: ")
while True:
    print("""
          [i] Your options:
          [1] Get general info
          [2] Find hidden friends
          [3] Dig info
          [4] Test whether account is fake
          [5] View and export found info
          [6] Exit
          """)
    des = input("[?] Choose 1-6: ")
    if not (len(des) == 1) or (49 > ord(des) or 54 < ord(des)):
        print("[!] Choose one of the options 1-6!")
    else:
        pass

    if des == '1':
        print(extractor(session, target))
        if input("[?] Run another module? [Y/n]").upper().startswith("Y"):
            continue
        else:
            break
    else:
        print("[-] Not yet implemented")
        continue

