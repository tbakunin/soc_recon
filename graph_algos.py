import networkx as nx
import _vk
import cache


def create_ego_graph(vk_id, session):
    if cache.contains_graph(vk_id):
        return cache.get_graph(vk_id)

    g = nx.Graph()
    g.add_node(vk_id)
    friends = _vk.get_friends(session=session, target=vk_id)
    g.add_nodes_from(friends)

    for friend in friends:
        temp_friends = _vk.get_friends(session=session, target=friend)
        if temp_friends != -1:
            for temp_friend in temp_friends:
                if temp_friend in friends or temp_friend == vk_id:
                    g.add_edge(friend, temp_friend)

    cache.add_graph(vk_id, g)
    return g
