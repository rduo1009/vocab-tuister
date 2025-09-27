# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "pywikibot",
#   "mwparserfromhell",
#   "tqdm",
# ]
# ///

"""
Fetch Latin adjectives from Wiktionary and extract which ones lack adverb forms.

This script scrapes the Wiktionary category `Category:Latin adjectives`
using Pywikibot, parses entries with mwparserfromhell, and writes out a Python
file containing a set of adjectives that do not have explicit adverbs listed.

Output
------
_latin_adjectives_no_adverb.py
    Temporary file that contains a single Python set named NO_ADVERB_ADJECTIVES,
    which can be copied elsewhere in the codebase.
"""

# ruff: noqa: T201, ANN001, ANN201, BLE001
# pyright: basic, reportMissingImports=false

import logging
from pathlib import Path

import mwparserfromhell
import pywikibot
from pywikibot import pagegenerators
from tqdm import tqdm

# Suppress pywikibot's verbose logging
logging.getLogger("pywiki").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def process_page(page, output):
    """Process a single page to extract adverb information."""
    try:
        # Page content is already preloaded, so page.text is fast
        text = page.text
    except Exception:
        return

    # Parse only once
    wikicode = mwparserfromhell.parse(text)

    # Look for 'adverb' in the la-adj headword template
    adverbs = []
    for template in wikicode.filter_templates():
        if template.name.matches("la-adj"):
            adverbs.extend(
                str(param.value).strip()
                for param in template.params
                if "adv" in param.name.lower()
            )
            break  # Only process first la-adj template

    # If not found, look for an explicit ==Adverb== section
    if not adverbs:
        sections = wikicode.get_sections(levels=[2])
        for section in sections:
            headings = section.filter_headings()
            if headings and headings[0].title.strip().lower() == "adverb":
                lines = section.strip_code().splitlines()
                if len(lines) > 1:
                    adverbs.append(lines[1].strip())
                break

    if adverbs:
        output.add(page.title())


def main() -> None:
    """Fetch the Latin adjectives."""
    print("Connecting to Wiktionary...", flush=True)
    site = pywikibot.Site("en", "wiktionary")

    print("Fetching Latin adjective pages...", flush=True)
    cat = pywikibot.Category(site, "Category:Latin adjectives")

    number_of_pages = cat.categoryinfo["pages"]
    print(f"Found {number_of_pages} pages.", flush=True)

    # Use PreloadingGenerator to batch fetch pages efficiently
    preloading_gen = pagegenerators.PreloadingGenerator(
        cat.articles(), groupsize=100, quiet=True
    )

    no_adverb = set()
    with tqdm(
        total=number_of_pages,
        desc="Processing Latin adjectives",
        unit="page",
        leave=True,
        dynamic_ncols=True,
    ) as pbar:
        for page in preloading_gen:
            try:
                process_page(page, no_adverb)
            except Exception as e:
                print(f"\nError processing {page.title()}: {e}")
            pbar.update(1)

    out_file = (
        Path(__file__).parent.parent
        / "core"
        / "accido"
        / "_latin_adjectives_no_adverb.py"
    )
    out_file.write_text(
        "# Auto-generated list of Latin adjectives without explicit adverbs\n\n"
        f"NO_ADVERB_ADJECTIVES = {no_adverb!r}\n"
    )

    print(f"Finished. Collected {len(no_adverb)} adjectives.", flush=True)


if __name__ == "__main__":
    main()
