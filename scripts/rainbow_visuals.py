"""Small shared rainbow accents; neutral surfaces keep the content readable."""
SPECTRUM = ['#e68195', '#e6ad67', '#c7bc63', '#60bba5', '#69a7d0', '#9b8ac7']


def spectral_defs(prefix='spectrum'):
    stops = ''.join(f'<stop offset="{i*20}%" stop-color="{color}"/>' for i, color in enumerate(SPECTRUM))
    return f'<defs><linearGradient id="{prefix}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient></defs>'


def spectrum_rule(x, y, width, prefix='spectrum', opacity=1, height=3):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{height/2}" fill="url(#{prefix})" opacity="{opacity}"/>'
