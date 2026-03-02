#!/usr/bin/env python3
"""
Article SEO Optimizer & Keyword Researcher

Fetches an article, performs keyword research using free sources (Google Autocomplete),
analyzes content, and suggests full paragraph replacements to improve SEO.

Usage:
    python article_seo.py https://example.com/article
    python article_seo.py https://example.com/article --json
"""

import argparse
import json
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from collections import Counter
import math


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_h1 = False
        self.in_h2 = False
        self.in_h3 = False
        self.in_p = False
        
        self.title = ""
        self.h1 = []
        self.h2s = []
        self.h3s = []
        self.paragraphs = []
        self.meta_description = ""
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
        elif tag == "h2":
            self.in_h2 = True
        elif tag == "h3":
            self.in_h3 = True
        elif tag == "p":
            self.in_p = True
            self.in_p_continued = False
        elif tag == "meta":
            if attrs_dict.get("name", "").lower() == "description":
                self.meta_description = attrs_dict.get("content", "")
            elif attrs_dict.get("property", "").lower() == "og:description":
                if not self.meta_description:
                    self.meta_description = attrs_dict.get("content", "")
        elif tag == "img":
            self.images.append({
                "src": attrs_dict.get("src", ""),
                "alt": attrs_dict.get("alt", "")
            })

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
        elif tag == "h2":
            self.in_h2 = False
        elif tag == "h3":
            self.in_h3 = False
        elif tag == "p":
            self.in_p = False

    def handle_data(self, data):
        # Handle data text node within tags
        data = data.replace('\n', ' ').replace('\r', ' ').strip()
        if not data:
            return
            
        if self.in_title:
            self.title += data + " "
        elif self.in_h1:
            self.h1.append(data)
        elif self.in_h2:
            self.h2s.append(data)
        elif self.in_h3:
            self.h3s.append(data)
        elif self.in_p:
            if not getattr(self, 'in_p_continued', False):
                self.paragraphs.append(data)
                self.in_p_continued = True
            else:
                self.paragraphs[-1] += " " + data


def fetch_html(url: str) -> str:
    """Fetch HTML content from a URL."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return ""


def get_google_autocomplete(query: str) -> list:
    """Fetch autocomplete suggestions from Google (free, no API key)."""
    try:
        url = f"http://suggestqueries.google.com/complete/search?client=chrome&q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if len(data) >= 2 and isinstance(data[1], list):
                return data[1]
    except Exception:
        pass
    return []


def extract_keywords_tfidf(text: str, top_n: int = 10) -> list:
    """Basic term extraction (pseudo-TF-IDF focusing on multi-word phrases)."""
    # Extended stop words list
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "of", "from", "as", 
        "is", "are", "was", "were", "be", "been", "this", "that", "these", "those", "it", "he", "she", "they", 
        "we", "you", "i", "your", "my", "their", "our", "its", "which", "who", "whom", "whose", "what", "where", 
        "when", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", 
        "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just", "should"
    }
    
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    filtered_words = [w for w in words if w not in stop_words]
    
    # Simple bigram and trigram extraction
    bigrams = [f"{filtered_words[i]} {filtered_words[i+1]}" for i in range(len(filtered_words)-1)]
    trigrams = [f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}" for i in range(len(filtered_words)-2)]
    
    word_counts = Counter(filtered_words)
    bigram_counts = Counter(bigrams)
    trigram_counts = Counter(trigrams)
    
    # Combine and score (favor bigrams and trigrams)
    scored = []
    for term, count in word_counts.items():
        if count > 3:
            scored.append((term, count))
    for term, count in bigram_counts.items():
        if count > 2:
            scored.append((term, count * 3.0)) # 3x weight for bigrams
    for term, count in trigram_counts.items():
        if count > 1:
            scored.append((term, count * 5.0)) # 5x weight for trigrams
            
    scored.sort(key=lambda x: x[1], reverse=True)
    
    # Deduplicate (if bigram contains unigram, keep bigram)
    final_terms = []
    for term, _ in scored:
        if not any(term in t and term != t for t, _ in scored[:top_n*3]):
            final_terms.append(term)
        if len(final_terms) >= top_n:
            break
            
    return final_terms


def main():
    parser = argparse.ArgumentParser(description="Article SEO Extractor & Keyword Researcher")
    parser.add_argument("url", help="URL of the article to optimize")
    parser.add_argument("--keyword", help="Target primary keyword (optional, will extract if not provided)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    html = fetch_html(args.url)
    if not html:
        print(json.dumps({"error": "Failed to fetch URL"}) if args.json else "Error: Failed to fetch URL")
        return

    # Parse HTML
    article_parser = ArticleParser()
    article_parser.feed(html)
    
    # 1. Keyword Research
    full_text = " ".join(article_parser.h1 + article_parser.h2s + article_parser.paragraphs)
    extracted_kws = extract_keywords_tfidf(full_text)
    
    target_kw = args.keyword.lower() if args.keyword else (extracted_kws[0] if extracted_kws else "")
    
    lsi_kws = []
    if target_kw:
        # Get Google Autocomplete suggestions for the target keyword
        lsi_kws = get_google_autocomplete(target_kw)
        
    # Filter out the exact target keyword from LSI list
    lsi_kws = [kw for kw in lsi_kws if kw.lower() != target_kw.lower()]
    
    # If autocomplete failed or returned few, fallback to TF-IDF extracted words
    if len(lsi_kws) < 5:
        lsi_kws.extend([kw for kw in extracted_kws if kw not in lsi_kws and kw != target_kw])

    # 2. Output
    result = {
        "url": args.url,
        "title": article_parser.title.strip(),
        "meta_description": article_parser.meta_description.strip(),
        "headings": {
            "h1": article_parser.h1,
            "h2": article_parser.h2s,
            "h3": article_parser.h3s
        },
        "paragraphs": [p for p in article_parser.paragraphs if len(p.split()) > 10], # Skip tiny fragments
        "images": article_parser.images,
        "word_count": len(full_text.split()),
        "target_keyword": target_kw,
        "lsi_keywords": lsi_kws[:15]
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Article SEO Extractor: {args.url}")
        print("="*50)
        print(f"Title: {result['title']}")
        print(f"Meta: {result['meta_description'][:100]}...")
        print(f"H1 Count: {len(result['headings']['h1'])}")
        print(f"H2 Count: {len(result['headings']['h2'])}")
        print(f"Word Count: {result['word_count']} words")
        print(f"Target Keyword (Estimated): '{result['target_keyword']}'")
        print(f"LSI & Related Keywords: {', '.join(result['lsi_keywords'])}")
        print("\nNote: Use the --json flag to pipe this extracted data into an LLM for SEO analysis.")


if __name__ == "__main__":
    main()
