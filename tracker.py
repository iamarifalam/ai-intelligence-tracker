#!/usr/bin/env python3
"""
AI Intelligence & Research Tracker
Daily automated crawler, benchmark synthesizer, and dataset builder.
Tracks arXiv AI papers, trending Hugging Face models, and generates structured digests.
"""

import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import List, Dict, Any

DATA_DIR = "data"
DAILY_DIR = os.path.join(DATA_DIR, "daily")
SUMMARIES_DIR = "reports"

os.makedirs(DAILY_DIR, exist_ok=True)
os.makedirs(SUMMARIES_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

def fetch_arxiv_papers(max_results: int = 5) -> List[Dict[str, Any]]:
    """Fetch latest AI, Computation and Language, and Machine Learning papers from arXiv."""
    url = f"https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    papers = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            # Namespace for Atom feed
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                published_elem = entry.find('atom:published', ns)
                id_elem = entry.find('atom:id', ns)
                
                title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None and title_elem.text else "Untitled"
                summary = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None and summary_elem.text else ""
                published = published_elem.text.strip() if published_elem is not None and published_elem.text else ""
                link = id_elem.text.strip() if id_elem is not None and id_elem.text else ""
                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns) if a.find('atom:name', ns) is not None]
                
                papers.append({
                    "title": title,
                    "summary": summary[:280] + ("..." if len(summary) > 280 else ""),
                    "published": published,
                    "url": link,
                    "authors": authors[:3] if authors else ["Various Authors"]
                })
    except Exception as e:
        print(f"[-] Warning: Failed to fetch arXiv papers: {e}")
    return papers

def fetch_huggingface_trending(max_results: int = 5) -> List[Dict[str, Any]]:
    """Fetch trending machine learning models from Hugging Face API."""
    url = "https://huggingface.co/api/models?sort=likes7d&direction=-1&limit=" + str(max_results)
    models = []
    try:
        req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode('utf-8'))
            for item in data:
                models.append({
                    "id": item.get("id", ""),
                    "likes": item.get("likes", 0),
                    "downloads": item.get("downloads", 0),
                    "pipeline_tag": item.get("pipeline_tag", "N/A"),
                    "url": f"https://huggingface.co/{item.get('id', '')}"
                })
    except Exception as e:
        print(f"[-] Warning: Failed to fetch Hugging Face trending: {e}")
    return models

def build_daily_digest(papers: List[Dict[str, Any]], models: List[Dict[str, Any]]) -> str:
    """Compile research and model intelligence into a daily markdown digest."""
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    md = []
    md.append(f"# 🤖 Daily AI Intelligence Report — {date_str}\n")
    md.append(f"> *Automated intelligence snapshot generated on `{timestamp_str}`*\n")
    
    md.append("## 📄 Latest Research Papers (arXiv CS.AI / CS.CL / CS.LG)\n")
    if papers:
        for idx, paper in enumerate(papers, 1):
            authors_str = ", ".join(paper["authors"])
            md.append(f"### {idx}. [{paper['title']}]({paper['url']})")
            md.append(f"- **Authors**: {authors_str}")
            md.append(f"- **Published**: `{paper['published']}`")
            md.append(f"- **Abstract Summary**: {paper['summary']}\n")
    else:
        md.append("_No new papers retrieved in this run._\n")

    md.append("## 🔥 Trending Models & Architectures (Hugging Face)\n")
    if models:
        md.append("| Model ID | Task / Pipeline | Likes | Downloads | Link |")
        md.append("| :--- | :--- | :--- | :--- | :--- |")
        for m in models:
            md.append(f"| `{m['id']}` | `{m['pipeline_tag']}` | {m['likes']} | {m['downloads']} | [Inspect Model]({m['url']}) |")
        md.append("")
    else:
        md.append("_No model metrics retrieved in this run._\n")
        
    return "\n".join(md)

def run():
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    
    print(f"[*] Starting AI Intelligence Tracker run for {date_str}...")
    papers = fetch_arxiv_papers(5)
    models = fetch_huggingface_trending(5)
    
    # Save structured raw JSON dataset
    daily_data = {
        "date": date_str,
        "generated_at": now_utc.isoformat(),
        "papers_count": len(papers),
        "models_count": len(models),
        "papers": papers,
        "models": models
    }
    
    json_path = os.path.join(DAILY_DIR, f"ai_intel_{date_str}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(daily_data, f, indent=2)
    print(f"[+] Saved structured dataset to {json_path}")
    
    # Generate and save markdown report
    report_content = build_daily_digest(papers, models)
    report_path = os.path.join(SUMMARIES_DIR, f"report_{date_str}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[+] Saved digest report to {report_path}")
    
    # Update latest summary
    with open(os.path.join(SUMMARIES_DIR, "LATEST.md"), "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[+] Updated {SUMMARIES_DIR}/LATEST.md")

if __name__ == "__main__":
    run()
