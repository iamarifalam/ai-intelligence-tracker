#!/usr/bin/env python3
"""
Daily ingestion pipeline for arXiv research papers and Hugging Face model metadata.
"""

import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any, Dict, List

DATA_DIR = "data"
DAILY_DIR = os.path.join(DATA_DIR, "daily")
SUMMARIES_DIR = "reports"

os.makedirs(DAILY_DIR, exist_ok=True)
os.makedirs(SUMMARIES_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


def fetch_arxiv_papers(max_results: int = 5) -> List[Dict[str, Any]]:
    """Fetch latest machine learning papers from arXiv API."""
    url = f"https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    papers = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)

            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns):
                title_elem = entry.find("atom:title", ns)
                summary_elem = entry.find("atom:summary", ns)
                published_elem = entry.find("atom:published", ns)
                id_elem = entry.find("atom:id", ns)

                title = (
                    title_elem.text.strip().replace("\n", " ")
                    if title_elem is not None and title_elem.text
                    else "Untitled"
                )
                summary = (
                    summary_elem.text.strip().replace("\n", " ")
                    if summary_elem is not None and summary_elem.text
                    else ""
                )
                published = (
                    published_elem.text.strip()
                    if published_elem is not None and published_elem.text
                    else ""
                )
                link = (
                    id_elem.text.strip()
                    if id_elem is not None and id_elem.text
                    else ""
                )
                authors = [
                    a.find("atom:name", ns).text
                    for a in entry.findall("atom:author", ns)
                    if a.find("atom:name", ns) is not None
                ]

                papers.append(
                    {
                        "title": title,
                        "summary": summary[:280] + ("..." if len(summary) > 280 else ""),
                        "published": published,
                        "url": link,
                        "authors": authors[:3] if authors else ["Various Authors"],
                    }
                )
    except Exception as e:
        print(f"[-] Warning: Failed to fetch arXiv papers: {e}")
    return papers


def fetch_huggingface_trending(max_results: int = 5) -> List[Dict[str, Any]]:
    """Fetch trending machine learning models from Hugging Face API."""
    url = f"https://huggingface.co/api/models?sort=likes7d&direction=-1&limit={max_results}"
    models = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
            for item in data:
                models.append(
                    {
                        "id": item.get("id", ""),
                        "likes": item.get("likes", 0),
                        "downloads": item.get("downloads", 0),
                        "pipeline_tag": item.get("pipeline_tag", "N/A"),
                        "url": f"https://huggingface.co/{item.get('id', '')}",
                    }
                )
    except Exception as e:
        print(f"[-] Warning: Failed to fetch Hugging Face trending: {e}")
    return models


def build_daily_digest(papers: List[Dict[str, Any]], models: List[Dict[str, Any]]) -> str:
    """Format daily research and model metrics into markdown summary."""
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    timestamp_str = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = []
    lines.append(f"# Daily Research Summary ({date_str})\n")
    lines.append(f"Generated at: `{timestamp_str}`\n")

    lines.append("## arXiv Papers (cs.AI, cs.CL, cs.LG)\n")
    if papers:
        for idx, paper in enumerate(papers, 1):
            authors_str = ", ".join(paper["authors"])
            lines.append(f"### {idx}. [{paper['title']}]({paper['url']})")
            lines.append(f"- Authors: {authors_str}")
            lines.append(f"- Published: `{paper['published']}`")
            lines.append(f"- Summary: {paper['summary']}\n")
    else:
        lines.append("No new papers retrieved in this cycle.\n")

    lines.append("## Trending Models (Hugging Face)\n")
    if models:
        lines.append("| Model ID | Pipeline | Likes | Downloads | Source |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for m in models:
            lines.append(
                f"| `{m['id']}` | `{m['pipeline_tag']}` | {m['likes']} | {m['downloads']} | [Link]({m['url']}) |"
            )
        lines.append("")
    else:
        lines.append("No model metrics retrieved in this cycle.\n")

    return "\n".join(lines)


def run():
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")

    print(f"Starting data ingestion for {date_str}...")
    papers = fetch_arxiv_papers(5)
    models = fetch_huggingface_trending(5)

    daily_data = {
        "date": date_str,
        "generated_at": now_utc.isoformat(),
        "papers_count": len(papers),
        "models_count": len(models),
        "papers": papers,
        "models": models,
    }

    json_path = os.path.join(DAILY_DIR, f"ai_intel_{date_str}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(daily_data, f, indent=2)
    print(f"Saved dataset to {json_path}")

    report_content = build_daily_digest(papers, models)
    report_path = os.path.join(SUMMARIES_DIR, f"report_{date_str}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Saved report to {report_path}")

    with open(os.path.join(SUMMARIES_DIR, "LATEST.md"), "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"Updated {SUMMARIES_DIR}/LATEST.md")


if __name__ == "__main__":
    run()
