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
MODEL = "gpt-4o"   # Any chat-capable model your key can access
TIMEOUT = 30              # Seconds
INSTRUCTIONS_FILE = "/Users/eric/Development/AI/PromptImprove/openai-prompt-improver/instructions.md"
# ────────────────────────────────────────────────────── #


def load_system_prompt() -> str:
    """Load the system prompt from instructions.md file."""
    try:
        with open(INSTRUCTIONS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            # Remove the markdown header if present
            if content.startswith("# Instructions\n"):
                content = content[len("# Instructions\n"):].strip()
            return content
    except FileNotFoundError:
        sys.stderr.write("Error: instructions.md file not found.\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"Error reading instructions.md: {e}\n")
        sys.exit(1)


def read_stdin() -> str:
    """Read a prompt from STDIN; exit if nothing was piped in."""
    data = sys.stdin.read().strip()
    if not data:
        sys.stderr.write(
            "No input detected. Pipe or redirect a prompt into stdin.\n")
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
  python polish_prompt.py -s "Need help sorting a list faster in JS" > output.txt
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
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="Silent mode - disable spinner for clean output that can be piped"
    )

    args = parser.parse_args()

    # Priority: --prompt flag > positional argument > stdin
    if args.prompt_flag:
        prompt = args.prompt_flag.strip()
    elif args.prompt:
        prompt = args.prompt.strip()
    else:
        # Fall back to stdin if no arguments provided
        if sys.stdin.isatty():
            parser.error(
                "No prompt provided. Either pass as argument or pipe to stdin.")
        prompt = read_stdin()

    return prompt, args.silent


def main() -> None:
    raw_prompt, silent_mode = get_prompt()
    system_prompt = load_system_prompt()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.stderr.write(
            "Error: OPENAI_API_KEY environment variable not set.\n")
        sys.exit(1)

    openai.api_key = api_key

    if not silent_mode:
        spinner = Halo(text="Refining prompt...", spinner="dots")
        spinner.start()

    response = openai.chat.completions.create(
        model=MODEL,
        timeout=TIMEOUT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": raw_prompt},
        ],
    )

    if not silent_mode:
        spinner.stop()

    print(response.choices[0].message.content.strip())


if __name__ == "__main__":
    main()
