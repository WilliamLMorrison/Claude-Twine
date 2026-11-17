"""Sync the Twee source into the compiled index.html.

Usage:  python3 build.py            # updates index.html from Adventure(1).twee
        python3 build.py --check    # only reports passages that differ

Passage text, the StoryStylesheet and the StoryScript are copied from the
.twee file into the matching elements of index.html (Harlowe engine untouched).
"""
import html, re, sys

TWEE = "Adventure(1).twee"
HTML = "index.html"


def unescape_name(raw):
    return re.sub(r"\\(.)", r"\1", raw)


def parse_twee(text):
    passages = {}
    parts = re.split(r"^:: ", text, flags=re.M)[1:]
    for part in parts:
        header, _, body = part.partition("\n")
        m = re.match(r"((?:\\.|[^\\\[{])*?)\s*(?:\[([^\]]*)\])?\s*(?:\{.*\})?\s*$", header)
        name = unescape_name(m.group(1))
        passages[name] = {"tags": (m.group(2) or "").split(), "body": body.rstrip("\n")}
    return passages


def esc(s):
    return html.escape(s, quote=True)


def main():
    check = "--check" in sys.argv
    passages = parse_twee(open(TWEE, encoding="utf-8").read())
    doc = open(HTML, encoding="utf-8").read()
    changed = []

    def repl_passage(m):
        attrs, body = m.group(1), m.group(2)
        name = html.unescape(re.search(r'name="([^"]*)"', attrs).group(1))
        if name not in passages:
            raise SystemExit(f"passage {name!r} is in index.html but not in the twee")
        new = esc(passages[name]["body"])
        if new != body:
            changed.append(name)
        return f"<tw-passagedata{attrs}>{new}</tw-passagedata>"

    doc = re.sub(r"<tw-passagedata([^>]*)>(.*?)</tw-passagedata>", repl_passage, doc, flags=re.S)

    for pname, tag, ident in (("StoryStylesheet", "style", "twine-user-stylesheet"),
                              ("StoryScript", "script", "twine-user-script")):
        if pname not in passages:
            continue
        pat = re.compile(rf'(<{tag} role="[^"]*" id="{ident}"[^>]*>)(.*?)(</{tag}>)', re.S)
        m = pat.search(doc)
        new = passages[pname]["body"]
        if m.group(2) != new:
            changed.append(pname)
        doc = doc[:m.start(2)] + new + doc[m.end(2):]

    print("differs:" if check else "updated:", ", ".join(changed) or "nothing")
    if not check:
        open(HTML, "w", encoding="utf-8").write(doc)


if __name__ == "__main__":
    main()
