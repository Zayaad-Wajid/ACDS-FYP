"""
Text Preprocessing Module for Phishing Detection
=================================================
Provides text cleaning and preprocessing functions that match
the preprocessing used during model training.
"""

import re
import string
from typing import Optional
import logging

# Try to import NLTK components
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    
    # Download required NLTK data (if not already present)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)
    
    NLTK_AVAILABLE = True
    STOP_WORDS = set(stopwords.words('english'))
    LEMMATIZER = WordNetLemmatizer()
except ImportError:
    NLTK_AVAILABLE = False
    STOP_WORDS = set()
    LEMMATIZER = None
    logging.warning("NLTK not available. Using basic preprocessing.")

# Common phishing indicators
PHISHING_KEYWORDS = [
    'urgent', 'verify', 'account', 'suspended', 'password', 'click here',
    'immediately', 'expire', 'confirm', 'update your', 'security alert',
    'unusual activity', 'unauthorized', 'limited time', 'act now',
    'winner', 'prize', 'congratulations', 'selected', 'lucky',
    'bank', 'paypal', 'apple', 'microsoft', 'amazon', 'netflix',
    'invoice', 'payment', 'refund', 'transfer', 'wire',
]


def preprocess_text(text: str) -> str:
    """
    Comprehensive text cleaning for email content.
    This function MUST match the preprocessing used during model training.
    
    Args:
        text: Raw email text content
        
    Returns:
        Cleaned and preprocessed text ready for model prediction
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs (replace with token for context)
    text = re.sub(r'http\S+|www\S+|https\S+', ' urltoken ', text)
    
    # Remove email addresses (replace with token)
    text = re.sub(r'\S+@\S+', ' emailtoken ', text)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize and lemmatize (if NLTK available)
    if NLTK_AVAILABLE and LEMMATIZER:
        words = text.split()
        words = [
            LEMMATIZER.lemmatize(w) 
            for w in words 
            if w not in STOP_WORDS and len(w) > 2
        ]
        text = ' '.join(words)
    
    return text


def preprocess_file(file_path: str) -> str:
    """
    Read and preprocess text content from a file.
    
    Args:
        file_path: Path to the file to process
        
    Returns:
        Preprocessed text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return preprocess_text(content)
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return ""


def extract_email_features(email_content: str) -> dict:
    """
    Extract additional features from email content for enhanced detection.
    
    Args:
        email_content: Raw email content
        
    Returns:
        Dictionary of extracted features
    """
    features = {
        'url_count': 0,
        'email_count': 0,
        'has_html': False,
        'urgency_score': 0,
        'suspicious_keywords': [],
        'has_attachments': False,
        'link_text_mismatch': False,
    }
    
    if not email_content:
        return features
    
    content_lower = email_content.lower()
    
    # Count URLs
    urls = re.findall(r'http\S+|www\S+|https\S+', email_content)
    features['url_count'] = len(urls)
    
    # Count email addresses
    emails = re.findall(r'\S+@\S+', email_content)
    features['email_count'] = len(emails)
    
    # Check for HTML content
    features['has_html'] = bool(re.search(r'<[^>]+>', email_content))
    
    # Calculate urgency score based on keywords
    urgency_words = ['urgent', 'immediately', 'asap', 'now', 'expire', 'limited', 'act now']
    features['urgency_score'] = sum(1 for word in urgency_words if word in content_lower)
    
    # Find suspicious keywords
    features['suspicious_keywords'] = [
        kw for kw in PHISHING_KEYWORDS 
        if kw in content_lower
    ]
    
    # Check for attachment indicators
    attachment_patterns = ['.exe', '.zip', '.pdf', 'attachment', 'attached', 'enclosed']
    features['has_attachments'] = any(p in content_lower for p in attachment_patterns)
    
    return features


def extract_urls(text: str) -> list:
    """
    Extract all URLs from text.
    
    Args:
        text: Text content to search
        
    Returns:
        List of extracted URLs
    """
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def extract_email_addresses(text: str) -> list:
    """
    Extract all email addresses from text.
    
    Args:
        text: Text content to search
        
    Returns:
        List of extracted email addresses
    """
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)


def calculate_suspicion_score(features: dict) -> float:
    """
    Calculate an overall suspicion score based on extracted features.
    
    Args:
        features: Dictionary of extracted email features
        
    Returns:
        Suspicion score between 0 and 1
    """
    score = 0.0
    
    # URL count contribution (many URLs = more suspicious)
    if features.get('url_count', 0) > 3:
        score += 0.15
    elif features.get('url_count', 0) > 1:
        score += 0.05
    
    # Urgency score contribution
    urgency = features.get('urgency_score', 0)
    score += min(urgency * 0.1, 0.3)
    
    # Suspicious keywords contribution
    keyword_count = len(features.get('suspicious_keywords', []))
    score += min(keyword_count * 0.05, 0.25)
    
    # HTML content (phishing often uses HTML)
    if features.get('has_html', False):
        score += 0.05
    
    # Attachment indicators
    if features.get('has_attachments', False):
        score += 0.1
    
    return min(score, 1.0)


class EmailPreprocessor:
    """
    Class-based preprocessor for batch processing of emails.
    """
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
    
    def process(self, content: str) -> dict:
        """
        Process a single email and return full analysis.
        
        Args:
            content: Raw email content
            
        Returns:
            Dictionary with preprocessed text and features
        """
        try:
            preprocessed = preprocess_text(content)
            features = extract_email_features(content)
            suspicion_score = calculate_suspicion_score(features)
            
            self.processed_count += 1
            
            return {
                'preprocessed_text': preprocessed,
                'features': features,
                'suspicion_score': suspicion_score,
                'urls': extract_urls(content),
                'emails': extract_email_addresses(content),
            }
        except Exception as e:
            self.error_count += 1
            logging.error(f"Error processing email: {e}")
            return {
                'preprocessed_text': '',
                'features': {},
                'suspicion_score': 0.0,
                'urls': [],
                'emails': [],
                'error': str(e)
            }
    
    def process_batch(self, contents: list) -> list:
        """
        Process multiple emails.
        
        Args:
            contents: List of raw email contents
            
        Returns:
            List of processed results
        """
        return [self.process(content) for content in contents]
    
    def get_stats(self) -> dict:
        """Get processing statistics."""
        return {
            'processed_count': self.processed_count,
            'error_count': self.error_count,
            'success_rate': (
                self.processed_count / (self.processed_count + self.error_count)
                if (self.processed_count + self.error_count) > 0 else 0
            )
        }
