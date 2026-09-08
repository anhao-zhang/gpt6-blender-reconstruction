#!/usr/bin/env python3

import argparse
import json
import re
from pathlib import Path


SECRET_PATTERNS = [
    (re.compile(r'sk-[A-Za-z0-9_-]{16,}'), '[REDACTED_OPENAI_KEY]'),
    (re.compile(r'ghp_[A-Za-z0-9]{20,}'), '[REDACTED_GITHUB_TOKEN]'),
    (re.compile(r'github_pat_[A-Za-z0-9_]{20,}'), '[REDACTED_GITHUB_TOKEN]'),
    (
        re.compile(r'Bearer\s+[A-Za-z0-9._~+/=-]{20,}', re.I),
        'Bearer [REDACTED]',
    ),
]

BASE64_RE = re.compile(
    r'data:image/[^;]+;base64,[A-Za-z0-9+/=\s]{500,}',
    re.I,
)

LONG_BASE64_RE = re.compile(
    r'(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{1000,}={0,2}'
)


def sanitize_text(text: str, max_len: int = 12000) -> str:
    text = BASE64_RE.sub('[IMAGE_BASE64_OMITTED]', text)
    text = LONG_BASE64_RE.sub('[LARGE_BASE64_OMITTED]', text)

    for pattern, replacement in SECRET_PATTERNS:
        text = pattern.sub(replacement, text)

    if len(text) > max_len:
        text = text[:max_len] + '\n[OUTPUT_TRUNCATED]'

    return text


def extract_message_text(content):
    parts = []

    if not isinstance(content, list):
        return ''

    for item in content:
        if not isinstance(item, dict):
            continue

        if item.get('type') in {
            'input_text',
            'output_text',
            'text',
        }:
            text = item.get('text')
            if text:
                parts.append(text)

    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    dst.parent.mkdir(parents=True, exist_ok=True)

    kept = 0

    with src.open('r', encoding='utf-8', errors='replace') as fin, \
         dst.open('w', encoding='utf-8') as fout:

        for raw in fin:
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue

            timestamp = record.get('timestamp')
            record_type = record.get('type')
            payload = record.get('payload') or {}

            # Keep actual Codex response items.
            if record_type != 'response_item':
                continue

            payload_type = payload.get('type')

            # User / assistant conversational messages.
            if payload_type == 'message':
                role = payload.get('role')

                # Drop developer/system infrastructure messages.
                if role not in {'user', 'assistant'}:
                    continue

                text = extract_message_text(payload.get('content'))

                if not text.strip():
                    continue

                out = {
                    'timestamp': timestamp,
                    'kind': 'message',
                    'role': role,
                    'text': sanitize_text(text),
                }

            # Codex tool invocation.
            elif payload_type == 'custom_tool_call':
                out = {
                    'timestamp': timestamp,
                    'kind': 'tool_call',
                    'tool': payload.get('name'),
                    'call_id': payload.get('call_id'),
                    'input': sanitize_text(str(payload.get('input', ''))),
                }

            # Tool result.
            elif payload_type == 'custom_tool_call_output':
                output = payload.get('output')

                if isinstance(output, str):
                    output_text = output
                else:
                    output_text = json.dumps(
                        output,
                        ensure_ascii=False,
                    )

                out = {
                    'timestamp': timestamp,
                    'kind': 'tool_result',
                    'call_id': payload.get('call_id'),
                    'output': sanitize_text(output_text),
                }

            else:
                continue

            fout.write(json.dumps(out, ensure_ascii=False) + '\n')
            kept += 1

    print(f'Input : {src}')
    print(f'Output: {dst}')
    print(f'Kept records: {kept}')


if __name__ == '__main__':
    main()
