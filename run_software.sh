#!/bin/bash

if [ $1 = "-d" ] ; then
echo "Webscraping ..."
python3 webscraper.py

echo "API-ing ..."
python3 pull_api.py
fi

echo "Creating database schema"
if [ -f db.sqlite3 ] ; then
    rm db.sqlite3
fi

sqlite3 db.sqlite3 < db.sql

if [ $1 = "-g" ] ; then 
echo "Generating visualizations"

echo "Generating 2017 graphs"
python3 make_2017_graph.py

echo "Generating 1960-2017 graphs"
python3 make_1960_2017_graph.py
fi

echo "Pulling up UI"
python3 manage.py runserver