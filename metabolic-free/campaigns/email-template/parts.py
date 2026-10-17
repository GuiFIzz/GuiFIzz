M = 'https://metabolicgfcxtremefit.com/media/email'

def head(mini_label, mini_href):
    """Dark bar: small logo left, same-action pill right."""
    return f'''<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#e9e9ec;margin:0;padding:0;"><tr><td align="center" style="padding:0;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#ffffff;">
<tr><td bgcolor="#0A0A0A" style="background:#0A0A0A;padding:14px 18px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td valign="middle" align="left"><img src="{M}/gfc-xtreme-logo-360.png" alt="GFC Xtreme Fitness" width="116" style="width:116px;height:auto;display:block;border:0;"></td>
<td valign="middle" align="right">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="#F26B2A" style="background:#F26B2A;border-radius:18px;">
<a href="{mini_href}" style="display:block;padding:9px 15px;font:800 12px/1 Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;white-space:nowrap;">{mini_label}</a>
</td></tr></table></td>
</tr></table>
</td></tr>'''

def title(h1, deck):
    return f'''<tr><td style="padding:26px 22px 0;font-family:Helvetica,Arial,sans-serif;">
<h1 style="margin:0 0 10px;font:800 30px/1.12 Helvetica,Arial,sans-serif;color:#0A0A0A;letter-spacing:-.025em;">{h1}</h1>
<p style="margin:0 0 20px;font:400 17px/1.45 Helvetica,Arial,sans-serif;color:#52525b;">{deck}</p>
</td></tr>'''

def hero(src, href, cap=""):
    c = f'<tr><td style="padding:8px 22px 0;"><p style="margin:0;font:400 12px/1.5 Helvetica,Arial,sans-serif;color:#71717a;">{cap}</p></td></tr>' if cap else ""
    return f'''<tr><td style="padding:0 22px;">
<a href="{href}" style="text-decoration:none;display:block;"><img src="{M}/{src}" alt="" width="556" style="width:100%;max-width:556px;height:auto;display:block;border:0;border-radius:10px;"></a>
</td></tr>{c}'''

def para(html, top=18):
    return f'''<tr><td style="padding:{top}px 22px 0;font-family:Helvetica,Arial,sans-serif;"><p style="margin:0;font:400 16px/1.62 Helvetica,Arial,sans-serif;color:#3f3f46;">{html}</p></td></tr>'''

def cta(label, href):
    return f'''<tr><td style="padding:24px 22px 4px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
<td bgcolor="#F26B2A" style="background:#F26B2A;border-radius:7px;">
<a href="{href}" style="display:block;padding:16px 26px;font:800 16px/1.2 Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;">{label}</a>
</td></tr></table>
</td></tr>'''

def callout(label, html):
    return f'''<tr><td style="padding:22px 22px 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFF7ED;border-left:4px solid #F26B2A;border-radius:0 7px 7px 0;"><tr><td style="padding:15px 17px;font-family:Helvetica,Arial,sans-serif;">
<p style="margin:0 0 6px;font:800 12px/1 Helvetica,Arial,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:#C2410C;">{label}</p>
<p style="margin:0;font:400 15px/1.55 Helvetica,Arial,sans-serif;color:#27272a;">{html}</p>
</td></tr></table></td></tr>'''

def sign(note=""):
    n = f'<p style="margin:12px 0 0;font:italic 400 12px/1.55 Helvetica,Arial,sans-serif;color:#8a8a92;">{note}</p>' if note else ""
    return f'''<tr><td style="padding:22px 22px 0;font-family:Helvetica,Arial,sans-serif;">
<p style="margin:0;font:400 16px/1.6 Helvetica,Arial,sans-serif;color:#3f3f46;"><strong style="color:#0A0A0A;">Coach Gui</strong></p>{n}</td></tr>'''

def labs():
    return f'''<tr><td style="padding:26px 22px 24px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0A0A0A;border-radius:12px;"><tr><td style="padding:24px 20px;font-family:Helvetica,Arial,sans-serif;">
<p style="margin:0 0 6px;font:800 11px/1 Helvetica,Arial,sans-serif;letter-spacing:.17em;text-transform:uppercase;color:#F26B2A;">GFC Labs</p>
<p style="margin:0 0 8px;font:800 24px/1.15 Helvetica,Arial,sans-serif;color:#ffffff;letter-spacing:-.02em;">Want results faster?</p>
<p style="margin:0 0 16px;font:400 16px/1.45 Helvetica,Arial,sans-serif;color:#a1a1aa;">Add the medical side.</p>
<p style="margin:0 0 16px;font:700 16px/1.45 Helvetica,Arial,sans-serif;color:#F26B2A;">GLP-1 medications &middot; Peptides &middot; Hormone therapy</p>
<p style="margin:0 0 18px;font:400 14px/1.6 Helvetica,Arial,sans-serif;color:#d4d4d8;">Reviewed online by licensed clinicians. No waiting room, no referral, no months on a list. Most people have never had their fasting insulin or hormones measured even once.</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="#F26B2A" style="background:#F26B2A;border-radius:7px;">
<a href="https://metabolicgfcxtremefit.com/lab.html" style="display:block;padding:15px 24px;font:800 15px/1.2 Helvetica,Arial,sans-serif;color:#ffffff;text-decoration:none;">See what you'd qualify for &rarr;</a>
</td></tr></table>
<p style="margin:18px 0 0;padding-top:16px;border-top:1px solid #27272a;font:400 13px/1.55 Helvetica,Arial,sans-serif;color:#a1a1aa;"><strong style="color:#F26B2A;">Best Supplements</strong> &mdash; one hand-picked brand per category, at an exclusive discount. <a href="https://metabolicgfcxtremefit.com/fortify.html" style="color:#ffffff;font-weight:700;">See what's worth buying &rarr;</a></p>
</td></tr></table></td></tr>'''

def foot():
    return '''<tr><td bgcolor="#f4f4f5" style="background:#f4f4f5;padding:18px 22px;font-family:Helvetica,Arial,sans-serif;border-top:1px solid #e4e4e7;">
<p style="margin:0 0 5px;font:700 13px/1.3 Helvetica,Arial,sans-serif;color:#27272a;">GFC Xtreme Fitness &middot; Metabolic Flex</p>
<p style="margin:0;font:italic 400 11px/1.5 Helvetica,Arial,sans-serif;color:#71717a;">Prescription treatments require evaluation by a licensed clinician, where legally permitted. Clinicians prescribe; your coach does not. Individual results vary.</p>
</td></tr>
</table></td></tr></table>'''

def hero_small(src, href, cap=""):
    """Contained picture, ~60% width, centred."""
    c = f'<tr><td align="center" style="padding:9px 30px 0;"><p style="margin:0;font:400 12px/1.5 Helvetica,Arial,sans-serif;color:#71717a;text-align:center;">{cap}</p></td></tr>' if cap else ""
    return f'''<tr><td align="center" style="padding:4px 22px 0;">
<a href="{href}" style="text-decoration:none;display:block;"><img src="{M}/{src}" alt="" width="300" style="width:300px;max-width:85%;height:auto;display:block;border:0;border-radius:10px;"></a>
</td></tr>{c}'''

def hero_side(src, href, html):
    """Thumbnail left, copy right."""
    return f'''<tr><td style="padding:6px 22px 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
<td width="150" valign="top" style="padding-right:14px;">
<a href="{href}" style="text-decoration:none;display:block;"><img src="{M}/{src}" alt="" width="150" style="width:150px;height:auto;display:block;border:0;border-radius:8px;"></a></td>
<td valign="top" style="font-family:Helvetica,Arial,sans-serif;">
<p style="margin:0;font:400 15px/1.55 Helvetica,Arial,sans-serif;color:#3f3f46;">{html}</p></td>
</tr></table></td></tr>'''
