# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['location', 'twitter_tools']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.13.1,<2.0.0']

setup_kwargs = {
    'name': 'twitter-toolkit',
    'version': '0.1.0',
    'description': 'This project contains different tools to help search and analyze in twitter.',
    'long_description': 'Twitter tools\n=============\n\nThis project contains different tools to help search and analyze in twitter.\n\nThe analysis of tweets is often followed by doing the same pipeline for different projects.\nThis toolkit is a compilation and wrapper of many tools to ease the pipeline of analysis in twitter.\nFirst of all it provides search utilities, either by searching by a twitter query or by identifier.\nThen it integrates some models to infer users age, gender, and if it is a person or an organisation. This inference should be used with caution since it is not perfect, but can yield an overview of the type of users analyzed.\nThere is also a location of users inference for Spanish locations based on their _location_ text or _description_ in their Twitter profile.\nFor the text analysis we provide a pipeline for Topic analysis using the LDA algorithm and some sentiment analysis too.\nFinally we provide a network creation of the tweets and users function for a network analysis.\n\nTwitter Search\n--------------\n\n### Credentials\n\nTo run this you need to provide your Twitter API credentials in the form of \nYAML file.  \n\nFor example:\n```yaml\nsearch_tweets_api:\n  endpoint: https://api.twitter.com/2/tweets/search/all\n  consumer_key: XXXXXXXXXXXX\n  consumer_secret: XXXXXXXXXXXXXXXX\n  bearer_token: XXXXXXXXXXXXXXXXX\n```\n\n### Searching tweets\n\nYou query tweets with `search_tweets_by_query`.  \nTo have a more detailed for the parameters take a look at the [Twitter API](https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all)\n\n\n```python\nfrom twitter_tools.search_tools import TweetSearchUtil\n\ntsu = TweetSearchUtil(\'path_to_yaml_creds\')\ntweets = tsu.search_tweets_by_query(\n    "python OR #python"\n    ,tweet_fields="author_id,conversation_id,created_at,id,in_reply_to_user_id,lang,public_metrics,text"\n    )\n```\n\n### Searching by id\n\nYou can also search retrieve tweets and users by their id.\n\n```python\nfrom twitter_tools.search_tools import TweetSearchUtil\n\ntsu = TweetSearchUtil(\'path_to_yaml_creds\')\ntweets = tsu.retreive_tweets_by_id(\n    [\'12341\',\'12342\']\n    ,tweet_fields="author_id,conversation_id,created_at,id,in_reply_to_user_id,lang,public_metrics,text"\n    )\n\nusers = tsu.retreive_users_by_id(\n    [\'4321\',\'4322\']\n    ,user_fields="created_at,description,id,name,profile_image_url,public_metrics,username"\n    )\n```\n\n\nTwitter Inference\n-----------------\n\nThis is a Wrapper of [M3Inference](https://github.com/euagendas/m3inference)\nbut with an ease to use and make a general pipeline with this set of tools.  \n\n```python\nfrom twitter_tools.user_inference import TwitterUserInference\n\nusers = [{...},...]\n\ntui = TwitterUserInference()\n\ninference = tui.infer_users(users, lang=\'en\')\n```\n\nUsers Location\n--------------\n\nThis tool is only available for Spain locations.  \nTo feature other countries, a json in the format as `places_spain.json` should\nbe added.  \n\nThis tools checks the location of an user based otheir text location and\ndescription when no geolocation is available.\nChecks for city/country/region words in the user profile to try to identify for\nits location.\n\n```python\nfrom location.location_detector import LocationDetector\n\nuser = {...}\n\ndetector = LocationDetector(\'path_to_places_json\')\n\nloc, method = detector.identify_location(user[\'location\'], user[\'description\'])\n\n```\n\nTopic analysis\n--------------\n\nThis tool will do every step of topic analysis using LDA.  \n\nThe typical pipeline can be represented by as follows.\n\n```python\nfrom twitter_tools.topic_analysis import TopicAnalysis\n\ntweets = [...]\nanalyzer = TopicAnalysis(language=\'es\')\n\ntweets_clean = analyser.clean_docs(tweets)\ntweets_lemmas = analyser.lemmatize(tweets_clean, \n                                filter_postags=[\'ADJ\', \'ADV\', \'NOUN\', \'VERB\'])\nldamodel, docs_dict = analyzer.topic_analysis(tweets_lemmas,\n                                            topics_nb=10, print_words=10)\n```\n\nSentiment Analysis\n------------------\n\nSentiment analysis of text using pretrained models.\n\n```python\nfrom twitter_tools.topic_analysis import TopicAnalysis\n\ntweets = [...]\nanalyzer = TopicAnalysis(language=\'es\')\n\nsentiments = [analyzer.sentiment_analysis(t) for t in tweets]\n```\n\nNetwork creation\n----------------\n\nThis tool creates graphs based on the tweets and users interactions.  \nIt can create the user and the tweet graph.\n\nThe tweets dict like object must contain at least the following fields:\n`id`, `retweeted_by`, `favorited_by`.  \nThe users dict like object must contain at least the following fields:\n`id`, `screen_name`.\n\n```python\nfrom twitter_tools.network_tools import create_tweets_network, create_users_network\n\nusers = [...]\ntweets = [...]\n\nT = create_tweets_network(tweets)\nU = create_users_network(users, tweets)\n\n```\n\nOnce the network create you can export it and open the file in Gephi to visualize it and analize it.\n\n```python\nimport networkx as nx\n\nnx.write_gml(T, "tweets_network.gml")\n```\n',
    'author': 'Diego Saby',
    'author_email': 'cuquiwi@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
