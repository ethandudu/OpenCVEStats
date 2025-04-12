import sys
import mariadb
import logging
from dotenv import dotenv_values
import requests
from datetime import datetime
from dateutil import parser
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This class will be used to represent a feed in the database
# It will contain the attributes of a feed
# id, title, link, description, docs, generator, language
class feed:
    def __init__(self, id, title, link, description, docs, generator, language):
        self.id = id
        self.title = title
        self.link = link
        self.description = description
        self.docs = docs
        self.generator = generator
        self.language = language
        
    def __str__(self):
        return f"Feed({self.id}, {self.title}, {self.link}, {self.description}, {self.docs}, {self.generator}, {self.language})"
    
    @staticmethod
    def getAll():
        db = database()
        cur = db.get_cursor()
        cur.execute("SELECT * FROM feed")
        fetched_feeds = cur.fetchall()
        feeds = []
        for row in fetched_feeds:
            feeds.append(feed(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return feeds
    
    @staticmethod
    def getWhere(where_string):
        db = database()
        cur = db.get_cursor()
        cur.execute(f"SELECT * FROM feed WHERE TRUE AND {where_string}")
        fetched_feeds = cur.fetchall()
        feeds = []
        for row in fetched_feeds:
            feeds.append(feed(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        return feeds
    
    def save(self):
        db = database()
        cur = db.get_cursor()
        cur.execute("REPLACE INTO feed (title, link, description, docs, generator, language) VALUES (?, ?, ?, ?, ?, ?)", (self.title, self.link, self.description, self.docs, self.generator, self.language))
        db.commit()
    

# This class will be used to represent a CVE in the database
# It will contain the attributes of a CVE
# id, title, link, description, guid, timestamp, type, feed
class cve:
    def __init__(self, id, title, link, description, guid, timestamp, type, feed):
        self.id = id
        self.title = title
        self.link = link
        self.description = description
        self.guid = guid
        self.timestamp = timestamp
        self.type = type
        self.feed = feed
        
    def __str__(self):
        return f"CVE({self.id}, {self.title}, {self.link}, {self.description}, {self.guid}, {self.timestamp}, {self.type}, {self.feed})"
    
    @staticmethod
    def getAll():
        db = database()
        cur = db.get_cursor()
        cur.execute("SELECT * FROM cve")
        fetched_cves = cur.fetchall()
        cves = []
        for row in fetched_cves:
            cves.append(cve(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return cves
    
    @staticmethod
    def getWhere(where_string):
        db = database()
        cur = db.get_cursor()
        cur.execute(f"SELECT * FROM cve WHERE TRUE AND {where_string}")
        fetched_cves = cur.fetchall()
        cves = []
        for row in fetched_cves:
            cves.append(cve(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return cves
    
    def save(self):
        db = database()
        cur = db.get_cursor()
        cur.execute("REPLACE INTO cve (title, link, description, guid, timestamp, feed) VALUES (?, ?, ?, ?, ?, ?)", (self.title, self.link, self.description, self.guid, self.timestamp, self.feed))
        db.commit()
    
    
# Singleton class for database connection
class database:
    __instance = None
    def __new__(cls, *_, **__):
        if cls.__instance is None:
            cls.__instance = super(database, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        if hasattr(self, "initialized"):
            return  # already initialized
        config = dotenv_values()
        self.host = config.get("DB_HOST", "localhost")
        self.port = int(config.get("DB_PORT", 3306))
        self.user = config.get("DB_USER", "root")
        self.password = config.get("DB_PASSWORD", "")
        self.database = config.get("DB_NAME", "")

        try:
            self.connection = mariadb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            logger.info("Successfully connected to the database.")
        except mariadb.Error as e:
            logger.error(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        self.initialized = True

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
        logger.info("Database connection closed.")

if __name__ == "__main__":
    db = database()    
    
    feeds = feed.getAll()
    
    # Fetch each feed with its link
    for f in feeds:
        logger.info(f"Fetching feed {f.title} from {f.link}")
        response = requests.get(f.link)
        if response.status_code == 200:
            logger.info(f"Feed {f.title} fetched successfully")
        else:
            logger.error(f"Failed to fetch feed {f.title}")
            continue
        
        # Check if the response is XML
        if "application/xml" not in response.headers.get('Content-Type', ''):
            logger.warning(f"Feed {f.title} is not XML")
            logger.info(f"Response headers: {response.headers}")
            logger.info(f"Response content: {response.text}")
        
        try:
            # Decode HTML entities and parse XML response
            XML_test = html.unescape(response.text)  # Decode HTML entities
            root = ET.fromstring(XML_test)
            cves = []
            for item in root.findall(".//item"):
                title = item.find("title").text
                title = html.unescape(title) if title else title  # Decode HTML entities
                link = item.find("link").text
                link = html.unescape(link) if link else link
                description = item.find("description").text
                description = html.unescape(description) if description else description
                guid = item.find("guid").text
                timestamp_str = item.find("pubDate").text
                timestamp_str = html.unescape(timestamp_str) if timestamp_str else timestamp_str
                dt = parser.parse(timestamp_str)
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
                cves.append(cve(None, title, link, description, guid, timestamp, None, f.id))
        except Exception as e:
            logger.error(f"Failed to decode or parse XML for feed '{f.title}' at URL {f.link}. Error details: {e}")
            cves = []
            
        logger.info(f"Parsed {len(cves)} CVEs from feed {f.title}")
        
        # Save each CVE to the database
        for c in cves:
            c.save()

    db.close()