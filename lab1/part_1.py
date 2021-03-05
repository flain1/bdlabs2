from typing import List, Tuple
from urllib.request import urlopen
from lxml import etree
import xml.etree.cElementTree as ET

INITIAL_URL = "https://kpi.ua"


def parse_kpi_website() -> Tuple[int, dict]:
    """Scrape images and text from pages of the KPI website. Save to an XML file.
    Return the total number of text tags and a dict with the page url containing most text elements and their count.
    """
    xml_root = ET.Element("data")
    htmlparser = etree.HTMLParser()

    # Parse INITIAL_URL and get a list of the subsequent URLs to be parsed.
    urls_to_parse, initial_page_text_elements_count = parse_initial_page(xml_root, htmlparser)

    # Used to determine the page with most text
    page_with_max_text_elements = INITIAL_URL
    max_text_elements_on_page: int = initial_page_text_elements_count

    # Go through the list of URLs and append them to the XML root. Find the page with most text
    for url in urls_to_parse:
        url_to_parse = INITIAL_URL + url
        response = urlopen(url_to_parse)
        tree = etree.parse(response, htmlparser)
        text_elements_count: int = parse_url(xml_root, tree, url_to_parse)

        if text_elements_count > max_text_elements_on_page:
            max_text_elements_on_page = text_elements_count
            page_with_max_text_elements = url_to_parse

    # Write all the parsed pages to an XML file
    xml_tree = ET.ElementTree(xml_root)
    xml_tree.write("kpi_website.xml", encoding="UTF-8")

    text_tags_count = len(xml_tree.findall(".//fragment[@type='text']"))

    return text_tags_count, dict(page_with_max_text_elements=page_with_max_text_elements, max_text_elements_on_page=max_text_elements_on_page)


def parse_initial_page(xml_root, htmlparser) -> Tuple[List[str], int]:
    """ Scrape data from `INITIAL_URL` and determine which other urls should be parsed. """
    response = urlopen(INITIAL_URL)
    tree = etree.parse(response, htmlparser)
    urls = tree.xpath("//a/@href")
    urls_to_parse = urls[1:20]

    text_elements_count: int = parse_url(xml_root, tree, INITIAL_URL)

    return urls_to_parse, text_elements_count


def parse_url(xml_root, tree, url) -> int:
    """ Extract all the text and image elements from a webpage and appends them to an XML file.

        Return the number of text elements found on the page.
     """
    text_pieces: List[str] = [
        text_piece
        for text_piece in (tree.xpath("//body//text()"))
        if any(char.isalpha() for char in text_piece)
    ]
    image_urls: List[str] = [image.attrib["src"] for image in tree.xpath("//body//img")]

    # Create a new "page" entry for the output XML doc
    page = ET.SubElement(xml_root, "page", url=url)
    for text in text_pieces:
        ET.SubElement(page, "fragment", type="text").text = text
    for image_url in image_urls:
        ET.SubElement(page, "fragment", type="image").text = image_url

    return len(text_pieces)


if __name__ == "__main__":
    number_of_text_tags, page_with_most_text = parse_kpi_website()

    print(f"Total number of text tags accumulated: {number_of_text_tags}")
    print(f"Page with most text elements: {page_with_most_text['page_with_max_text_elements']}; Number of elements: {page_with_most_text['max_text_elements_on_page']} ")
