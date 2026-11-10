#!/usr/bin/env python3
"""
Apple-Style Strong Password Generator
-------------------------------------
Recreates Apple's strong password pattern with configurable length.

Default (3 blocks):
    xxxxxx-xxxxxx-xxxxxx          (18 characters)

You can set any number of blocks (including extremely large values):
    --blocks 1
    --blocks 100
    --blocks 1000000000000     # 1 trillion blocks (will take a very long time)

Rules (same as Apple):
  • CVC syllables (Consonant-Vowel-Consonant)
  • Only non-ambiguous characters
  • Exactly one uppercase letter
  • Exactly one digit on a block boundary
  • Blocklist filter (skipped for very large passwords)
  • Cryptographically secure randomness

Usage:
  python3 passgen.py
  python3 passgen.py --blocks 5
  python3 passgen.py -n 100 --blocks 4 -o long_passwords.txt
"""

import argparse
import secrets
import sys
from pathlib import Path

# Safe character pools (no visual ambiguity)
CONSONANTS = "bcdfghjkmnpqrstvwxz"
VOWELS     = "aeiouy"
DIGITS     = "23456789"

# Minimal blocklist (only used when the password is reasonably small)
BLOCKLIST = {
    "anal", "anus", "arse", "ass", "bastard", "bitch", "bollock", "cock",
    "crap", "cunt", "damn", "dick", "dyke", "fag", "fuck", "hell", "homo",
    "jizz", "lesbian", "nazi", "nigga", "nigger", "piss", "porn", "pussy",
    "queer", "rape", "sex", "shit", "slut", "tit", "twat", "wank", "whore",
}


def cvc() -> str:
    """Return one random CVC syllable."""
    return (
        secrets.choice(CONSONANTS)
        + secrets.choice(VOWELS)
        + secrets.choice(CONSONANTS)
    )


def generate_one(num_blocks: int = 3) -> str:
    """
    Generate one Apple-style password.
    For very large num_blocks this still builds the full string in memory.
    Prefer generate_and_write() for huge sizes.
    """
    total_chars = num_blocks * 6
    syllables_needed = num_blocks * 2

    # Pre-decide the special positions so we can apply them while building
    digit_block = secrets.randbelow(num_blocks)
    digit_at_end = secrets.choice([True, False])          # start or end of block
    digit_pos = digit_block * 6 + (5 if digit_at_end else 0)

    upper_pos = secrets.randbelow(total_chars)
    while upper_pos == digit_pos:
        upper_pos = secrets.randbelow(total_chars)

    digit_char = secrets.choice(DIGITS)

    # Build all characters
    chars = []
    for i in range(syllables_needed):
        chars.extend(cvc())

    # Apply mutations
    chars[digit_pos] = digit_char
    chars[upper_pos] = chars[upper_pos].upper()

    # Blocklist only for reasonably sized passwords
    if num_blocks <= 50:
        raw = "".join(chars).lower()
        if any(bad in raw for bad in BLOCKLIST):
            return generate_one(num_blocks)          # rare retry

    # Format with hyphens
    parts = ["".join(chars[i:i+6]) for i in range(0, total_chars, 6)]
    return "-".join(parts)


def generate_and_write(num_blocks: int, file_handle) -> None:
    """
    Stream a single huge password directly to a file / stdout
    without ever holding the whole thing in memory.
    """
    total_chars = num_blocks * 6

    # Decide special positions first
    digit_block = secrets.randbelow(num_blocks)
    digit_at_end = secrets.choice([True, False])
    digit_pos = digit_block * 6 + (5 if digit_at_end else 0)

    upper_pos = secrets.randbelow(total_chars)
    while upper_pos == digit_pos:
        upper_pos = secrets.randbelow(total_chars)

    digit_char = secrets.choice(DIGITS)

    # Stream block by block
    char_index = 0
    for block in range(num_blocks):
        if block > 0:
            file_handle.write("-")

        # Each block = two CVC syllables = 6 characters
        for _ in range(2):
            for c in cvc():
                if char_index == digit_pos:
                    file_handle.write(digit_char)
                elif char_index == upper_pos:
                    file_handle.write(c.upper())
                else:
                    file_handle.write(c)
                char_index += 1

    file_handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Apple-style strong passwords (any length)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s --blocks 1
  %(prog)s --blocks 5
  %(prog)s --blocks 1000000 -o huge.txt
  %(prog)s -n 100 --blocks 4
        """
    )
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=1,
        help="How many passwords to generate (default: 1)"
    )
    parser.add_argument(
        "-b", "--blocks",
        type=int,
        default=3,
        help="Number of 6-character blocks (default: 3). "
             "Can be extremely large (e.g. 1000000000000)."
    )
    parser.add_argument(
        "-o", "--output",
        help="Write passwords to a file instead of stdout"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode"
    )

    args = parser.parse_args()

    if args.number < 1:
        print("Error: -n must be at least 1", file=sys.stderr)
        sys.exit(1)
    if args.blocks < 1:
        print("Error: --blocks must be at least 1", file=sys.stderr)
        sys.exit(1)

    # Warning for huge sizes
    if args.blocks > 100_000 and not args.quiet:
        chars = args.blocks * 6
        print(f"[!] Warning: {args.blocks:,} blocks = ~{chars:,} characters "
              f"per password. This will take a long time.", file=sys.stderr)

    use_streaming = args.blocks > 10_000   # stream when it starts getting big

    if args.output:
        path = Path(args.output)
        with path.open("w", encoding="utf-8") as f:
            for i in range(args.number):
                if use_streaming:
                    generate_and_write(args.blocks, f)
                else:
                    f.write(generate_one(args.blocks) + "\n")

                if not args.quiet and args.number >= 1000 and (i + 1) % 1000 == 0:
                    print(f"[+] {i+1:,} / {args.number:,}", file=sys.stderr)

        if not args.quiet:
            print(f"[+] Generated {args.number:,} password(s) → {path}", file=sys.stderr)
    else:
        # Writing to stdout
        for i in range(args.number):
            if use_streaming:
                generate_and_write(args.blocks, sys.stdout)
            else:
                print(generate_one(args.blocks))

        if not args.quiet and args.number > 1:
            print(f"\n[+] Generated {args.number:,} passwords", file=sys.stderr)


if __name__ == "__main__":
    main()
