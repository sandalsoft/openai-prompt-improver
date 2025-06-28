#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai>=1.0.0",
#     "halo>=0.0.31",
# ]
# ///
"""
polish_prompt.py
Refines a raw software-development prompt using the
"Code-Prompt Polisher" system prompt.

USAGE EXAMPLES
--------------
  uv run prompt-enhance.py "Need help sorting a list faster in JS"
  uv run prompt-enhance.py --prompt "Need help sorting a list faster in JS"
  echo "Need help sorting a list faster in JS" | uv run prompt-enhance.py
  cat myprompt.txt | uv run prompt-enhance.py
"""
import os
import sys
import argparse
import openai
from halo import Halo

# ─────────────────── Configuration ─────────────────── #
MODEL   = "gpt-4o-mini"   # Any chat-capable model your key can access
TIMEOUT = 30              # Seconds
# ────────────────────────────────────────────────────── #

SYSTEM_PROMPT = r"""
You are *Code-Prompt Improver*. Your sole task is to transform a raw coding
prompt into a concise, unambiguous, best-practice prompt for a code-generation
LLM (e.g. Copilot, GPT-4o-mini).

─── 1 · Output format ──────────────────────────────────
Return **exactly three Markdown sections**:

1. ### Polished Prompt — the refined prompt, ready for a coding LLM  
2. ### Technical Details — 3-7 bullet points

─── 2 · Polishing checklist ────────────────────────────
* State language/runtime (e.g. "TypeScript 5.4 / Node 20").  
* Summarise the goal.  
* List constraints — style guides, versions, perf/security rules.  
* Define acceptance criteria — inputs/outputs, edge cases, tests.  
* Request brief reasoning where useful.  
* Use imperative voice & fenced code for snippets.  
* Remove fluff, apologies, chit-chat.

─── 3 · Tone & length ──────────────────────────────────
Optimized for an LLM.

─── 4 · Example (abridged) ─────────────────────────────
INPUT  
    Need help sorting a list faster in JS

OUTPUT  
    ### Polished Prompt  
    Write an **ES2023 / Node 20** function that sorts an array of up to  
    10 million 32-bit integers in-place…  
    ### Technical Details  
    • Use a funtional style
    • Separate the sorting logic from the main function
    • Use a test-driven approach
    • Log output to stdout

─── 5 · "Explain changes only" requests ────────────────
Still return the three sections; leave *Polished Prompt* empty and
populate *Rationale*.

""".strip()


def read_stdin() -> str:
    """Read a prompt from STDIN; exit if nothing was piped in."""
    data = sys.stdin.read().strip()
    if not data:
        sys.stderr.write("No input detected. Pipe or redirect a prompt into stdin.\n")
        sys.exit(1)
    return data


def get_prompt() -> str:
    """Get prompt from command line argument or stdin."""
    parser = argparse.ArgumentParser(
        description="Refine a raw software-development prompt using the Code-Prompt Polisher system.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
USAGE EXAMPLES:
  echo "Need help sorting a list faster in JS" | python polish_prompt.py
  cat myprompt.txt | python polish_prompt.py
  python polish_prompt.py "Need help sorting a list faster in JS"
  python polish_prompt.py --prompt "Need help sorting a list faster in JS"
        """.strip()
    )
    parser.add_argument(
        "prompt", 
        nargs="?", 
        help="The prompt to polish (if not provided, reads from stdin)"
    )
    parser.add_argument(
        "--prompt", 
        dest="prompt_flag",
        help="The prompt to polish (alternative to positional argument)"
    )
    
    args = parser.parse_args()
    
    # Priority: --prompt flag > positional argument > stdin
    if args.prompt_flag:
        return args.prompt_flag.strip()
    elif args.prompt:
        return args.prompt.strip()
    else:
        # Fall back to stdin if no arguments provided
        if sys.stdin.isatty():
            parser.error("No prompt provided. Either pass as argument or pipe to stdin.")
        return read_stdin()


def main() -> None:
    raw_prompt = get_prompt()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.stderr.write("Error: OPENAI_API_KEY environment variable not set.\n")
        sys.exit(1)

    openai.api_key = api_key

    spinner = Halo(text="Refining prompt...", spinner="dots")
    spinner.start()

    response = openai.chat.completions.create(
        model=MODEL,
        timeout=TIMEOUT,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": raw_prompt},
        ],
    )

    spinner.stop()

    print(response.choices[0].message.content.strip())


if __name__ == "__main__":
    main()
