import networkx as nx
import _vk
import cache
import igraph  # cannot install this one on Win
import os


VERTICES_THRESHOLD = 600
EDGES_THRESHOLD = 3000


# Done
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


def get_communities(nx_g, user):
    # heuristics for choosing community detection algo
    def use_bc(nx_g_h):
        if len(nx_g_h.nodes) < VERTICES_THRESHOLD and len(nx_g_h.edges) < EDGES_THRESHOLD:
            # if there are not so many edges we may use betweenness centrality algo
            return True
        else:
            # else we should use much faster (but less accurate) multilevel algo
            return False

    # returns graph without unneeded nodes, done
    # Feature: do not just delete node with degree 1
    # but build their ego-graph as well in order to make connections to existing communities
    def clean_graph(nx_g_c, user_c):
        nx_g_c.remove_node(user_c)
        deleted = list(nx.isolates(nx_g_c))
        deleted.append(user_c)
        nx_g_c.remove_nodes_from(list(nx.isolates(nx_g_c)))
        cleaned = nx_g_c
        return cleaned, deleted

    # TODO: create getting partitions using bc
    def get_partitions_bc(c_nx_g):
        ig_g = nx_to_ig(c_nx_g)
        dendrogram = ig_g.community_edge_betweenness()
        clusters = dendrogram.as_clustering()
        membership = clusters.membership
        a = list()
        for name, membership in zip(ig_g.vs["name"], membership):
            a.append([name, membership])
        return a

    # TODO: create getting partitions using ml
    def get_partitions_ml(c_nx_g):
        ig_g = nx_to_ig(c_nx_g)
        return ig_g

    # TODO: create graph recovery function
    def recover_graph(partitioned, deleted):
        return 0

    clean_nx_g, deleted_nodes = clean_graph(nx_g, user)
    if use_bc(clean_nx_g):
        partitioned = get_partitions_bc(clean_nx_g)
    else:
        partitioned = get_partitions_ml(clean_nx_g)

    result_g = recover_graph(partitioned, deleted_nodes)

    return result_g


# function for detecting similarities in communities
# TODO: create it
def find_similar(list_of_ids):
    return list_of_ids


def get_partitions_bc(c_nx_g):
    ig_g = nx_to_ig(c_nx_g)
    dendrogram = ig_g.community_edge_betweenness()
    clusters = dendrogram.as_clustering()
    membership = clusters.membership
    a = list()
    for name, membership in zip(ig_g.vs["label"], membership):
        a.append([name, membership])
    return a


def clean_graph(nx_g_c, user_c):
    nx_g_c.remove_node(user_c)
    deleted = list(nx.isolates(nx_g_c))
    deleted.append(user_c)
    nx_g_c.remove_nodes_from(list(nx.isolates(nx_g_c)))
    return nx_g_c, deleted


g3 = nx.read_gml("cache/graphs/525008285.gml")
cleaned, deleted = clean_graph(g3, "525008285")
print(get_partitions_bc(cleaned))
