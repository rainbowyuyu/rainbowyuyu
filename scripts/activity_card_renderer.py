#!/usr/bin/env python3
"""Readable public activity cards with replayable, self-contained SVG snapshots.

The embedded metadata is public aggregate data, not a new API response. Legacy
cards are migrated only from their explicit labels/tooltips; the old activity
curve retains its normalized coordinates because it did not save exact counts.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from rainbow_visuals import spectral_defs, spectrum_rule
from studio_art import illustration

NS = {'svg': 'http://www.w3.org/2000/svg'}
SCHEMA = 'rainbow.activity-card/v1'
FILES = {
    'base.svg': 'base', 'languages.indepth.svg': 'languages',
    'streak.svg': 'streak', 'calendar.full.svg': 'calendar',
    'habits.charts.svg': 'habits', 'activity.svg': 'activity',
    'wakatime.svg': 'wakatime',
}
TITLES = {
    'base': 'GitHub 概览 / Public profile',
    'languages': '语言分布 / Languages',
    'streak': '持续构建 / Contribution streak',
    'calendar': '贡献日历 / Contribution calendar',
    'habits': '活跃时段 / Activity rhythm',
    'activity': '公开活动 / Public activity',
    'wakatime': '编码时间 / Coding time',
}
PALETTES = {
    'light': {
        'surface': '#faf7ef', 'panel': '#f0ece2', 'ink': '#203744',
        'muted': '#465967', 'quiet': '#526775', 'accent': '#137962',
        'track': '#dfdfd4', 'blue': '#286da5', 'purple': '#72559d',
        'gold': '#8a641d', 'pink': '#a14772', 'area': '#d4e6e1',
        'heat': ['#d9e2e6', '#b0d4c7', '#74b298', '#3d9274', '#16664e'],
    },
    'dark': {
        'surface': '#1b2228', 'panel': '#273139', 'ink': '#eef2f4',
        'muted': '#b8c4ce', 'quiet': '#9eafbd', 'accent': '#7dddc1',
        'track': '#34444f', 'blue': '#88bce6', 'purple': '#b9a2dc',
        'gold': '#d9bb7c', 'pink': '#dc9cbb', 'area': '#263e3c',
        'heat': ['#33434d', '#315f53', '#40836b', '#55b38d', '#83e2bb'],
    },
}


def esc(value):
    return html.escape(str(value), quote=True)


def text(x, y, value, size=16, color='ink', weight=400, anchor='start'):
    return (f'<text x="{x}" y="{y}" class="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{esc(value)}</text>')


def rect(x, y, width, height, color, radius=0, title=None):
    tip = f'<title>{esc(title)}</title>' if title is not None else ''
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" '
            f'rx="{radius}" fill="{color}">{tip}</rect>')


def snapshot(kind, updated_at, data, description, provenance='api'):
    return {'schema': SCHEMA, 'kind': kind, 'updated_at': updated_at,
            'description': description, 'provenance': provenance, 'data': data}


def _timestamp(root):
    desc = root.findtext('svg:desc', '', NS)
    match = re.search(r'Updated (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)', desc)
    if not match:
        raise ValueError('Saved card has no explicit snapshot timestamp')
    return match.group(1), desc


def _calendar_days(root):
    days = []
    for item in root.findall('.//svg:rect/svg:title', NS):
        match = re.fullmatch(r'(\d{4}-\d\d-\d\d): (\d+) contributions', item.text or '')
        if match:
            days.append({'date': match.group(1), 'count': int(match.group(2))})
    return days


def snapshot_from_svg(raw: str, filename: str, folder: Path | None = None):
    """Read semantic metadata, or explicitly migrate the known original format."""
    root = ET.fromstring(raw)
    metadata = root.find('svg:metadata[@id="activity-snapshot"]', NS)
    if metadata is not None:
        saved = json.loads(metadata.text or '{}')
        if saved.get('schema') != SCHEMA or saved.get('kind') != FILES[filename]:
            raise ValueError('Unrecognized activity snapshot schema/kind')
        return saved
    updated, description = _timestamp(root)
    kind = FILES[filename]
    labels = [element.text or '' for element in root.findall('svg:text', NS)]
    integers = [int(value.replace(',', '')) for value in labels if re.fullmatch(r'[\d,]+', value)]
    if kind == 'base':
        if len(integers) != 4:
            raise ValueError('Expected four explicit profile totals')
        data = dict(zip(('repositories', 'stars', 'followers', 'forks'), integers))
    elif kind == 'languages':
        rows = []
        for i, label in enumerate(labels):
            if re.fullmatch(r'\d+\.\d%', label):
                rows.append({'name': labels[i - 1], 'percentage': float(label[:-1])})
        if len(rows) != 5:
            raise ValueError('Expected five saved language percentages')
        data = {'rows': rows, 'precision': 'saved display percentages, one decimal',
                'scope': 'public non-fork source bytes; top five only'}
    elif kind == 'calendar':
        days = _calendar_days(root)
        if len(days) < 300 or len(integers) != 1:
            raise ValueError('Incomplete explicit calendar snapshot')
        data = {'total': integers[0], 'days': days}
    elif kind == 'streak':
        if len(integers) != 2:
            raise ValueError('Expected two explicit streak totals')
        data = {'current': integers[0], 'longest': integers[1]}
        if folder is not None:
            other = snapshot_from_svg((folder / 'calendar.full.svg').read_text(encoding='utf-8'), 'calendar.full.svg')
            if other['updated_at'] == updated:
                data['recent_days'] = other['data']['days'][-14:]
    elif kind == 'habits':
        pairs = []
        for item in root.findall('.//svg:rect/svg:title', NS):
            match = re.fullmatch(r'(\d\d):00 UTC\+8: (\d+) public events', item.text or '')
            if match:
                pairs.append((int(match.group(1)), int(match.group(2))))
        if [hour for hour, _ in pairs] != list(range(24)):
            raise ValueError('Expected 24 explicit hourly buckets')
        sample = re.search(r'Last (\d+) public events', description)
        if not sample or int(sample.group(1)) != sum(count for _, count in pairs):
            raise ValueError('Hourly counts disagree with explicit event sample size')
        data = {'hours': [count for _, count in pairs], 'sample_size': int(sample.group(1)), 'timezone': 'UTC+8'}
    elif kind == 'activity':
        curve = root.find('svg:polyline', NS)
        dates = [label for label in labels if re.fullmatch(r'\d{4}-\d\d-\d\d', label)]
        if curve is None or len(dates) != 2:
            raise ValueError('Saved event curve or dates unavailable')
        points = curve.attrib['points']
        if len(points.split()) != 30:
            raise ValueError('Expected a saved 30-point curve')
        data = {'start': dates[0], 'end': dates[1], 'legacy_points': points,
                'legacy_baseline': 210, 'legacy_range': 110,
                'precision': 'normalized curve only; exact event counts were not stored'}
    elif kind == 'wakatime':
        hours = [float(value[:-2]) for value in labels if re.fullmatch(r'\d+\.\d h', value)]
        if len(hours) != 2:
            raise ValueError('Expected two explicitly recorded WakaTime values')
        data = {'hours': hours[0], 'daily_average_hours': hours[1],
                'precision': 'saved hours rounded to one decimal; not unconfigured'}
    else:
        raise ValueError('Unsupported activity card')
    return snapshot(kind, updated, data, description, 'saved SVG labels and tooltips; no API refresh')


def _footer(saved, width, height):
    date = saved['updated_at'][:16].replace('T', ' ') + ' UTC'
    return text(28, height - 21, 'rainbow鱼', 13, 'muted', 600) + text(width - 28, height - 21, date, 12, 'quiet', anchor='end')


def _base(data, p):
    body = text(28, 66, '公开数据 / Public profile totals', 15, 'muted')
    rows = [('repositories', '公开仓库', 'Repositories'), ('stars', '获得星标', 'Stars'),
            ('followers', '关注者', 'Followers'), ('forks', '公开分叉', 'Forks')]
    for i, (key, zh, en) in enumerate(rows):
        x = 28 + (i % 2) * 224
        y = 111 + (i // 2) * 118
        body += text(x, y, zh, 17, 'muted')
        body += text(x, y + 48, f"{data[key]:,}", 49, ['blue','accent','purple','gold'][i], 650)
        body += text(x, y + 73, en, 15, 'muted')
    return body


def _languages(data, p):
    body = text(28, 66, '公开非 Fork 仓库 / Public non-fork repos', 14, 'muted')
    colors = [p[name] for name in ('accent', 'blue', 'purple', 'gold', 'pink')]
    rows = data['rows']
    if not rows:
        return body + text(28, 180, '暂无公开语言数据 / No language data', 18, 'muted')
    for i, row in enumerate(rows):
        y = 102 + i * 41
        pct = row['percentage']
        body += text(28, y, row['name'], 16, 'ink', 500)
        body += text(452, y, f'{pct:.1f}%', 16, 'ink', 600, 'end')
        body += rect(28, y + 9, 424, 9, p['track'], 4)
        body += rect(28, y + 9, max(.4, 424 * pct / 100), 9, colors[i % len(colors)], 4,
                     f"{row['name']}: {pct:.1f}% of all public non-fork source bytes")
    body += text(28, 309, '源码字节占比 / Source bytes, not proficiency', 13, 'muted')
    return body


def _habits(data, p):
    body = text(28, 66, '公开事件样本 / Public event sample · UTC+8', 14, 'muted')
    total = data['sample_size']
    total_label = f'{total:,}'
    # Reserve the actual digit count, including grouped thousands, before labels.
    label_x = max(118, math.ceil(28 + 54 * sum(.62 if ch.isdigit() else .29 for ch in total_label) + 24))
    body += text(28, 132, total_label, 54, 'ink', 650)
    body += text(label_x, 110, '公开事件', 17, 'muted')
    if label_x > 210:
        body += text(label_x, 134, 'public events', 14, 'muted') + text(label_x, 156, 'up to 90 days', 14, 'muted')
    else:
        body += text(label_x, 134, 'public events · up to 90 days', 14, 'muted')
    values = data['hours']
    maximum = max(values) or 1
    for i, count in enumerate(values):
        x = 28 + i * (424 / 24)
        height = count / maximum * 98
        body += rect(x, 264 - height if count else 262, 12, height if count else 2,
                     p['accent'] if count else p['track'], 3,
                     f'{i:02}:00 UTC+8: {count} public events')
    for hour in (0, 6, 12, 18, 23):
        body += text(28 + hour * (424 / 24), 286, f'{hour:02}', 14, 'muted')
    body += text(28, 310, '事件频率，非编码时长 / Events, not coding hours', 13, 'muted')
    return body


def _wakatime(data, p):
    body = text(28, 66, 'WakaTime · 仅计入记录 / Recorded activity only', 14, 'muted')
    value = f"{data['hours']:.1f}"
    body += text(28, 165, value, 76, 'purple', 650)
    body += text(28 + len(value) * 43 + 7, 164, 'h', 26, 'muted', 500)
    body += text(28, 198, '最近 7 天 / Last 7 days', 19, 'ink', 500)
    body += rect(28, 222, 424, 69, p['panel'], 14)
    body += text(46, 267, f"{data['daily_average_hours']:.1f} h", 31, 'ink', 600)
    body += text(192, 253, '日均记录', 17, 'muted') + text(192, 276, 'Daily average', 15, 'muted')
    body += text(28, 311, '仅聚合时长 / Aggregate hours, no project names', 13, 'muted')
    return body


def _streak(data, p):
    body = text(28, 71, '基于 GitHub 贡献日历 / GitHub contribution days', 17, 'muted')
    for x, key, zh, en in ((28, 'current', '当前连续天数', 'Current streak'),
                          (238, 'longest', '年度最长记录', 'Longest in returned year')):
        body += text(x, 151, str(data[key]), 70, 'accent' if key == 'current' else 'purple', 650)
        body += text(x, 184, zh, 20, 'ink', 500) + text(x, 209, en, 15, 'muted')
    recent = data.get('recent_days', [])
    if recent:
        body += text(447, 111, '近两周 / Last 14 days', 16, 'muted')
        maximum = max(day['count'] for day in recent) or 1
        for i, day in enumerate(recent):
            level = 0 if not day['count'] else min(4, 1 + int(day['count'] / maximum * 3))
            body += rect(447 + i * 17, 131, 13, 25, p['heat'][level], 3,
                         f"{day['date']}: {day['count']} contributions")
        body += text(447, 184, recent[0]['date'][5:] + ' — ' + recent[-1]['date'][5:], 15, 'muted')
    body += text(28, 239, '允许今天尚未结束 / Current streak allows an unfinished today', 14, 'muted')
    return body


def _calendar(data, p):
    days = data['days']
    total_label = f"{data['total']:,}"
    label_x = max(178, math.ceil(28 + 54 * sum(.62 if ch.isdigit() else .29 for ch in total_label) + 24))
    body = text(28, 117, total_label, 54, 'accent', 650)
    body += text(label_x, 96, '过去一年贡献', 20, 'ink', 500) + text(label_x, 122, 'Contributions · rolling year', 17, 'muted')
    first = dt.date.fromisoformat(days[0]['date'])
    origin = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    maximum = max(day['count'] for day in days) or 1
    previous_month = None
    for day in days:
        date = dt.date.fromisoformat(day['date'])
        week, weekday = divmod((date - origin).days, 7)
        x = 28 + week * 12.4
        y = 170 + weekday * 14
        level = 0 if not day['count'] else min(4, 1 + int(day['count'] / maximum * 3))
        body += rect(x, y, 9.7, 10.5, p['heat'][level], 2,
                     f"{day['date']}: {day['count']} contributions")
        if date.day <= 7 and date.month != previous_month and date.month % 2 == 1:
            body += text(x, 157, date.strftime('%b'), 14, 'muted')
            previous_month = date.month
    body += text(28, 285, days[0]['date'] + ' — ' + days[-1]['date'], 14, 'muted')
    body += text(548, 285, '少 / Less', 12, 'muted')
    for i, color in enumerate(p['heat']):
        body += rect(610 + i * 14, 275, 10, 10, color, 2)
    return body


def _activity(data, p):
    body = text(28, 71, '30 日公开事件 / 30-day public event window', 17, 'muted')
    if 'counts' in data:
        values = data['counts']
        maximum = max(values) or 1
        fractions = [value / maximum for value in values]
    else:
        fractions = [(data['legacy_baseline'] - float(point.split(',')[1])) / data['legacy_range']
                     for point in data['legacy_points'].split()]
    coords = [(28 + i * 664 / (len(fractions) - 1), 225 - value * 114)
              for i, value in enumerate(fractions)]
    pts = ' '.join(f'{x:.2f},{y:.2f}' for x, y in coords)
    body += f'<polygon points="28,225 {pts} 692,225" fill="{p["area"]}"/>'
    body += (f'<polyline points="{pts}" fill="none" stroke="{p["accent"]}" '
             'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')
    if 'counts' in data:
        first = dt.date.fromisoformat(data['start'])
        for i, (x, y) in enumerate(coords):
            tip = f"{first + dt.timedelta(days=i)}: {data['counts'][i]} public events"
            body += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="{p["accent"]}"><title>{esc(tip)}</title></circle>'
    body += text(28, 252, data['start'], 15, 'muted') + text(692, 252, data['end'], 15, 'muted', anchor='end')
    body += text(28, 280, '公开事件相对走势，非全部提交 / Relative events, not all commits', 15, 'muted')
    return body


def render_card(saved, theme='dark'):
    if saved['schema'] != SCHEMA or theme not in PALETTES:
        raise ValueError('Unsupported activity renderer input')
    kind = saved['kind']
    data = saved['data']
    p = PALETTES[theme]
    width, height = (720, 310) if kind == 'streak' else (720, 350) if kind in ('calendar', 'activity') else (480, 400)
    # GitHub's inline README images can wrap without a vertical CSS gap.
    # Keep the card and content unchanged; reserve transparent space below it.
    canvas_height = height + 12 if width == 480 else height
    renderer = {'base': _base, 'languages': _languages, 'habits': _habits,
                'wakatime': _wakatime, 'streak': _streak, 'calendar': _calendar,
                'activity': _activity}[kind]
    title = TITLES[kind]
    zh, en = title.split(' / ', 1)
    en = {'base':'Public profile totals', 'languages':'Languages · public non-fork',
          'habits':'Activity rhythm · UTC+8', 'wakatime':'Coding time · WakaTime',
          'streak':'Contribution days'}.get(kind, en)
    motif = {'base':'robot', 'languages':'brushes', 'habits':'plane', 'wakatime':'hourglass',
             'streak':'plane', 'calendar':'robot', 'activity':'brushes'}[kind]
    content = renderer(data, p)
    if kind not in ('calendar',):
        # The title is split into two readable lines; its old subtitle is redundant.
        content = re.sub(r'^<text\b[^>]*>.*?</text>', '', content, count=1)
    offset = 20 if kind not in ('calendar', 'activity') else 10
    # Keep every datum and tooltip, moving the existing coordinates as a unit.
    content = re.sub(r'\by="(-?[\d.]+)"', lambda m:f'y="{float(m.group(1))+offset:g}"', content)
    content = re.sub(r'\bcy="(-?[\d.]+)"', lambda m:f'cy="{float(m.group(1))+offset:g}"', content)
    style = ("text{font-family:'Segoe UI','Microsoft YaHei',Arial,sans-serif;font-variant-numeric:tabular-nums}"
             + ''.join(f'.{name}' + '{fill:' + p[name] + '}' for name in ('ink', 'muted', 'quiet', 'accent','blue','purple','gold','pink')))
    metadata = json.dumps(saved, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    description = saved['description']
    if saved['updated_at'] not in description:
        description += '. Updated ' + saved['updated_at'] + '. Public aggregate data.'
    result = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{canvas_height}" '
              f'viewBox="0 0 {width} {canvas_height}" role="img" aria-label="{esc(title)}">'
              f'<title>{esc(title)}</title><desc>{esc(description)}</desc>'
              f'<metadata id="activity-snapshot">{esc(metadata)}</metadata><style>{style}</style>'
              + spectral_defs()
              + f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="22" fill="{p["surface"]}" stroke="{p["track"]}" stroke-opacity=".5"/>'
              + f'<path d="M25 83q110 -8 {width-150} 0" fill="none" stroke="{p["track"]}" stroke-width=".8" stroke-dasharray="2 5"/>'
              + illustration(motif+'.png', width-133, 7, 113, 94)
              + text(28, 42, zh, 26, 'ink', 650)
              + text(29, 65, en, 14, 'muted', 400)
              + content
              + (spectrum_rule(28, height-51, 45, opacity=.65, height=2) if width == 480 else '')
              + _footer(saved, width, height) + '</svg>\n')
    ET.fromstring(result)
    return result
