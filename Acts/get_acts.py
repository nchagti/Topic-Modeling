import json
from urllib import request
from urllib.error import HTTPError, URLError
from lxml import etree

dracor_api = "https://dracor.org/api/v1"
corpus = "rom"

# Ecerinis info
ecerinis_path = r"C:\Users\dell\Dropbox\Nits\Syracuse\Ecerinis_DH\TEI\Ecerinis.xml"
ecerinis_title = "Ecerinis"
ecerinis_author = "Albertino Mussato"
ecerinis_slug = "mussato-ecerinis"

output_json = "latin_tragedies_acts.json"

# --- helpers  ---

def fetch_json(url: str) -> dict:
    req = request.Request(url, headers={"Accept": "application/json", "User-Agent": "python-urllib"})
    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"[fetch_json] {e.code} {e.reason} for {url}\n{body}")

def fetch_text(url: str) -> str:
    req = request.Request(url, headers={"Accept": "application/xml", "User-Agent": "python-urllib"})
    try:
        with request.urlopen(req, timeout=60) as resp:
            return resp.read().decode("utf-8")
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"[fetch_text] {e.code} {e.reason} for {url}\n{body}")

def parse_tei(xml_text: str) -> etree._Element:
    parser = etree.XMLParser(remove_comments=True, recover=True)
    return etree.fromstring(xml_text.encode("utf-8"), parser=parser)

def tei_ns(root: etree._Element) -> dict:
    ns = root.nsmap.copy()
    if None in ns:
        ns["tei"] = ns.pop(None)
    ns.setdefault("tei", "http://www.tei-c.org/ns/1.0")
    return ns

def text_norm(s: str) -> str:
    return " ".join(s.split())

def extract_spoken_by_act(root: etree._Element) -> list[str]:
    """use TEI to slice acts and collect spoken lines"""
    ns = tei_ns(root)
    acts = root.xpath(".//tei:div[@type='act']", namespaces=ns)
    if acts:
    # If acts exist, break by acts only
        divs = acts
    else:
    # If no acts, break by scenes
        divs = root.xpath(".//tei:div[@type='scene']", namespaces=ns)

    out = []
    for div in divs:
        pieces = []
        # Pull lines inside <sp>, excluding anything in <stage> and excluding <speaker>
        nodes = div.xpath(
            ".//tei:sp//tei:l[not(ancestor::tei:stage)]",
            namespaces=ns,
        )
        if nodes:
            for n in nodes:
                t = text_norm("".join(n.itertext()))
                if t:
                    pieces.append(t)
        else:
            # Fallback: some encodings place text directly under <sp>
            for sp in div.xpath(".//tei:sp", namespaces=ns):
                for child in sp.iterchildren():
                    tag = etree.QName(child).localname.lower()
                    if tag in ("stage", "speaker"):
                        continue
                    t = text_norm("".join(child.itertext()))
                    if t:
                        pieces.append(t)

        out.append("\n".join(pieces).strip())

    # Accept more than 5 acts
    return [a for a in out if a]

def is_seneca(meta: dict) -> bool:
    return "seneca" in (meta.get("firstAuthor") or "").lower()

def has_title(meta: dict) -> bool:
    return (meta.get("title") or "").strip()

# def _self_test():
  #  print(fetch_json("https://dracor.org/api/v1/info"))
   # print(fetch_json("https://dracor.org/api/v1/corpora/rom/metadata")[:1])  # first item


# --- main pipeline ---

def main():
    plays_meta = fetch_json(f"{dracor_api}/corpora/{corpus}/metadata")

    # Debugging
   # for m in plays_meta[:5]:  # show first 5
    #    print({k: m[k] for k in ("name", "title", "firstAuthor") if k in m})


    # Filter Seneca only via JSON metadata
    seneca = [m for m in plays_meta if is_seneca(m) and has_title(m) and m.get("name")]

    out = []
    problems = []

    # Build from DraCor plays
    for m in seneca:
        play_slug = m["name"]                # e.g., "seneca-medea"
        title = m.get("title", "")   # from JSON metadata
        author = m.get("firstAuthor", "") # from JSON metadata

        tei_url = f"{dracor_api}/corpora/{corpus}/plays/{play_slug}/tei"
        try:
            tei_xml = fetch_text(tei_url)
            root = parse_tei(tei_xml)
            acts = extract_spoken_by_act(root)
            for i, act_text in enumerate(acts, start=1):
                out.append({
                    "id": f"{play_slug}_act{i}",
                    "play_slug": play_slug,
                    "title": title,
                    "author": author,
                    "act": i,
                    "text": act_text
                    })
        except (HTTPError, URLError, Exception) as e:
            problems.append(f"{play_slug}: {e}")

    # Add Ecerinis
    if ecerinis_path:
        try:
            with open(ecerinis_path, "r", encoding="utf-8") as f:
                eci_xml = f.read()
            root = parse_tei(eci_xml)
            acts = extract_spoken_by_act(root)
            for i, act_text in enumerate(acts, start=1):
                out.append({
                    "id": f"{ecerinis_slug}_act{i}",
                    "play_slug": ecerinis_slug,
                    "title": ecerinis_title,
                    "author": ecerinis_author,
                    "act": i, "text": act_text
                    })
        except FileNotFoundError:
            problems.append(f"Ecerinis TEI not found at {ecerinis_path}")
        except Exception as e:
            problems.append(f"Ecerinis parse/extract failed: {e}")

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(out)} act-level docs → {output_json}")
    if problems:
        print("Issues:")
        for p in problems:
            print(" -", p)


if __name__ == "__main__":
    main()
