import time
import calendar
import os
import networkx as nx

EXPIRE_TIME = 60**3

def init():
    if "cache" not in os.listdir("."):
        os.mkdir("cache")

def contains(target):
    os.chdir("cache")
    a = target in os.listdir(".") and ((calendar.timegm(time.gmtime()) - os.path.getmtime(str(target))) < EXPIRE_TIME)
    print("Expire time is " + str(EXPIRE_TIME))
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
    filename = str(target) + ".gexf"
    os.chdir("cache/graphs")
    a = filename in os.listdir(".") and ((calendar.timegm(time.gmtime()) - os.path.getmtime(filename)) < 60 ** 3)
    os.chdir("../..")
    return a


def get_graph(target):
    os.chdir("cache/graphs")
    print("[*] Loading ", target, "'s graph from cache")
    g = nx.read_gexf(str(target) + ".gexf")
    os.chdir("../..")
    return g


def add_graph(target, g):
    os.chdir("cache/graphs")
    print("[*] User's ", target, " graph is not in cache. Adding")
    nx.write_gexf(g, str(target) + ".gexf")
    os.chdir("../..")
    return 0
