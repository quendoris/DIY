#!/usr/bin/env python3
"""Discover Wavecor's actual linked response datasets without inventing URLs.

This is a provenance discovery step, NOT an acoustic model.
"""
from __future__ import annotations
import json
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

PAGES = {
    "LOW": "https://www.wavecor.com/html/wf168wa05_06.html",
    "MID": "https://www.wavecor.com/html/mr120bd01_02_03_04.html",
    "HIGH": "https://www.wavecor.com/html/tw030wa21_22.html",
}

class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._href = None
        self._text = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self._href = dict(attrs).get("href")
            self._text = []
    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)
    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []

def discover_one(url: str) -> dict:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (research provenance; DIY loudspeaker project)"})
    with urlopen(req, timeout=25) as response:
        raw = response.read(1_000_000)
        charset = response.headers.get_content_charset() or "utf-8"
    p = LinkCollector()
    p.feed(raw.decode(charset, errors="replace"))
    links=[]
    for href, label in p.links:
        if any(token in (href+" "+label).lower()
               for token in (".txt","spl response","impedance response","download")):
            dest=urljoin(url,href)
            links.append({"text":label,"url":dest,
                          "same_origin":urlparse(dest).hostname in ("wavecor.com","www.wavecor.com")})
    return {"page":url,"response_bytes":len(raw),"relevant_links":links}

if __name__ == "__main__":
    out=[]
    for name,url in PAGES.items():
        try:
            out.append({"name":name,**discover_one(url)})
        except Exception as exc:
            out.append({"name":name,"page":url,"error":str(exc)})
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if any("error" in x for x in out):
        sys.exit(2)
