import networkx as nx
import _vk
import cache
import igraph
import os


def create_ego_graph(vk_id, session):
    if cache.contains_graph(vk_id):
        return cache.get_graph(vk_id)

    nx_g = nx.Graph()
    nx_g.add_node(vk_id)
    friends = _vk.get_friends(session=session, target=vk_id)
    nx_g.add_nodes_from(friends)

    for friend in friends:
        temp_friends = _vk.get_friends(session=session, target=friend)
        if temp_friends != -1:
            for temp_friend in temp_friends:
                if temp_friend in friends or temp_friend == vk_id:
                    nx_g.add_edge(friend, temp_friend)
        else:
            nx_g.add_edge(vk_id, friend)

    cache.add_graph(vk_id, nx_g)
    return nx_g


# TODO: adequate converter from networkx graph to igraph, current version is nasty

def nx_to_ig(g):
    nx.write_gml(g, "temp.gml")
    g1 = igraph.read("temp.gml", format="gml")
    os.remove("temp.gml")
    return g1


# heuristics for choosing community detection algo
def choose_cda():
    pass
