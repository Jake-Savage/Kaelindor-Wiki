#!/usr/bin/env python3
"""Static-site generator for the Kaelindor campaign knowledge base.

Reads the markdown source of truth in ``kb/`` and renders a searchable static
HTML wiki into ``site/``. Dependency-light: only PyYAML (for frontmatter) plus
the standard library. A compact built-in markdown renderer handles the subset of
markdown the KB uses, and resolves ``[[id]]`` / ``[[id|text]]`` wikilinks to
internal links — reporting any that don't resolve.

Usage:
    py generator/build.py            # build into ./site
    py generator/build.py --serve    # build, then serve site/ on localhost:8000
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required. Install it with:  py -m pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / "kb"
SITE = ROOT / "site"
TEMPLATES = ROOT / "generator" / "templates"
STATIC = ROOT / "generator" / "static"

# Display order + labels for entity types. (sessions handled specially.)
TYPES = [
    ("characters", "Characters"),
    ("locations", "Locations"),
    ("quests", "Quests"),
    ("factions", "Factions"),
    ("items", "Items"),
    ("lore", "Lore"),
    ("sessions", "Sessions"),
]
TYPE_LABEL = dict(TYPES)


# --------------------------------------------------------------------------- #
# Frontmatter + markdown                                                       #
# --------------------------------------------------------------------------- #
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_frontmatter(text: str):
    """Return (meta dict, body str). Tolerates files without frontmatter."""
    m = FM_RE.match(text)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        print(f"  ! YAML error: {exc}")
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, body


_WIKILINK = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]")
_MDLINK = re.compile(r"\[([^\]]+?)\]\(([^)]+?)\)")
_BOLD = re.compile(r"\*\*([^*]+?)\*\*")
_ITALIC = re.compile(r"(?<!\*)\*(?!\*)([^*]+?)\*(?!\*)")
_CODE = re.compile(r"`([^`]+?)`")


def render_inline(text, ctx):
    """Inline markdown -> HTML, resolving wikilinks via ctx['index']."""
    code_spans = []

    def stash_code(m):
        code_spans.append(m.group(1))
        return f"\x00CODE{len(code_spans) - 1}\x00"

    text = _CODE.sub(stash_code, text)
    text = html.escape(text, quote=False)

    def wiki(m):
        target = m.group(1).strip()
        label = (m.group(2) or "").strip()
        entry = ctx["index"].get(target)
        if entry:
            disp = label or entry["title"]
            url = ctx["root"] + entry["url"]
            badge = entry["type"][:1].upper()
            return (f'<a class="xref xref-{entry["type"]}" href="{url}" '
                    f'title="{html.escape(entry["title"])}">{html.escape(disp)}'
                    f'<span class="xref-badge">{badge}</span></a>')
        # unresolved
        ctx["broken"].append((ctx["id"], target))
        disp = label or target
        return (f'<span class="broken-link" '
                f'title="unresolved reference: {html.escape(target)}">'
                f'{html.escape(disp)}</span>')

    text = _WIKILINK.sub(wiki, text)
    text = _MDLINK.sub(r'<a href="\2">\1</a>', text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)

    def restore_code(m):
        return f"<code>{html.escape(code_spans[int(m.group(1))], quote=False)}</code>"

    text = re.sub(r"\x00CODE(\d+)\x00", restore_code, text)
    return text


def render_markdown(body, ctx):
    """A small block-level markdown renderer for the KB's subset."""
    lines = body.split("\n")
    out = []
    i = 0
    n = len(lines)

    def flush_para(buf):
        if buf:
            out.append("<p>" + render_inline(" ".join(buf).strip(), ctx) + "</p>")
            buf.clear()

    para: list[str] = []
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para(para)
            i += 1
            continue

        # heading
        hm = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if hm:
            flush_para(para)
            level = len(hm.group(1))
            out.append(f"<h{level}>{render_inline(hm.group(2), ctx)}</h{level}>")
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_para(para)
            out.append("<hr>")
            i += 1
            continue

        # blockquote (consecutive)
        if stripped.startswith(">"):
            flush_para(para)
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append("<blockquote>" + render_inline(" ".join(quote), ctx) + "</blockquote>")
            continue

        # list (unordered, one level of nesting via indentation)
        if re.match(r"^\s*[-*]\s+", line):
            flush_para(para)
            out.append(render_list(lines, i, ctx, _consume=False)[0])
            i = render_list(lines, i, ctx, _consume=False)[1]
            continue

        # plain paragraph line
        para.append(stripped)
        i += 1

    flush_para(para)
    return "\n".join(out)


def render_list(lines, start, ctx, _consume=True):
    """Render an unordered list starting at ``start``. Returns (html, next_index)."""
    n = len(lines)
    i = start
    base_indent = len(lines[i]) - len(lines[i].lstrip())
    html_parts = ["<ul>"]
    while i < n:
        line = lines[i]
        if not line.strip():
            # allow blank line only if next is still a list item
            if i + 1 < n and re.match(r"^\s*[-*]\s+", lines[i + 1]):
                i += 1
                continue
            break
        m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        if not m:
            break
        indent = len(m.group(1))
        if indent < base_indent:
            break
        if indent > base_indent:
            sub_html, i = render_list(lines, i, ctx)
            # attach nested list to the previous <li>
            if html_parts and html_parts[-1].endswith("</li>"):
                html_parts[-1] = html_parts[-1][:-5] + sub_html + "</li>"
            else:
                html_parts.append(sub_html)
            continue
        html_parts.append("<li>" + render_inline(m.group(2), ctx) + "</li>")
        i += 1
    html_parts.append("</ul>")
    return "\n".join(html_parts), i


def strip_markdown(body):
    """Plain-text version of a body for the search index."""
    text = _WIKILINK.sub(lambda m: (m.group(2) or m.group(1)), body)
    text = _MDLINK.sub(r"\1", text)
    text = re.sub(r"[#>*`_-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# --------------------------------------------------------------------------- #
# Loading the KB                                                               #
# --------------------------------------------------------------------------- #
def url_for(etype, eid):
    return f"{etype}/{eid}.html"


def load_entities():
    entities = []
    for etype, _ in TYPES:
        d = KB / etype
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            meta, body = parse_frontmatter(text)
            eid = meta.get("id") or path.stem
            if eid != path.stem:
                print(f"  ! {path.name}: id '{eid}' != filename '{path.stem}'")
            entities.append({
                "id": eid,
                "etype": etype,
                "title": meta.get("title") or eid.replace("-", " ").title(),
                "summary": meta.get("summary", ""),
                "meta": meta,
                "body": body,
                "url": url_for(etype, eid),
                "tags": meta.get("tags", []) or [],
            })
    return entities


# --------------------------------------------------------------------------- #
# Rendering pages                                                              #
# --------------------------------------------------------------------------- #
def reset_site():
    """Empty site/ in place, retrying past transient Windows file locks."""
    import time
    SITE.mkdir(parents=True, exist_ok=True)
    for child in SITE.iterdir():
        for attempt in range(3):
            try:
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
                break
            except (PermissionError, OSError):
                if attempt == 2:
                    print(f"  ! could not remove {child} (in use?) — leaving stale copy")
                    break
                time.sleep(0.3)


def load_base():
    return (TEMPLATES / "base.html").read_text(encoding="utf-8")


def nav_html(root, active=None):
    parts = []
    for etype, label in TYPES:
        cls = "active" if etype == active else ""
        parts.append(f'<a class="{cls}" href="{root}{etype}/index.html">{label}</a>')
    return "".join(parts)


def page(base, title, root, content, active=None):
    return (base
            .replace("%%TITLE%%", html.escape(title))
            .replace("%%ROOT%%", root)
            .replace("%%NAV%%", nav_html(root, active))
            .replace("%%CONTENT%%", content))


def meta_chips(meta):
    """Render selected frontmatter fields as a chip list on entity pages."""
    skip = {"id", "type", "title", "summary", "tags"}
    chips = []
    for k, v in meta.items():
        if k in skip or v in (None, "", [], {}):
            continue
        if isinstance(v, list):
            if v and isinstance(v[0], dict):
                continue  # relationships handled separately
            val = ", ".join(str(x) for x in v)
        else:
            val = str(v)
        chips.append(f'<span class="chip"><b>{html.escape(k.replace("_", " "))}:</b> '
                     f'{html.escape(val)}</span>')
    return '<div class="chips">' + "".join(chips) + "</div>" if chips else ""


def entity_page(base, e, ctx):
    root = "../"
    ctx["id"] = e["id"]
    parts = [f'<article class="entity entity-{e["etype"]}">']
    parts.append(f'<p class="crumb"><a href="{root}{e["etype"]}/index.html">'
                 f'{TYPE_LABEL[e["etype"]]}</a> / {html.escape(e["title"])}</p>')
    parts.append(f"<h1>{html.escape(e['title'])}</h1>")
    if e["summary"]:
        parts.append(f'<p class="summary">{render_inline(e["summary"], ctx)}</p>')
    parts.append(meta_chips(e["meta"]))
    # relationships, if present
    rels = e["meta"].get("relationships")
    if isinstance(rels, list) and rels and isinstance(rels[0], dict):
        parts.append('<div class="rels"><h3>Relationships</h3><ul>')
        for r in rels:
            who = r.get("who", "")
            note = r.get("note", "")
            link = render_inline(f"[[{who}]]", ctx) if who in ctx["index"] else html.escape(str(who))
            parts.append(f"<li>{link} — {render_inline(str(note), ctx)}</li>")
        parts.append("</ul></div>")
    parts.append('<div class="body">')
    parts.append(render_markdown(e["body"], ctx))
    parts.append("</div></article>")
    # backlinks
    back = ctx["backlinks"].get(e["id"])
    if back:
        parts.append('<aside class="backlinks"><h3>Referenced by</h3><ul>')
        for bid in sorted(back):
            be = ctx["by_id"][bid]
            parts.append(f'<li>{render_inline("[[" + bid + "]]", ctx)} '
                         f'<span class="muted">({TYPE_LABEL[be["etype"]]})</span></li>')
        parts.append("</ul></aside>")
    return page(base, e["title"], root, "\n".join(parts), active=e["etype"])


def session_sort_key(e):
    m = e["meta"]
    return (m.get("chapter", 0) or 0, m.get("number", 0) or 0, e["id"])


def index_page(base, etype, label, entities, ctx):
    root = "../"
    ctx["id"] = f"{etype}-index"
    items = [e for e in entities if e["etype"] == etype]
    if etype == "sessions":
        items.sort(key=session_sort_key)
    else:
        items.sort(key=lambda e: e["title"].lower())
    parts = [f"<h1>{label}</h1>",
             f'<p class="muted">{len(items)} entries.</p>']
    if etype == "sessions":
        parts.append('<ol class="card-list session-list">')
        for e in items:
            m = e["meta"]
            date = m.get("date_inworld") or m.get("date_real") or ""
            label_num = f"S{m.get('chapter','?')}.{str(m.get('number','?')).zfill(2)}"
            parts.append(
                f'<li class="card"><a href="{root}{e["url"]}">'
                f'<span class="card-tag">{label_num}</span>'
                f'<span class="card-title">{html.escape(e["title"])}</span></a>'
                f'<span class="card-date muted">{html.escape(str(date))}</span>'
                f'<p>{render_inline(e["summary"], ctx)}</p></li>')
        parts.append("</ol>")
    else:
        parts.append('<ul class="card-list">')
        for e in items:
            parts.append(
                f'<li class="card"><a href="{root}{e["url"]}">'
                f'<span class="card-title">{html.escape(e["title"])}</span></a>'
                f'<p>{render_inline(e["summary"], ctx)}</p></li>')
        parts.append("</ul>")
    return page(base, label, root, "\n".join(parts), active=etype)


def home_page(base, entities, ctx):
    ctx["id"] = "index"
    root = ""
    # intro from kb/index.md if present
    intro = ""
    idx = KB / "index.md"
    if idx.exists():
        _, ibody = parse_frontmatter(idx.read_text(encoding="utf-8"))
        intro = render_markdown(ibody, ctx)
    parts = ['<div class="home">']
    if intro:
        parts.append(f'<section class="intro">{intro}</section>')
    # section cards with counts
    parts.append('<section class="sections"><h2>Browse the codex</h2><div class="grid">')
    for etype, label in TYPES:
        count = sum(1 for e in entities if e["etype"] == etype)
        parts.append(f'<a class="section-card" href="{root}{etype}/index.html">'
                     f'<span class="section-title">{label}</span>'
                     f'<span class="section-count">{count}</span></a>')
    parts.append("</div></section>")
    # active quests
    active_quests = [e for e in entities if e["etype"] == "quests"
                     and str(e["meta"].get("status", "")).lower() == "active"]
    active_quests.sort(key=lambda e: 0 if e["meta"].get("priority") == "main" else 1)
    if active_quests:
        parts.append('<section class="active-quests"><h2>Active threads</h2><ul>')
        for e in active_quests:
            pr = " — <b>main</b>" if e["meta"].get("priority") == "main" else ""
            parts.append(f'<li>{render_inline("[[" + e["id"] + "]]", ctx)}{pr}<br>'
                         f'<span class="muted">{render_inline(e["summary"], ctx)}</span></li>')
        parts.append("</ul></section>")
    # latest sessions
    sessions = sorted((e for e in entities if e["etype"] == "sessions"),
                      key=session_sort_key, reverse=True)[:5]
    if sessions:
        parts.append('<section class="latest"><h2>Latest sessions</h2><ul>')
        for e in sessions:
            parts.append(f'<li>{render_inline("[[" + e["id"] + "]]", ctx)}<br>'
                         f'<span class="muted">{render_inline(e["summary"], ctx)}</span></li>')
        parts.append("</ul></section>")
    parts.append("</div>")
    return page(base, "Home", root, "\n".join(parts))


def search_page(base):
    root = ""
    content = (
        '<h1>Search</h1>'
        '<form id="search-form" class="search-page-form" onsubmit="return false;">'
        '<input type="search" id="search-input" placeholder="Search characters, places, quests, lore…" '
        'autofocus autocomplete="off"></form>'
        '<p class="muted" id="search-status"></p>'
        '<div id="search-results"></div>'
    )
    return page(base, "Search", root, content, active=None)


# --------------------------------------------------------------------------- #
# Main build                                                                   #
# --------------------------------------------------------------------------- #
def build():
    entities = load_entities()
    by_id = {e["id"]: e for e in entities}
    index = {e["id"]: {"type": e["etype"], "title": e["title"], "url": e["url"]}
             for e in entities}

    # compute backlinks by scanning wikilinks in each body
    backlinks: dict[str, set] = {}
    for e in entities:
        for m in _WIKILINK.finditer(e["body"]):
            tgt = m.group(1).strip()
            if tgt in index and tgt != e["id"]:
                backlinks.setdefault(tgt, set()).add(e["id"])

    ctx = {"index": index, "by_id": by_id, "backlinks": backlinks,
           "root": "../", "id": "", "broken": []}

    # reset output — clean contents in place (robust against Windows file locks,
    # which can block removing the top-level directory itself)
    reset_site()
    shutil.copytree(STATIC, SITE / "static", dirs_exist_ok=True)

    base = load_base()

    # entity pages
    for e in entities:
        ctx["root"] = "../"
        out = SITE / e["etype"] / f"{e['id']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(entity_page(base, e, ctx), encoding="utf-8")

    # type index pages
    for etype, label in TYPES:
        ctx["root"] = "../"
        out = SITE / etype / "index.html"
        out.write_text(index_page(base, etype, label, entities, ctx), encoding="utf-8")

    # home + search
    ctx["root"] = ""
    (SITE / "index.html").write_text(home_page(base, entities, ctx), encoding="utf-8")
    (SITE / "search.html").write_text(search_page(base), encoding="utf-8")

    # search index
    search_docs = []
    for e in entities:
        search_docs.append({
            "id": e["id"],
            "type": e["etype"],
            "title": e["title"],
            "summary": e["summary"],
            "url": e["url"],
            "tags": e["tags"],
            "text": strip_markdown(e["body"])[:4000],
        })
    (SITE / "search-index.json").write_text(
        json.dumps(search_docs, ensure_ascii=False), encoding="utf-8")

    # report
    print(f"Built {len(entities)} pages into {SITE}")
    for etype, label in TYPES:
        print(f"  {label:12} {sum(1 for e in entities if e['etype'] == etype)}")
    broken = ctx["broken"]
    if broken:
        uniq = sorted(set(broken))
        print(f"\n  {len(uniq)} unresolved [[wikilinks]]:")
        for src, tgt in uniq:
            print(f"    {src}  ->  [[{tgt}]]")
    else:
        print("\n  All wikilinks resolved.")
    return entities, broken


def serve():
    import http.server
    import socketserver
    import os
    os.chdir(SITE)
    port = 8000
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"Serving {SITE} at http://localhost:{port}  (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
