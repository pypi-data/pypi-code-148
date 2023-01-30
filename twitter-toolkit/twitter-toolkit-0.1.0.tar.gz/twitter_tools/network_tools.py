import math
import pandas as pd
from itertools import combinations
import progressbar
import networkx as nx
from community import community_louvain
from collections import defaultdict


# ------------ utils -------------

def jaccard_index(a, b):
    """https://en.wikipedia.org/wiki/Jaccard_index"""
    if not a or not b:
        return 0
    return len(set(a).intersection(b))/len(set(a).union(b))

def combinations_lenght(n, k):
    """https://math.stackexchange.com/questions/3458791/count-of-all-possible-combinations-of-length-k-for-a-given-string-of-n-lette"""
    return math.factorial(n)/(2*math.factorial(n - k))

# ------------ build network -------------  

def create_tweets_network(json, and_links_dataframe=False):
    """
    Creates a graph from a JSON representing tweets.
    """
    df = pd.DataFrame(json)
    df['retweeted_by'] = df['retweeted_by'].apply(lambda x: [e[0] for e in x]) # keep just the screenname, discard the user id
    df['favorited_by'] = df['favorited_by'].apply(lambda x: [e[0] for e in x])
    df['tweetid'] = df.id
    df = df.set_index('tweetid')


    # select network nodes: filter for tweets with at least one user favorited or retweeted
    df['interactions'] = df.apply(lambda x: x['retweeted_by'] + x['favorited_by'], axis=1)
    interactions = df['interactions'].to_dict()
    interactions = {k: v for k, v in interactions.items() if len(v) > 0}

    print(f"{len(interactions)} nodes (tweets with at least one user interaction)")


    # compute network links: check all the combinations
    comb_iter = combinations(interactions, 2)
    comb_length = combinations_lenght(len(interactions), 2)

    print(f'Computing links for all the combinations of {len(interactions)} tweets:')

    links = []

    for id1, id2 in progressbar.progressbar(comb_iter, max_value=comb_length):
        users1 = set(interactions[id1])
        users2 = set(interactions[id2])
        j = jaccard_index(users1, users2)
        # print(id1, id2, users1, users2, j)
        if j > 0:
            links.append((id1, id2, j))


    print(f"{len(links)} links")


    # create networkx graph
    graph_df = pd.DataFrame(links, columns=['id1', 'id2', 'weight'])
    G = nx.from_pandas_edgelist(graph_df, 'id1', 'id2', ["weight"])


    # set all tweets attributes as node attributes
    columns = df.columns
    for key in columns:
        nx.set_node_attributes(G, df[key].apply(lambda x: str(x)).to_dict(), key)


    # compute louvain communities
    print("Computing communities with louvain algorithm")
    partition = community_louvain.best_partition(G, random_state=42)
    nx.set_node_attributes(G, partition, 'partition_louvain')


    # compute centrality: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.degree_centrality.html#networkx.algorithms.centrality.degree_centrality
    print("Computing degree centrality")
    centrality = nx.degree_centrality(G)
    nx.set_node_attributes(G, centrality, 'degree_centrality')


    # compute betweeness centrality: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html#networkx.algorithms.centrality.betweenness_centrality
    print("Computing betweeness centrality")
    betweeness = nx.betweenness_centrality(G, k=100, weight='weight')
    nx.set_node_attributes(G, betweeness, 'betweeness_centrality')

    if and_links_dataframe:
        return G, graph_df
    else:
        return G

def create_users_network(json_users, json_tweets, and_links_dataframe=False):
    """
    Creates a graph from a JSON representing tweets.
    """

    users_df = pd.DataFrame(json_users)
    users_df = users_df.set_index('screen_name')

    tweets_df = pd.DataFrame(json_tweets)
    tweets_df['retweeted_by'] = tweets_df['retweeted_by'].apply(lambda x: [e[0] for e in x]) # keep just the screenname, discard the user id
    tweets_df['favorited_by'] = tweets_df['favorited_by'].apply(lambda x: [e[0] for e in x])
    tweets_df['tweetid'] = tweets_df.id
    tweets_df = tweets_df.set_index('tweetid')

    
    # select network nodes: filter for tweets with at least one user favorited or retweeted
    tweets_df['interactions'] = tweets_df.apply(lambda x: x['retweeted_by'] + x['favorited_by'], axis=1)
    interactions = tweets_df['interactions'].to_dict()
    interactions = {k: v for k, v in interactions.items() if len(v) > 0}


    # invert the relationship
    users_liked_tweets = defaultdict(list)

    for tweet_id, users_ids in interactions.items():
        for user in users_ids:
            users_liked_tweets[user].append(tweet_id)

    print(f"{len(users_liked_tweets)} nodes (users with at least one interaction)")


    # compute network links: check all the combinations
    comb_iter = combinations(users_liked_tweets, 2)
    comb_length = combinations_lenght(len(users_liked_tweets), 2)

    print(f'Computing links for all the combinations of {len(users_liked_tweets)} nodes:')

    links = []

    for id1, id2 in progressbar.progressbar(comb_iter, max_value=comb_length):
        tweets1 = set(users_liked_tweets[id1])
        tweets2 = set(users_liked_tweets[id2])
        j = jaccard_index(tweets1, tweets2)
        if j > 0:
            links.append((id1, id2, j))


    print(f"{len(links)} links")


    # create networkx graph
    graph_df = pd.DataFrame(links, columns=['id1', 'id2', 'weight'])
    G = nx.from_pandas_edgelist(graph_df, 'id1', 'id2', ["weight"])


    # set node attributes
    columns = users_df.columns
    for key in columns:
        nx.set_node_attributes(G, users_df[key].apply(lambda x: str(x)).to_dict(), key)
    
    screen_names = {}
    for i in users_df.index:
        screen_names[i] = i

    nx.set_node_attributes(G, screen_names, 'screen_name')


    # compute louvain communities: https://python-louvain.readthedocs.io/en/latest/index.html
    print("Computing communities with louvain algorithm")
    partition = community_louvain.best_partition(G, random_state=42)
    nx.set_node_attributes(G, partition, 'partition_louvain')


    # compute centrality: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.degree_centrality.html#networkx.algorithms.centrality.degree_centrality
    print("Computing degree centrality")
    centrality = nx.degree_centrality(G)
    nx.set_node_attributes(G, centrality, 'degree_centrality')


    # compute betweeness centrality: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html#networkx.algorithms.centrality.betweenness_centrality
    print("Computing betweeness centrality")
    betweeness = nx.betweenness_centrality(G, k=100, weight='weight')
    nx.set_node_attributes(G, betweeness, 'betweeness_centrality')

    if and_links_dataframe:
        return G, graph_df
    else:
        return G
