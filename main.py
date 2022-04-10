import re
import requests
from bs4 import BeautifulSoup, SoupStrainer
from random import randint


strip_pattern = re.compile(r"[^\S]([ ]{2,})")


def fetch_webpage(url: str) -> BeautifulSoup:
    webpage = requests.get(url)
    webpage.raise_for_status()

    return BeautifulSoup(webpage.content, "html.parser", parse_only=SoupStrainer("div", class_="mw-parser-output"))


def get_text(soup_obj: BeautifulSoup) -> str:
    """
    :param soup_obj: Used for finding the elements
    :return: Formatted str, containing all the text
    """
    formatted_str = ""

    for element in soup_obj.find_all("p"):
        el_text = element.text.replace('\n', '')

        if el_text.strip() == "": continue

        el_text = re.sub(r"\[\d*\]", "", el_text)
        paragraph = strip_pattern.sub(" ", el_text)

        if randint(2, 4) == 3:
            paragraph += "\n"
            print()

        formatted_str += paragraph

    return formatted_str


def main():
    from colorama import Fore, init as colorama_init

    colorama_init(autoreset=True)

    wikipedia_url = "wikipedia.org"
    url_check_patten = re.compile(rf"https://(.+?)\.{wikipedia_url}/wiki/(.+?)")

    while True:
        url = input("Input Wikipedia Url: ")

        if not url_check_patten.match(url):
            if wikipedia_url not in url:
                print(Fore.RED + "Not a Wikipedia Url")

            elif f"{wikipedia_url}/wiki/" not in url:
                print(
                    Fore.RED +
                    f"Url must be of a wiki page\nEg: https://en.{wikipedia_url}/wiki/Python_(programming_language)"
                )

            elif not url.endswith("wiki/"):
                print(Fore.RED + 'Page not Provided after "wiki/"')

            else:
                print(Fore.RED + 'Invalid URL')

            # for newline
            print()

        else:
            # if url was valid
            try:
                soup = fetch_webpage(url)
            except requests.exceptions.RequestException as exc:
                print(str(exc))

            else:
                text = get_text(soup)
                if "may refer to" in text:
                    print(soup.get_text(strip=True))
                else:
                    print(text)


        fetch_again = input("Fetch another Url (y/n): ")

        if fetch_again != "y":
            print(Fore.YELLOW + "Exiting...")
            break


if __name__ == "__main__":
    main()

