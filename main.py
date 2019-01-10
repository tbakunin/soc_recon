import argparse
import os
import sys

import cache
import graph_algos
import stats
from _vk import auth

"""
[?] - input from user needed
[!] - error occured
[+] - everything goes according to plan
[*] - debugging messages
[i] - informing user
"""


def parse_args():
    parser = argparse.ArgumentParser(description='''"Show me who your friends are and Ill tell you who you are"''')
    parser.add_argument("--clean_cache", help="clean cache files", action="store_true")
    parser.add_argument("--clean_creds", help="clean saved credentials", action="store_true")
    # parser.add_argument("--logging", help="enables logging (0 - no logging, 3 - debug level)")
    args = parser.parse_args()

    if args.clean_cache:
        os.chdir("cache")
        for file in os.listdir("."):
            if file not in ("graphs"):
                os.remove(file)

        os.chdir("graphs")
        for file in os.listdir("."):
            os.remove(file)
        os.chdir("../..")

        print("[+] Done cleaning cache")

    if args.clean_creds:
        if os.path.exists("vk_config.v2.json"):
            os.remove("vk_config.v2.json")

        if os.path.exists("resources/creds.log"):
            os.remove("resources/creds.log")

        print("[+] Done cleaning creds")

    if args.clean_creds or args.clean_cache:
        sys.exit()

    return 0


def main():
    session = auth()
    cache.init()
    target = int(input("[?] Enter target's ID or handle: "))
    g = graph_algos.create_ego_graph(target, session)
    comm_list = graph_algos.get_communities(g, target, session=session)
    comm_dict = graph_algos.separate_communities(comm_list)
    sims = {"city": [], "country": [], "school": [], "university": []}
    for t in sims.keys():
        for comm in comm_dict.keys():
            sims[t].append(stats.find_similar(comm_dict[comm], session))
        sims[t] = stats.normalize_data(sims[t])

    print(sims)
    return 0


if __name__ == "__main__":
    parse_args()
    main()
