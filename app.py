from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import requests
import os

app = Flask(__name__)

def get_user_data(username):
    user_url = f"https://api.github.com/users/{username}"
    followers_url = f"https://api.github.com/users/{username}/followers"
    repos_url = f"https://api.github.com/users/{username}/repos"

    user_data = requests.get(user_url).json()
    followers_data = requests.get(followers_url).json()
    repos_data = requests.get(repos_url).json()

    return user_data, followers_data, repos_data

def create_user_graph(user_data, followers_data, repos_data):
    graph = nx.DiGraph()
    graph.add_node(user_data["login"])
    for follower in followers_data:
        graph.add_node(follower["login"])
        graph.add_edge(follower["login"], user_data["login"])
    for repo in repos_data:
        graph.add_node(repo["name"])
        graph.add_edge(user_data["login"], repo["name"])
    return graph

def manual_pagerank(graph, max_iterations=100, damping_factor=0.85, tol=1e-6):
    nodes = list(graph.nodes())
    num_nodes = len(nodes)
    ranks = {node: 1 / num_nodes for node in nodes}
    for _ in range(max_iterations):
        new_ranks = {}
        for node in nodes:
            incoming_links = [n for n in graph.predecessors(node)]
            rank_sum = sum(ranks[incoming] / len(list(graph.successors(incoming))) for incoming in incoming_links)
            new_ranks[node] = (1 - damping_factor) / num_nodes + damping_factor * rank_sum
        if all(abs(new_ranks[node] - ranks[node]) < tol for node in nodes):
            break
        ranks = new_ranks
    return ranks

def visualize_graph(graph, pagerank_scores, username):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    node_sizes = [10000 * pagerank_scores[node] for node in graph.nodes()]
    nx.draw(graph, pos, with_labels=True, node_size=node_sizes, node_color="lightblue", font_size=8, edge_color="pink", arrowsize=15)
    plt.title(f"GitHub Network Graph for {username}")
    graph_path = f"static/{username}_graph.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        username1 = request.form['username1']
        username2 = request.form['username2']

        user1_data, followers1_data, repos1_data = get_user_data(username1)
        user2_data, followers2_data, repos2_data = get_user_data(username2)

        graph1 = create_user_graph(user1_data, followers1_data, repos1_data)
        graph2 = create_user_graph(user2_data, followers2_data, repos2_data)

        pagerank_scores1 = manual_pagerank(graph1)
        pagerank_scores2 = manual_pagerank(graph2)

        score1 = pagerank_scores1.get(username1, 0)
        score2 = pagerank_scores2.get(username2, 0)

        winner = (
            username1 if score1 > score2 else
            username2 if score2 > score1 else
            "Tie"
        )

        graph1_img = visualize_graph(graph1, pagerank_scores1, username1)
        graph2_img = visualize_graph(graph2, pagerank_scores2, username2)

        result = {
            'username1': username1,
            'username2': username2,
            'score1': round(score1, 6),
            'score2': round(score2, 6),
            'winner': winner,
            'graph1_img': graph1_img,
            'graph2_img': graph2_img
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
