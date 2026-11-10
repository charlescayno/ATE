"""HTML formatting for the in-app log console (View Logs).

``format_data_row_html`` turns the one-line ``[DATA_ROW] k=v | k=v ...`` text into
grouped, colored lines. Only the on-screen console uses it; app_log.txt keeps the
raw single line.
"""
import html

KEY_COLOR = '#8a8f98'   # dim gray for field names
SEP_COLOR = '#555b66'

# (group title, color, bold values, matcher)
_GROUPS = (
    ("Input", '#40e0d0', False,
     lambda k: k.startswith(('VDC', 'Freq', 'Vin', 'Iin', 'Pin', 'PF', '%THD', 'Vin ('))),
    ("Port 1", '#98fb98', False,
     lambda k: k.startswith(('Ch1 Load', 'Vo1', 'Io1', 'Po1', '%V Reg 1'))),
    ("Port 2", '#ffaa00', False,
     lambda k: k.startswith(('Ch2 Load', 'Vo2', 'Io2', 'Po2', '%V Reg 2'))),
    ("Result", '#ffff00', True,
     lambda k: k.startswith(('Po_Total', 'Efficiency'))),
    ("Timing", '#9aa0aa', False,
     lambda k: k.startswith(('Sample', 'Elapsed', 'Time', 'Interval'))),
    ("Cursors", '#00bfff', False,
     lambda k: k.startswith('Cursor Result')),
    ("Rds", '#ff69b4', True,
     lambda k: k.startswith('Rds')),
    ("File", '#7a808a', False,
     lambda k: k.startswith('Waveform File')),
)
_SCOPE = ("Scope", '#da70d6', False)  # everything else


def _group_for(key):
    for title, color, bold, match in _GROUPS:
        if match(key):
            return title, color, bold
    return _SCOPE


def format_data_row_html(clean_text: str, now: str) -> str:
    """clean_text contains '[DATA_ROW] k=v | k=v'. Returns HTML (ends with <br>)."""
    payload = clean_text.split('[DATA_ROW]', 1)[1].strip()
    groups = {}
    order = []
    for part in payload.split(' | '):
        key, sep, val = part.partition('=')
        key, val = key.strip(), val.strip()
        if not key:
            continue
        title, color, bold = _group_for(key)
        if title not in groups:
            groups[title] = (color, bold, [])
            order.append(title)
        groups[title][2].append((key, val))

    sample = next((v for t in groups.values() for k, v in t[2] if k == 'Sample'), '')
    head = f'[{now}] [DATA_ROW]' + (f' Sample {html.escape(sample)}' if sample else '')
    out = [f'<span style="color:#98fb98; font-weight:bold;">{head}</span>']
    nb = '&nbsp;'
    canonical = ["Input", "Port 1", "Port 2", "Result", "Timing", "Scope", "Cursors", "Rds", "File"]
    order = [t for t in canonical if t in groups] + [t for t in order if t not in canonical]
    for title in order:
        color, bold, items = groups[title]
        weight = 'bold' if bold else 'normal'
        cells = []
        for key, val in items:
            cells.append(
                f'<span style="color:{KEY_COLOR};">{html.escape(key)}=</span>'
                f'<span style="color:{color}; font-weight:{weight};">{html.escape(val)}</span>')
        sep = f'<span style="color:{SEP_COLOR};"> | </span>'
        label = f'<span style="color:{color};">{title:<7}</span>'.replace(' ', nb)
        out.append(f'{nb * 4}{label}{sep.join(cells)}')
    return '<br>'.join(out) + '<br>'
