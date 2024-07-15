"""
This file contains the API and its three endpoints:

arxiv: scrape arxiv.org API and store results in PostgreSQL database
results: provide all query results in JSON format
queries: fetch queries from database based on start and end time

"""

from flask import Flask, request, jsonify
from app.database import init_db, SessionLocal, ArxivPaper, QueryLog
from app.scraper import fetch_arxiv_papers, parse_and_store_papers
from datetime import datetime

app = Flask(__name__)  # flask application for creating an API


# endpoint to check if the API is running
@app.route('/')
def home():
    return jsonify(message="Hello, World!")


# arxiv endpoint
@app.route('/api/arxiv', methods=['POST'])
def scrape_arxiv():
    query = request.json.get('query', 'machine learning')   # extract 'query' and 'max_results' from request
    max_results = request.json.get('max_results', 5)
    start_time = datetime.utcnow()                          # save the query start time

    try:                                                    # fetch and store paper data from arxiv.org
        xml_data = fetch_arxiv_papers(query, max_results)
        end_time = datetime.utcnow()                        # save the query end time
        parse_and_store_papers(xml_data, query, start_time, end_time)
        return jsonify(message="Data scraped and stored successfully"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500


# results endpoint
@app.route('/api/results', methods=['GET'])
def get_results():
    session = SessionLocal()
    papers = session.query(ArxivPaper).all()
    session.close()
    return jsonify([{               # return all paper data in JSON format
        'title': paper.title,
        'summary': paper.summary,
        'link': paper.link
    } for paper in papers])


# queries endpoint
@app.route('/api/queries', methods=['GET'])
def get_queries():
    session = SessionLocal()

    # get the start and end time specified in the request
    query_params = request.args
    query_start_time = query_params.get('query_start_time')
    query_end_time = query_params.get('query_end_time')

    # convert query parameters to datetime Objects
    if query_start_time:
        query_start_time = datetime.fromisoformat(query_start_time)
    if query_end_time:
        query_end_time = datetime.fromisoformat(query_end_time)

    # create database query for only selecting queries that are between end time and start time (within the specified
    # time window)
    query = session.query(QueryLog)
    if query_start_time:
        query = query.filter(QueryLog.query_start_time >= query_start_time)
    if query_end_time:
        query = query.filter(QueryLog.query_end_time <= query_end_time)

    # retrieve said queries from database
    queries = query.all()
    session.close()

    # return the time data for each query in JSON format
    return jsonify([{
        'query': q.query,
        'query_start_time': q.query_start_time.isoformat(),
        'query_end_time': q.query_end_time.isoformat()
    } for q in queries])


if __name__ == '__main__':
    init_db()
    app.run()
