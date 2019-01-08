import time
import calendar
import os
import networkx as nx

EXPIRE_TIME = 60**3


def init():
    print("[.] Initializing cache")
    if "cache" not in os.listdir("."):
        os.mkdir("cache")
    os.chdir("cache")
    if "graphs" not in os.listdir("."):
        os.mkdir("graphs")
    os.chdir("..")


def contains(target):
    os.chdir("cache")
    a = target in os.listdir(".") and ((calendar.timegm(time.gmtime()) - os.path.getmtime(str(target))) < EXPIRE_TIME)
    os.chdir("..")
    return a


def get(target):
    os.chdir("cache")
    print("[*] Loading ", target, " from cache")
    with open(target, "r") as f:
        os.chdir("..")
        return list(map(int, f.readlines()))


def add(target, friends):
    os.chdir("cache")
    print("[*] User ", target, " is not in cache. Adding")
    with open(target, "w") as f:
        for vkid in friends:
            f.write("%s\n" % vkid)

    os.chdir("..")
    return 0


def contains_graph(target):
    filename = str(target) + ".gml"
    os.chdir("cache/graphs")
    a = filename in os.listdir(".") and ((calendar.timegm(time.gmtime()) - os.path.getmtime(filename)) < 60 ** 3)
    os.chdir("../..")
    return a


def get_graph(target):
    os.chdir("cache/graphs")
    print("[*] Loading ", target, "'s graph from cache")
    g = nx.read_gml(str(target) + ".gml")
    os.chdir("../..")
    return g


def add_graph(target, g):
    os.chdir("cache/graphs")
    print("[*] User's ", target, " graph is not in cache. Adding")
    nx.write_gml(g, str(target) + ".gml")
    os.chdir("../..")
    return 0
