from _vk import auth
import graph_algos
import cache


"""
[?] - input from user needed
[!] - error occured
[+] - everything goes according to plan
[*] - debugging messages
[.] - informing user
"""


print("""      
Social Reconnaissance Tool
"Show me who your friends are and I’ll tell you who you are"               
""")

# TODO: create tempfiles cleaner, config (do I need it?) and help message

session = auth()


def main():
    cache.init()
    target = int(input("[?] Enter target's ID or handle: "))
    g = graph_algos.create_ego_graph(target, session)


if __name__ == "__main__":
    main()
