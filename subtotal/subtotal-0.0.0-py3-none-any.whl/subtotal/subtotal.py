import argparse
import time
from pathlib import Path
from urllib.parse import urlparse

from printbuddies import ProgBar
from seleniumuser import User

root = Path(__file__).parent


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("url", type=str, help=""" The url to find subdomains for. """)

    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default=None,
        help=""" Output file to dump subdomains to. 
        If unspecified, a folder named "subtotals" will
        be created in your current working directory and
        the results will be saved to {url}-subdomains.txt""",
    )

    parser.add_argument(
        "-b",
        "--browser",
        type=str,
        default="firefox",
        help=""" Browser for selenium to use.
        Can be "firefox" or "chrome".
        The appropriate webdriver needs to be installed
        in your current working directory or in your PATH.""",
    )

    args = parser.parse_args()

    return args


class User(User):
    def expand_subdomains(self):
        """Expand the listing of subdomains until all are visible.
        Mostly using Javascript to deal with these nightmare shadow roots."""

        script = """ 
        var moreButton = document.getElementsByName("domain-view")[0].shadowRoot.getElementById("report").children[3].children[0].shadowRoot.children[0].children[1].children[0].getElementsByClassName("load-more mt-3")[0]; 
        function getVisibleSubdomains() {
            return document.getElementsByName("domain-view")[0].shadowRoot.children[0].children[3].children[0].shadowRoot.children[0].children[1].children[0].children[0].shadowRoot.children[0].children[1].children.length;
        }
        moreButton.click();
        return getVisibleSubdomains();
        """
        total_subdomains = self.script(
            'return document.getElementsByName("domain-view")[0].shadowRoot.children[0].children[3].children[0].shadowRoot.children[0].children[1].shadowRoot.getElementById("info-badge").textContent;'
        )
        total_subdomains = total_subdomains.strip().strip(")").strip("(")
        if "K" in total_subdomains:
            total_subdomains = float(total_subdomains.split()[0]) * 1000
        total_subdomains = int(total_subdomains)
        bar = ProgBar(total_subdomains)
        while True:
            visible_subdomains = self.script(script)
            bar.display(
                prefix="Expanding subdomains", counter_override=visible_subdomains
            )
            if visible_subdomains >= total_subdomains:
                break
            else:
                time.sleep(1)

    def get_subdomains(self) -> list[str]:
        script = """ return document.getElementsByName("domain-view")[0].shadowRoot.children[0].children[3].children[0].shadowRoot.children[0].children[1].children[0].children[0].shadowRoot.children[0].children[1].children;"""
        subdomain_body = self.script(script)
        subdomains = sorted(
            list(
                set(
                    [
                        row.find_element("xpath", ".//div/a").text
                        for row in subdomain_body
                    ]
                )
            )
        )
        return subdomains


def main(args: argparse.Namespace = None):
    if not args:
        args = get_args()

    parsedurl = urlparse(args.url)
    if parsedurl.netloc:
        args.url = parsedurl.netloc.strip("www.")
    if not args.output_file:
        (Path.cwd() / "subtotals").mkdir(parents=True, exist_ok=True)
        args.output_file = Path.cwd() / "subtotals" / f"{args.url}-subdomains.txt"

    virustotal_url = f"https://www.virustotal.com/gui/domain/{args.url}/relations"
    with User(
        headless=True if args.browser == "firefox" else False, browser_type=args.browser
    ) as user:
        user.get(virustotal_url)
        time.sleep(1)
        try:
            user.expand_subdomains()
        except Exception as e:
            try:
                user.solve_audio_captcha_google(
                    ['//iframe[@title="reCAPTCHA"]'],
                    ['//iframe[@title="recaptcha challenge expires in two minutes"]'],
                )
            except:
                pass
            time.sleep(1)
            user.expand_subdomains()
        subdomains = user.get_subdomains()
    print(*subdomains, sep="\n")
    print(f"Found {len(subdomains)} unique subdomains.")
    args.output_file.write_text("\n".join(subdomains))


if __name__ == "__main__":
    main(get_args())
