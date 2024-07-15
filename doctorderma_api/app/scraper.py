"""
This file contains the code for scraping the arxiv.org API and storing the results in the local PostgreSQL database.
"""

import requests
from app.database import ArxivPaper, SessionLocal, QueryLog


# function for fetching paper data from the arxiv.org API
def fetch_arxiv_papers(query="machine learning", max_results=5):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"
    response = requests.get(url)  # query to arxiv.com
    response.raise_for_status()
    return response.content


# function for parsing the arxiv.org API response and storing the results in the local PostgreSQL database
def parse_and_store_papers(xml_data, query, start_time, end_time):
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_data)
    ns = {'ns': 'http://www.w3.org/2005/Atom'}              # namespace for XML tags
    session = SessionLocal()                                # new database session

    for entry in root.findall('ns:entry', ns):              # access the data by parsing xml_data
        title = entry.find('ns:title', ns).text
        summary = entry.find('ns:summary', ns).text
        link = entry.find('ns:link', ns).attrib['href']
        paper = ArxivPaper(title=title, summary=summary, link=link)
        session.add(paper)

    # log the data into the database
    query_log = QueryLog(query=query, query_start_time=start_time, query_end_time=end_time)
    session.add(query_log)

    session.commit()
    session.close()
