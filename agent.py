#!/usr/bin/env python3
"""
Gemma 4 Agent — local AI agent with tools.
Gives Gemma 4 access to: bash, read_file, write_file, web_search, list_dir.
Usage: python3 agent.py "your task here"
       python3 agent.py   (interactive mode)
"""
import os, sys, json, subprocess, re, requests
from pathlib import Path
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL      = "gemma4"
MAX_TURNS  = 20   # max tool call rounds before giving up

# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command on the server and get its output. Use for system tasks, running scripts, checking processes, git operations, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to run"},
                    "timeout": {"type": "integer", "description": "Timeout in seconds (default 30)", "default": 30}
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file. Returns the file content as text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative file path to read"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write or overwrite a file with given content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Absolute or relative file path to write"},
                    "content": {"type": "string", "description": "Content to write to the file"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files and directories at a given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list (default: current directory)", "default": "."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web using DuckDuckGo and return top results with titles and snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Max results to return (default 5)", "default": 5}
                },
                "required": ["query"]
            }
        }
    }
]

# ── Tool executors ────────────────────────────────────────────────────────────

def run_bash(command, timeout=30):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            timeout=int(timeout), env={**os.environ, "DISPLAY": ":0"}
        )
        out = result.stdout.strip()
        err = result.stderr.strip()
        if result.returncode != 0:
            return f"Exit code {result.returncode}\n{out}\n{err}".strip()
        return out or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout}s"
    except Exception as e:
        return f"Error: {e}"

def run_read_file(path):
    try:
        p = Path(path).expanduser()
        if not p.exists():
            return f"File not found: {path}"
        if p.stat().st_size > 500_000:
            return f"File too large ({p.stat().st_size} bytes) — use bash to read specific lines"
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Error reading {path}: {e}"

def run_write_file(path, content):
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"✓ Written {len(content)} chars to {path}"
    except Exception as e:
        return f"Error writing {path}: {e}"

def run_list_dir(path="."):
    try:
        p = Path(path).expanduser()
        if not p.exists():
            return f"Path not found: {path}"
        entries = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name))
        lines = []
        for e in entries[:100]:
            kind = "DIR " if e.is_dir() else "FILE"
            size = f"{e.stat().st_size:>10,}" if e.is_file() else ""
            lines.append(f"{kind}  {size}  {e.name}")
        if len(list(p.iterdir())) > 100:
            lines.append("... (truncated at 100 entries)")
        return "\n".join(lines) or "(empty directory)"
    except Exception as e:
        return f"Error listing {path}: {e}"

def run_web_search(query, max_results=5):
    try:
        # DuckDuckGo instant answer API
        params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
        r = requests.get("https://api.duckduckgo.com/", params=params, timeout=10)
        data = r.json()

        results = []
        # Abstract (direct answer)
        if data.get("AbstractText"):
            results.append(f"[Answer] {data['AbstractText']}")
        # Related topics
        for topic in data.get("RelatedTopics", [])[:int(max_results)]:
            if isinstance(topic, dict) and topic.get("Text"):
                url = topic.get("FirstURL", "")
                results.append(f"• {topic['Text']}\n  {url}")

        if not results:
            return f"No results found for: {query}"
        return "\n\n".join(results)
    except Exception as e:
        return f"Search error: {e}"

EXECUTORS = {
    "bash":       lambda args: run_bash(args["command"], args.get("timeout", 30)),
    "read_file":  lambda args: run_read_file(args["path"]),
    "write_file": lambda args: run_write_file(args["path"], args["content"]),
    "list_dir":   lambda args: run_list_dir(args.get("path", ".")),
    "web_search": lambda args: run_web_search(args["query"], args.get("max_results", 5)),
}

# ── Agent loop ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = f"""You are a helpful AI assistant running on a local Ubuntu server.
Today is {datetime.now().strftime('%Y-%m-%d')}.
You have access to tools: bash, read_file, write_file, list_dir, web_search.
Use tools whenever needed to complete tasks accurately.
When running bash commands, you have full access to the server.
Be concise and focused. Complete the task, then give a clear final answer."""

def chat(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "stream": False,
        "options": {"temperature": 0.3}
    }
    r = requests.post(OLLAMA_URL, json=payload, timeout=300)
    r.raise_for_status()
    return r.json()["message"]

def run_agent(task, verbose=True):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": task}
    ]

    for turn in range(MAX_TURNS):
        if verbose:
            print(f"\n{'─'*50}")

        msg = chat(messages)
        messages.append(msg)

        # No tool calls — final answer
        if not msg.get("tool_calls"):
            answer = msg.get("content", "").strip()
            if verbose:
                print(f"\n🤖 Gemma 4: {answer}")
            return answer

        # Execute each tool call
        for call in msg["tool_calls"]:
            fn_name = call["function"]["name"]
            fn_args = call["function"]["arguments"]
            if isinstance(fn_args, str):
                fn_args = json.loads(fn_args)

            if verbose:
                print(f"\n🔧 Tool: {fn_name}({json.dumps(fn_args, ensure_ascii=False)[:120]})")

            executor = EXECUTORS.get(fn_name)
            if executor:
                result = executor(fn_args)
            else:
                result = f"Unknown tool: {fn_name}"

            if verbose:
                preview = str(result)[:300]
                print(f"   → {preview}{'...' if len(str(result)) > 300 else ''}")

            messages.append({
                "role": "tool",
                "content": str(result),
                "name": fn_name
            })

    return "Max turns reached — task may be incomplete."

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        run_agent(task)
    else:
        print("🤖 Gemma 4 Agent (type 'exit' to quit)\n")
        while True:
            try:
                task = input("You: ").strip()
                if task.lower() in ("exit", "quit", "q"):
                    break
                if not task:
                    continue
                run_agent(task)
            except KeyboardInterrupt:
                print("\nBye!")
                break
