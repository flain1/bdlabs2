from controller.Neo4jController import Neo4jController
from controller.Controller import Controller, Tags
from servers.neo4j_server.Neo4jServer import Neo4jServer

menu_list = {
    'Choose': {
        'Find users that received or forwarded message with these tags': Neo4jController.get_users_with_tagged_messages,
        'Find user pairs that are N messages distance away': Neo4jController.get_users_with_n_long_relations,
        'Find the shortest way on graph through messages': Neo4jController.shortest_way_between_users,
        'Find authors that are marked "spam"': Neo4jController.get_users_which_have_only_spam_conversation,
        'Find unrelated users that have tagged messages': Neo4jController.get_unrelated_users_with_tagged_messages,
        'Назад': Controller.stop_loop,
    }
}

roles = {
    'utilizer': 'Utilizer menu',
    'admin': 'Admin menu'
}

neo4j = Neo4jServer()
special_parameters = {
    'role': '(admin or utilizer)',
    'tags': '('+', '.join(x.name for x in list(Tags))+')',
    'username1': '(' + ', '.join(x for x in neo4j.get_users()) + ')',
    'username2': '(' + ', '.join(x for x in neo4j.get_users()) + ')'
}
