from bs4 import BeautifulSoup
import requests, re
import boj.core.util as util
from boj.commands.problem.converter import MarkdownConverter


# Returns markdown
def query_problem(problem_id):
    res = requests.get(util.problem_url(problem_id), headers=util.headers())
    soup = BeautifulSoup(res.text, "html.parser")

    problem_body = soup.select("#problem-body > div")

    html = ""
    for div in problem_body:
        headline = div.select_one("div > div > div > section > div.headline")
        if headline:
            html += headline.prettify()

        sample_data = div.select_one("div > div > div > section > pre.sampledata")
        if sample_data:
            html += sample_data.prettify()

        problem_text = div.select_one("div > div > div > section > div.problem-text")
        if problem_text:
            html += problem_text.prettify()

    # source = soup.select_one("#source")
    # if source:
    #     html += source.prettify()

    problem_tags = soup.select_one("#problem_tags")
    if problem_tags:
        html += problem_tags.prettify()

    problem_judge_info = soup.select_one("#problem-judge-info")
    if problem_judge_info:
        html += problem_judge_info.prettify()

    # problem_memo = soup.select_one("#problem_memo")
    # if problem_memo:
    #     html += problem_memo.prettify()

    html = re.sub(r"<button.+\n.*\n.*button>\n", "", html)
    html = re.sub(r"<h2>", "<h1>", html)
    html = re.sub(r"</h2>", "</h1>", html)

    return html


def markdownify_problem(html, problem_id):
    markdown = MarkdownConverter(heading_style="ATX").convert(html)
    markdown += "\nLink: " + util.home_url() + "/problem/" + str(problem_id)

    return markdown
