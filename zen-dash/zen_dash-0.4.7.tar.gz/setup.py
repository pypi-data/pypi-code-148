# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zen_dash', 'zen_dash.cli', 'zen_dash.project_management', 'zen_dash.support']

package_data = \
{'': ['*'], 'zen_dash': ['static/*']}

install_requires = \
['Jinja2>=3.1.1,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'fastapi>=0.75.1,<0.76.0',
 'python-multipart>=0.0.5,<0.0.6',
 'sphinx-rtd-theme>=1.0.0,<2.0.0']

entry_points = \
{'console_scripts': ['create_project = zen_dash.cli.main:create_project']}

setup_kwargs = {
    'name': 'zen-dash',
    'version': '0.4.7',
    'description': 'Simple yet scable and production ready python dashboard that is better than shiny application for business.',
    'long_description': "# What is Zen Dash?\nZen Dash, a python package, simplifies the building analytics/BI dashboard process while providing enterprise-level scalability, stability, and performance. You can use FastAPI and Flask to host the application. \n\n# Why did I build Zen Dash?\n\nThere are many dashboarding solutions, like shiny (R, python), Streamlit, and others. I have used all of these solutions. I enjoy building solutions. However, all of these tools and libraries lack one vital point. They are not enterprise-ready solutions. They are fragile and not scalable solutions. So, whenever I built analytics/ BI Dashboards, Even after many bandages, dashboards were delicate and unstable. \n\nBefore explaining the problem and its reasons, I like to describe the issues we are trying to solve. \n\n* Some of our dashboards need to be used by more than 200 people simultaneously and require a sub-second response to be practical. They will use more than 8 hours straight for work. The dashboard should not crash during usage.\n\n* more than a hundred field team members are using our other dashboard, which is spread across multiple countries. Their internet speed is not ideal like office, so the analytics dashboard needs to be anti-fragile. They should be able to share their data with our customers on the ground without worrying about the dashboard crashing or refreshing data. \n\n* the Third group of the dashboard is far more complex and sensitive since we integrated it into one of our company production environments. This dashboard needs to better code isolation for testing, so they deployed it, so we can be sure it is not breaking the company production environment. \n\nSo, I invested time in the zen-dash, which addresses these problems. Before jumping into the zen-dash, I want to show you what we have done to make anti-fragile systems using other analytics solutions. I will also explain why it is failing. You might want to try a zen dash to elevate pains in these stages. \n\n\n* Building plumber or fastapi/flask to offload computation. \nGood thing: application becomes somewhat better at responding\nBad thing: now, code is in multiple locations, which makes it difficult to onboard and debug. If we use shiny with python, it is difficult for some team members to understand what they are doing.\n\n* Rather than dashboards, we started to provide more reports. However, this, in turn, created more work to report on building and maintenance.\n\n* Building simpler dashboards with limited functionality or exploration. We also get pushed back on this type of dashboard because people want to know more than what limited functionality dashboard what returns\n\n* Using Tableau to deliver data to field or high requirements teams. Tableau is not a perfect solution, either. It limits what analytics tools we can use.\n\n\nIf you see these signs in your analytics dashboarding solutions, you face a similar and painful situation.\n\n\n# Why are other tools creating such issues?\n\nLet me explain in technical detail. Here I am focusing on specifically Shiny and Streamlit because both face similar situations. After all, they are using the same architecture and software design. In a single word, it is due to incompatible architecture and software design. \n\nThey are facing two main issues.\n\n* Websocket\n* Lack of separation between UI and backend (specifically with shiny).\n\n\nWebsocket is one great tool where you can connect the front and back end once and send as much data as you want between them. \n\nThe chat system uses Websocket. Websocket simplifies your communication architecture when you use WebSocket over the rest API. It is an effective tool for communicating real-time data with lower overhead. Websocket keeps the connection open to the backend server so that new data transfers don't require creating a new link and overhead related to it. \n\nHowever, this constant connection makes a delicate system. It can break for any reason. So, when shiny apps WebSocket crashes, it grays out the screen, and you must start again from scratch. You will lose all filter selections you have made. I believe this is done to reduce overhead to the complexity of code on the shiny side. Because of it, it is not an enterprise-grade solution. Due to these design selections, we are facing problems 1 and 2.\n\nAnother issue with the WebSocket will create an artificial choke point at the backend level since R is a single thread with poor async support. In R, code usually runs sequentially. You have to use the API pool to redistribute the load on other machines. However, R is choking data push even when an API pool is used. So if we offload work on other services using the rest API pool, it has to wait until all processes are finished. Even if threading support is in python, we are not thinking about additional processing we need where threading is not a good option. The best option is to do multiprocessing. To do that, you need a different type of software design. I have seen situations regularly where shiny renders time well over 1 min when you have too many things to render on the page. These limitations are attributing problems 2 and 3\n\nIf WebSocket is used, you select only one machine/service to respond. So single service needs to process all requests and respond to them. Because of it, we had to create situation one to address this. These design is attributing problem 1\n\nThe second biggest issue with shiny is not separating UI from the backend. This design is excellent for rapid development, but if misused, it can slow down your application. It creates problems precisely when you want to render a large data example table. Shiny, rather than sending data for the table, the backend converts to HTML code and pushes HTML code as a string through WebSocket. This process becomes cumbersome very quickly because sending just data will be light, but sending HTML as a string adds quite a bit of load. In addition, you have to use eval or similar code to evaluate the code base, which adds security venerability and other overhead processes. It also slowdowns applications.\n\n\n# How much does zen dash make a difference?\nA dashboard that regularly took more than 60 seconds to load response data within ten or fewer seconds. \n\nOur dashboard has become more stable. If the internet connection is slow or fast, it doesn't impact the entire application.\n\nThe dashboard can run for days at a time without stability issues.\n\nHow do we achieve it? After understanding the limitation of the WebSocket, I decided to remove the WebSocket for communicating information. Instead, it will send data using a traditional HTTP request. \n\nUI is prebuilt in angular and complies, where you can provide what to render using angular flex and material design. \n\n# Docs\nhttps://zen-reportz.github.io/zen_dash/index.html\n",
    'author': 'Zen',
    'author_email': 'zenreportz@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://zen-reportz.github.io/zen_dash/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
