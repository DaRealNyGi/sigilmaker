#!/usr/bin/env python3
"""
Command-line interface for SigilMaker

Usage examples:
  sigilmaker-cli --mantra "I AM WEALTH" --patterns "Seed-of-Life,Golden Spiral" --out wealth.png
  sigilmaker-cli --input mantras.txt --format svg --batch
  sigilmaker-cli --list-patterns
"""
import sys
import os
import argparse
from sigilmaker.core import get_symbols, draw_sigil
from sigilmaker.shapes import SHAPES  # assuming shapes registry imported or defined


def list_patterns():
    for name in sorted(SHAPES.keys()):
        print(name)


def main():
    parser = argparse.ArgumentParser(description="SigilMaker CLI")
    parser.add_argument('--mantra', '-m', help='Mantra string to encode')
    parser.add_argument('--patterns', '-p', help='Comma-separated list of pattern names')
    parser.add_argument('--out', '-o', help='Output filename (png/svg)')
    parser.add_argument('--format', '-f', choices=['png','svg'], default='png', help='Output format')
    parser.add_argument('--input', '-i', help='Batch input file: one mantra per line')
    parser.add_argument('--list-patterns', action='store_true', help='List available pattern names')
    parser.add_argument('--radial', action='store_true', help='Enable radial text orientation')
    args = parser.parse_args()

    if args.list_patterns:
        list_patterns()
        sys.exit(0)

    patterns = []
    if args.patterns:
        patterns = [p.strip() for p in args.patterns.split(',') if p.strip()]
    else:
        # default to all patterns
        patterns = list(SHAPES.keys())

    def process(mantra):
        symbols = get_symbols(mantra)
        if len(symbols) < 3:
            print(f"Error: mantra '{mantra}' yields <3 symbols: {symbols}", file=sys.stderr)
            return
        out_file = args.out or f"{mantra.replace(' ','_')}.{args.format}"
        draw_sigil(
            symbols,
            patterns,
            radial=args.radial,
            out_path=out_file,
            fmt=args.format
        )
        print(f"Generated {out_file}")

    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: input file '{args.input}' not found", file=sys.stderr)
            sys.exit(1)
        with open(args.input) as f:
            for line in f:
                mantra_line = line.strip()
                if mantra_line:
                    process(mantra_line)
    else:
        if not args.mantra:
            parser.print_help()
            sys.exit(1)
        process(args.mantra)

if __name__ == '__main__':
    main()
