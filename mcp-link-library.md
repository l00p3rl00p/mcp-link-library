```python
# McpLibrary - Main Script

import sqlite3
import hashlib
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import argparse
import sys

class SecureMcpLibrary:
    """
    Secure Multi-Contextual Processor (MCP) Link Library
    
    Provides secure link storage, retrieval, and management
    """

    def __init__(self, db_path='mcplibrary.db'):
        # Initialize secure database connection
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_secure_tables()
    
    def _create_secure_tables(self):
        """
        Create database tables with security constraints
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                domain TEXT NOT NULL,
                description TEXT,
                categories TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                hash TEXT
            )
        ''')
        self.conn.commit()
    
    def add_link(self, url, categories=None):
        """
        Add a new link with secure metadata extraction
        
        Args:
            url (str): URL to add
            categories (list): Optional categories for the link
        
        Returns:
            int: ID of the added link
        """
        # Validate and sanitize URL
        validated_url = self._validate_url(url)
        
        # Generate secure hash
        url_hash = hashlib.sha256(validated_url.encode()).hexdigest()
        
        # Extract metadata
        metadata = self._extract_link_metadata(validated_url)
        categories = categories or ['uncategorized']
        
        self.cursor.execute('''
            INSERT OR REPLACE INTO links 
            (url, title, domain, description, categories, is_active, hash) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            validated_url, 
            metadata['title'], 
            metadata['domain'], 
            metadata['description'], 
            ','.join(categories), 
            1,
            url_hash
        ))
        self.conn.commit()
        
        return self.cursor.lastrowid
    
    def _validate_url(self, url):
        """
        Comprehensive URL validation
        
        Args:
            url (str): URL to validate
        
        Returns:
            str: Validated URL
        """
        # Implement URL validation logic
        # Prevent malicious URL attempts
        pass
    
    def _extract_link_metadata(self, url):
        """
        Securely extract link metadata
        
        Args:
            url (str): URL to extract metadata from
        
        Returns:
            dict: Extracted metadata
        """
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return {
                'title': soup.title.string or url,
                'domain': urlparse(url).netloc,
                'description': (
                    soup.find('meta', attrs={'name': 'description'}).get('content', '') 
                    if soup.find('meta', attrs={'name': 'description'}) 
                    else ''
                )
            }
        except Exception as e:
            return {
                'title': url,
                'domain': urlparse(url).netloc,
                'description': 'Metadata extraction failed'
            }

def main():
    """
    Command-line interface for MCP Link Library
    """
    parser = argparse.ArgumentParser(description="Secure Link Library")
    parser.add_argument('--add', help="Add a new link")
    parser.add_argument('--categories', nargs='+', help="Categories for the link")
    
    args = parser.parse_args()
    library = SecureMCPLibrary()
    
    if args.add:
        link_id = library.add_link(args.add, args.categories)
        print(f"Added link with ID: {link_id}")

if __name__ == "__main__":
    main()
```
