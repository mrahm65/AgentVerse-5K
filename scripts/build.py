#!/usr/bin/env python3
"""Generate the 5000-AI-Agents-Projects markdown project from the source JSON."""
import json, re
from collections import defaultdict, Counter
from pathlib import Path
from datetime import datetime

ROOT = Path("/sessions/admiring-modest-heisenberg/mnt/outputs/5000-AI-Agents-Projects")
CAT_DIR = ROOT / "categories"
CAT_DIR.mkdir(parents=True, exist_ok=True)

data = json.load(open("/sessions/admiring-modest-heisenberg/mnt/uploads/repos_5080_all_unique.json"))
repos = data["repos"]

CATEGORIES = {
    "mcp-servers":      ("MCP Servers",             "Model Context Protocol servers and clients.",       "🔌"),
    "voice-agents":     ("Voice Agents",            "Speech-first conversational agents and pipelines.", "🎙️"),
    "coding-agents":    ("Coding Agents",           "Agents that write, edit, review or run code.",      "💻"),
    "langgraph":        ("LangGraph",               "Agents and workflows built with LangGraph.",        "🕸️"),
    "autogen":          ("AutoGen",                 "Microsoft AutoGen agents and multi-agent systems.", "🤝"),
    "crewai":           ("CrewAI",                  "Crew-style multi-agent collaboration projects.",    "👥"),
    "tool-calling":     ("Tool-Calling Agents",     "Function-calling, tool-use, and ReAct style agents.","🛠️"),
    "agent-frameworks": ("Agent Frameworks",        "Libraries and frameworks for building agents.",     "🏗️"),
    "agentic-ai":       ("Agentic AI",              "General agentic-AI applications and demos.",        "🤖"),
    "autonomous":       ("Autonomous Agents",       "Fully autonomous, goal-driven agents.",             "🧭"),
    "llm-agents":       ("LLM Agents",              "General LLM-based agent projects.",                 "🧠"),
    "lang-rust":        ("Rust Agents",             "Agent projects written in Rust.",                   "🦀"),
    "lang-go":          ("Go Agents",               "Agent projects written in Go.",                     "🐹"),
    "lang-typescript":  ("TypeScript Agents",       "Agent projects written in TypeScript.",             "🟦"),
    "lang-python":      ("Python Agents",           "Agent projects written in Python.",                 "🐍"),
    "lang-javascript":  ("JavaScript Agents",       "Agent projects written in JavaScript.",             "🟨"),
    "trending":         ("Trending (50+ stars)",    "Highest-velocity repos in the dataset.",            "🔥"),
    "all":              ("All Repositories",        "Every repo in the dataset.",                        "📚"),
}

def bucket(r):
    bs = set()
    q = (r.get("source_query") or "").lower()
    lang = (r.get("language") or "").lower()
    desc = (r.get("description") or "").lower()
    if "mcp-server" in q or "mcp server" in desc or " mcp " in f" {desc} ": bs.add("mcp-servers")
    if "voice-agent" in q or "voice agent" in desc or "speech" in desc: bs.add("voice-agents")
    if "coding-agent" in q or "coding agent" in desc or "code agent" in desc: bs.add("coding-agents")
    if "langgraph" in q or "langgraph" in desc: bs.add("langgraph")
    if "autogen" in q or "autogen" in desc: bs.add("autogen")
    if "crewai" in q or "crewai" in desc or "crew ai" in desc: bs.add("crewai")
    if "tool-calling" in q or "tool calling" in desc or "function calling" in desc: bs.add("tool-calling")
    if "agent-framework" in q or "agent framework" in desc: bs.add("agent-frameworks")
    if "agentic-ai" in q or "agentic" in q or "ai-agent" in q or "agentic" in desc: bs.add("agentic-ai")
    if "autonomous-agent" in q or "autonomous agent" in q or "autonomous" in desc: bs.add("autonomous")
    if "llm-agent" in q or ("llm" in q and "agent" in q): bs.add("llm-agents")
    if lang == "rust":       bs.add("lang-rust")
    if lang == "go":         bs.add("lang-go")
    if lang == "typescript": bs.add("lang-typescript")
    if lang == "python":     bs.add("lang-python")
    if lang == "javascript": bs.add("lang-javascript")
    if (r.get("stars") or 0) >= 50: bs.add("trending")
    bs.add("all")
    if not any(b in bs for b in ["mcp-servers","voice-agents","coding-agents","langgraph",
                                 "autogen","crewai","tool-calling","agent-frameworks",
                                 "agentic-ai","autonomous","llm-agents"]):
        bs.add("llm-agents")
    return bs

by_cat = defaultdict(list)
for r in repos:
    for b in bucket(r):
        by_cat[b].append(r)

def sk(r): return (-(r.get("stars") or 0), r.get("pushed_at") or "")
for k in by_cat: by_cat[k].sort(key=sk)

def esc(s, n=160):
    if not s: return ""
    s = re.sub(r"\s+"," ",str(s)).strip().replace("|","\\|")
    return s if len(s)<=n else s[:n-1].rstrip()+"…"

def lang_badge(lang):
    if not lang: return ""
    colors={"python":"3572A5","typescript":"3178C6","javascript":"F7DF1E","go":"00ADD8",
            "rust":"DEA584","java":"B07219","c++":"f34b7d","c":"555555","ruby":"701516",
            "shell":"89e051","html":"E34F26","kotlin":"A97BFF","swift":"F05138","c#":"178600",
            "jupyter notebook":"DA5B0B"}
    c = colors.get(lang.lower(), "888888")
    safe = lang.replace(" ","%20").replace("#","%23").replace("+","%2B")
    return f"![{lang}](https://img.shields.io/badge/{safe}-{c}?style=flat)"

def star_badge(s):
    s = s or 0
    txt = f"{s/1000:.1f}k".replace(".0k","k") if s>=1000 else str(s)
    color = "blueviolet" if s>=1000 else "blue" if s>=100 else "lightgrey"
    return f"![Stars](https://img.shields.io/badge/%E2%AD%90-{txt}-{color})"

def gh_badge(url): return f"[![GitHub](https://img.shields.io/badge/Code-GitHub-black?logo=github)]({url})"

def row(r):
    return (f"| **[{r['owner_repo']}]({r['url']})** | {esc(r.get('description'))} "
            f"| {lang_badge(r.get('language') or '')} | {star_badge(r.get('stars'))} "
            f"| {gh_badge(r['url'])} |")

HEADER = ("| Repository | Description | Language | Stars | Code |\n"
          "| ---------- | ----------- | -------- | ----- | ---- |")

TODAY = datetime.utcnow().strftime("%Y-%m-%d")
cat_stats={}
for slug,items in by_cat.items():
    title,blurb,emoji = CATEGORIES[slug]
    lines=[f"# {emoji} {title}","",
           "[← Back to main index](../README.md)","",
           f"> {blurb}","",
           f"**{len(items):,} repositories** · sorted by stars then recent activity · generated {TODAY}","",
           HEADER]
    lines.extend(row(r) for r in items)
    lines.append("")
    (CAT_DIR/f"{slug}.md").write_text("\n".join(lines))
    cat_stats[slug]=len(items)

total=len(repos)
lang_counts=Counter((r.get("language") or "Unknown") for r in repos)
top_langs=lang_counts.most_common(10)
top_starred=sorted(repos,key=sk)[:30]
licensed=sum(1 for r in repos if r.get("license") and r["license"]!="NOASSERTION")
y2026=sum(1 for r in repos if (r.get("pushed_at") or "").startswith("2026"))

R=[]
P=R.append
P("# 🤖 5000+ AI Agent Projects")
P("")
P(f"[![5000-AI-Agents-Projects](https://img.shields.io/badge/5000%2B--AI--Agents--Projects-UseCase-2ea44f?logo=github)](#)  "
  f"[![Repos](https://img.shields.io/badge/repos-{total:,}-blue)](#)  "
  f"[![Updated](https://img.shields.io/badge/updated-{TODAY}-informational)](#)  "
  f"[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)")
P("")
P("A curated, machine-indexed collection of **5,080 unique open-source AI-agent projects** — "
  "spanning MCP servers, voice agents, coding agents, LangGraph, AutoGen, CrewAI, tool-calling "
  "frameworks and more. Inspired by "
  "[ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects), "
  "scaled to 10× the size. 🚀")
P(""); P("---"); P("")
P("## 📋 Table of Contents"); P("")
for s in ["Introduction","Dataset at a Glance","Categories","By Programming Language",
          "Top 30 Trending Repos","How the List Was Built","Contributing","License"]:
    P(f"- [{s}](#-{s.lower().replace(' ','-')})")
P(""); P("---"); P("")
P("## 🧠 Introduction"); P("")
P("AI agents are the fastest-moving frontier in applied AI: LLMs paired with tools, memory, "
  "planning loops and multi-agent orchestration. This index is a one-stop map of what's "
  "actually being built right now in public on GitHub.")
P("")
P("Each repository is tagged into one or more categories so you can drill down by use case "
  "(MCP servers, voice, coding), by framework (LangGraph, AutoGen, CrewAI) or by language. "
  "Every row links straight to the source repo.")
P(""); P("---"); P("")
P("## 📊 Dataset at a Glance"); P("")
P(f"- **Total repositories:** `{total:,}`")
P(f"- **With an OSI license:** `{licensed:,}` ({licensed*100//total}%)")
P(f"- **Pushed in 2026:** `{y2026:,}` ({y2026*100//total}%)")
P(f"- **Unique primary languages:** `{len([l for l in lang_counts if l!='Unknown'])}`")
P("")
P("**Top 10 languages**"); P("")
P("| Language | Repos | Share |")
P("| -------- | ----- | ----- |")
for lang,n in top_langs:
    P(f"| {lang_badge(lang) if lang!='Unknown' else 'Unknown'} | {n:,} | {n*100/total:.1f}% |")
P(""); P("---"); P("")
P("## 🗂️ Categories"); P("")
P("Click any category to open its full table.")
P("")
P("| Category | Description | Repos |")
P("| -------- | ----------- | ----- |")
cat_order=["mcp-servers","voice-agents","coding-agents","langgraph","autogen","crewai",
           "tool-calling","agent-frameworks","agentic-ai","autonomous","llm-agents","trending","all"]
for slug in cat_order:
    if slug in cat_stats:
        t,b,e=CATEGORIES[slug]
        P(f"| {e} **[{t}](categories/{slug}.md)** | {b} | `{cat_stats[slug]:,}` |")
P(""); P("---"); P("")
P("## 🧬 By Programming Language"); P("")
P("| Language | Repos | Table |")
P("| -------- | ----- | ----- |")
for slug in ["lang-python","lang-typescript","lang-go","lang-rust","lang-javascript"]:
    t,b,e=CATEGORIES[slug]
    P(f"| {lang_badge(t.replace(' Agents',''))} | `{cat_stats[slug]:,}` | [{t}](categories/{slug}.md) |")
P(""); P("---"); P("")
P("## 🔥 Top 30 Trending Repos"); P("")
P("Ranked by star count across the entire dataset.")
P("")
P(HEADER)
for r in top_starred: P(row(r))
P(""); P("---"); P("")
P("## 🛠️ How the List Was Built"); P("")
P("- Queried the GitHub Search API across **54 distinct topic / keyword filters** "
  "(`topic:ai-agent`, `topic:mcp-server`, `topic:langgraph`, language-scoped queries, etc.).")
P("- Filtered to repos pushed since **2026-01-01** with at least minimal activity.")
P("- De-duplicated by `owner/repo` to produce **5,080 unique entries**.")
P("- Each entry is bucketed into one or more of the categories above using a rule-based "
  "classifier over `source_query`, `description` and `language`.")
P("- Rendered as Markdown tables, one file per category, linked from this README.")
P("")
P("Source data: `repos_5080_all_unique.json` (included as the upstream dataset).")
P(""); P("---"); P("")
P("## 🤝 Contributing"); P("")
P("PRs welcome! To add or correct a repo:")
P("")
P("1. Fork the repo.")
P("2. Edit the matching file in `categories/`.")
P("3. Open a pull request — keep the table format intact.")
P("")
P("See [CONTRIBUTING.md](CONTRIBUTING.md) for details.")
P("")
P("## 📜 License"); P("")
P("This index is released under the [MIT License](LICENSE). "
  "Each linked repository retains its own license.")
P(""); P("---"); P("")
P("⭐ **Star this repo** if it helped you find your next agent project.")
P("")
(ROOT/"README.md").write_text("\n".join(R))

print("README ok ->", ROOT/"README.md")
for slug in cat_order+["lang-python","lang-typescript","lang-go","lang-rust","lang-javascript"]:
    if slug in cat_stats:
        print(f"  {slug:20s} -> {cat_stats[slug]:>5,}")
