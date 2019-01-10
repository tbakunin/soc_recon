import os

import igraph  # cannot install this one on Win
import networkx as nx

import _vk
import cache

VERTICES_THRESHOLD = 600
EDGES_THRESHOLD = 3000
SIMILARITY_THRESHOLD = 0.3


# TODO: develop var and func naming conventions, refactor
# TODO: logging

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


# TODO: adequate conversion from networkx graph to igraph, current version is nasty
def nx_to_ig(g):
    nx.write_pajek(g, "temp.pajek")
    g1 = igraph.read("temp.pajek", format="pajek")
    os.remove("temp.pajek")
    return g1


def separate_communities(id_comm_list):
    comms = list(set([x[1] for x in id_comm_list]))
    comm_dict = {}
    for comm_label in comms:
        comm_dict.update({comm_label: []})
    for id_i in id_comm_list:
        comm_dict[id_i[1]].append(id_i[0])

    return comm_dict


def get_communities(nx_g, user, algo="auto", session=None):
    def use_bc(nx_g_h):
        if len(nx_g_h.nodes) < VERTICES_THRESHOLD and len(nx_g_h.edges) < EDGES_THRESHOLD:
            return True
        else:
            return False

    def clean_graph(nx_g_c, user_c):
        try:
            nx_g_c.remove_node(user_c)
        except nx.exception.NetworkXError:
            nx_g_c.remove_node(int(user_c))
        deleted = list(nx.isolates(nx_g_c))
        nx_g_c.remove_nodes_from(list(nx.isolates(nx_g_c)))
        cleaned = nx_g_c
        return cleaned, deleted

    def get_partitions_bc(c_nx_g):
        ig_g = nx_to_ig(c_nx_g)
        dendrogram = ig_g.community_edge_betweenness()
        clusters = dendrogram.as_clustering()
        membership = clusters.membership
        a = list()
        for name, membership in zip(ig_g.vs["id"], membership):
            a.append([name, membership])
        return a

    def get_partitions_ml(c_nx_g):
        ig_g = nx_to_ig(c_nx_g)
        clusters = ig_g.community_multilevel()
        membership = clusters.membership
        a = list()
        for name, membership in zip(ig_g.vs["id"], membership):
            a.append([name, membership])
        return a

    # testing func
    def write_labeled_graph(nx_graph, comm_list, i_session):
        id_comm_dict = dict()
        for pair in comm_list:
            dict_up = {pair[0]: pair[1]}
            id_comm_dict.update(dict_up)

        id_name_dict = _vk.get_names(i_session, list(nx_graph))
        nx.set_node_attributes(nx_graph, id_comm_dict, "community")
        nx.set_node_attributes(nx_graph, id_name_dict, "name")
        nx.write_gexf(nx_graph, "labeled.gexf")
        return 0

    clean_nx_g, deleted_nodes = clean_graph(nx_g, str(user))
    if algo == "auto":
        algo_des = use_bc(clean_nx_g)
    else:
        algo_des = True if algo == "bc" else False if algo == "ml" else -1
        if algo_des == -1:
            raise Exception("[-] No such algo!")

    id_comm_list = get_partitions_bc(clean_nx_g) if algo_des else get_partitions_ml(clean_nx_g)
    # write_labeled_graph(clean_nx_g, id_comm_list, session)
    return id_comm_list

