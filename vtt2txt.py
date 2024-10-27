"""
Code adapted from: https://gist.github.com/glasslion/b2fcad16bc8a9630dbd7a945ab5ebf5e
Modified for better integration and importing
"""

import re

def remove_tags(text):
    """Remove vtt markup tags"""
    tags = [
        r'</c>',
        r'<c(\.color\w+)?>',
        r'<\d{2}:\d{2}:\d{2}\.\d{3}>',
    ]

    for pat in tags:
        text = re.sub(pat, '', text)

    # Extract timestamp, only keep HH:MM
    text = re.sub(
        r'(\d{2}:\d{2}):\d{2}\.\d{3} --> .* align:start position:0%',
        r'\g<1>',
        text
    )

    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)
    return text

def remove_header(lines):
    """Remove vtt file header"""
    pos = -1
    for mark in ('##', 'Language: en',):
        if mark in lines:
            pos = lines.index(mark)
    lines = lines[pos+1:]
    return lines

def merge_duplicates(lines):
    """Remove duplicated subtitles. Duplicates are always adjacent."""
    last_timestamp = ''
    last_cap = ''
    for line in lines:
        if line == "":
            continue
        if re.match('^\d{2}:\d{2}$', line):
            if line != last_timestamp:
                yield line
                last_timestamp = line
        else:
            if line != last_cap:
                yield line
                last_cap = line

def merge_short_lines(lines):
    """Merge short lines into longer ones for better readability"""
    buffer = ''
    for line in lines:
        if line == "" or re.match('^\d{2}:\d{2}$', line):
            if buffer:
                yield buffer.strip()
                buffer = ''
            continue

        if len(line+buffer) < 80:
            buffer += ' ' + line
        else:
            if buffer:
                yield buffer.strip()
            buffer = line
    if buffer:
        yield buffer.strip()

def convert_vtt_to_text(vtt_file):
    """Convert a VTT file to clean plaintext"""
    try:
        with open(vtt_file, encoding='utf-8') as f:
            text = f.read()
            
        text = remove_tags(text)
        lines = text.splitlines()
        lines = remove_header(lines)
        lines = merge_duplicates(lines)
        lines = list(lines)
        lines = merge_short_lines(lines)
        
        return ' '.join(lines)
    except Exception as e:
        print(f"Error converting VTT to text: {str(e)}")
        return ""
