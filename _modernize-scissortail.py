#!/usr/bin/env python3
"""Modernize scissortailbath.com page markup (2026-10-01, round 2 redesign to the 904epoxyfloors bar).

Pairs with css/modern.css. Presentation only plus defect fixes. Keeps every title, meta tag,
canonical, H1, JSON-LD block, analytics script, form field and form endpoint, phone number and
claim exactly as they were (Costa 2026-10-01: do not remove claims, do not touch titles/meta/H1).

  - drops styles.v1.css + style.v2.5.css + site-theme.css + Phosphor icon font; loads Outfit/DM Sans
    and /css/modern.css LAST; body gets class "st st-<kind>"
  - every Phosphor <i> icon becomes a solid inline SVG (fill=currentColor)
  - header: brand matches the domain (Scissortail Bath), Services and Areas dropdowns
  - photo heroes (breadcrumb moved into the hero), stats card over the hero edge, alternating
    bands, numbered process, quote cards, price cards, native <details> FAQ, dark photo CTA band
  - defect fixes: placeholder SVG "Before/After" and "Professional Team Photo" graphics replaced by
    real photos; contact page hero never closed (whole page rendered inside the hero) and had no
    contact details; About "Why choose" grid left an orphan card (now 2 x 2)
Leading underscore keeps it out of the GitHub Pages (Jekyll) build. Idempotent: a page whose <body> already carries class "st" is skipped.
Never touches job/, lead*/, estimate/ (estimate is a form page with its own styles).

usage: python3 _modernize-scissortail.py [repo-root]
"""
import os, re, sys, glob

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
V = '20261001r2b'
PHONE = '(405) 281-3672'
TEL = 'tel:4052813672'

def svg(body, cls='ic'):
    return f'<svg class="{cls}" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">{body}</svg>'

# Heroicons 20 solid paths (MIT) plus a few simple solid shapes drawn for this site
P = {
 'phone': '<path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.513 2.31a1.5 1.5 0 0 1-1.02 1.737l-1.183.394a.531.531 0 0 0-.316.712 11.042 11.042 0 0 0 5.567 5.567c.27.12.588-.006.712-.316l.394-1.183a1.5 1.5 0 0 1 1.737-1.02l2.31.513A1.5 1.5 0 0 1 18 14.352V15.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 7.326 13.019 13.019 0 0 1 2 4V3.5Z" clip-rule="evenodd"/>',
 'arrow-right': '<path fill-rule="evenodd" d="M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z" clip-rule="evenodd"/>',
 'check-circle': '<path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clip-rule="evenodd"/>',
 'shield-check': '<path fill-rule="evenodd" d="M9.661 2.237a.531.531 0 0 1 .678 0 11.947 11.947 0 0 0 7.078 2.749.5.5 0 0 1 .479.425c.069.52.104 1.05.104 1.59 0 5.162-3.26 9.563-7.834 11.256a.48.48 0 0 1-.332 0C5.26 16.564 2 12.163 2 7c0-.538.035-1.069.104-1.589a.5.5 0 0 1 .48-.425 11.947 11.947 0 0 0 7.077-2.75Zm4.196 5.954a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z" clip-rule="evenodd"/>',
 'calculator': '<path fill-rule="evenodd" d="M10 1c-1.716 0-3.408.106-5.07.31C3.806 1.45 3 2.414 3 3.517V16.75A2.25 2.25 0 0 0 5.25 19h9.5A2.25 2.25 0 0 0 17 16.75V3.517c0-1.103-.806-2.068-1.93-2.207A41.403 41.403 0 0 0 10 1ZM5.99 8.75A.75.75 0 0 1 6.74 8h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75v-.01Zm.75 1.417a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75v-.01a.75.75 0 0 0-.75-.75h-.01Zm-.75 2.916a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75v-.01Zm.75 1.417a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75v-.01a.75.75 0 0 0-.75-.75h-.01Zm1.417-5.75a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75v-.01Zm.75 1.417a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75v-.01a.75.75 0 0 0-.75-.75h-.01Zm-.75 2.916a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75v-.01Zm.75 1.417a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75v-.01a.75.75 0 0 0-.75-.75h-.01Zm1.42-5.75a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75v-.01Zm.75 1.417a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75v-.01a.75.75 0 0 0-.75-.75h-.01Zm-.75 2.916a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75h-.01a.75.75 0 0 1-.75-.75v-.01Zm.75 1.417a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75v-.01a.75.75 0 0 0-.75-.75h-.01ZM6.25 3.5a.75.75 0 0 0-.75.75v1.5c0 .414.336.75.75.75h7.5a.75.75 0 0 0 .75-.75v-1.5a.75.75 0 0 0-.75-.75h-7.5Z" clip-rule="evenodd"/>',
 'star': '<path fill-rule="evenodd" d="M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401Z" clip-rule="evenodd"/>',
 'clock': '<path fill-rule="evenodd" d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm.75-13a.75.75 0 0 0-1.5 0v5c0 .199.079.39.22.53l3 3a.75.75 0 1 0 1.06-1.06l-2.78-2.78V5Z" clip-rule="evenodd"/>',
 'calendar': '<path d="M5.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H6a.75.75 0 0 1-.75-.75V12ZM6 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H6ZM7.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H8a.75.75 0 0 1-.75-.75V12ZM8 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H8ZM9.25 10a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H10a.75.75 0 0 1-.75-.75V10ZM10 11.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V12a.75.75 0 0 0-.75-.75H10ZM9.25 14a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H10a.75.75 0 0 1-.75-.75V14ZM12 9.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V10a.75.75 0 0 0-.75-.75H12ZM11.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H12a.75.75 0 0 1-.75-.75V12ZM12 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H12ZM13.25 10a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H14a.75.75 0 0 1-.75-.75V10ZM14 11.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V12a.75.75 0 0 0-.75-.75H14Z"/><path fill-rule="evenodd" d="M5.75 2a.75.75 0 0 1 .75.75V4h7V2.75a.75.75 0 0 1 1.5 0V4h.25A2.75 2.75 0 0 1 18 6.75v8.5A2.75 2.75 0 0 1 15.25 18H4.75A2.75 2.75 0 0 1 2 15.25v-8.5A2.75 2.75 0 0 1 4.75 4H5V2.75A.75.75 0 0 1 5.75 2Zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75Z" clip-rule="evenodd"/>',
 'clipboard': '<path fill-rule="evenodd" d="M18 5.25a2.25 2.25 0 0 0-2.012-2.238A2.25 2.25 0 0 0 13.75 1h-1.5a2.25 2.25 0 0 0-2.238 2.012c-.875.092-1.6.686-1.884 1.488H11A2.5 2.5 0 0 1 13.5 7v7h2.25A2.25 2.25 0 0 0 18 11.75v-6.5ZM12.25 2.5a.75.75 0 0 0-.75.75v.25h3v-.25a.75.75 0 0 0-.75-.75h-1.5Z" clip-rule="evenodd"/><path fill-rule="evenodd" d="M3 6a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1H3Zm6.874 4.166a.75.75 0 1 0-1.248-.832l-2.493 3.739-.853-.853a.75.75 0 0 0-1.06 1.06l1.5 1.5a.75.75 0 0 0 1.154-.114l3-4.5Z" clip-rule="evenodd"/>',
 'map-pin': '<path fill-rule="evenodd" d="m9.69 18.933.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 0 0 .281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 1 0 3 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 0 0 2.273 1.765 11.842 11.842 0 0 0 .976.544l.062.029.018.008.006.003ZM10 11.25a2.25 2.25 0 1 0 0-4.5 2.25 2.25 0 0 0 0 4.5Z" clip-rule="evenodd"/>',
 'home': '<path fill-rule="evenodd" d="M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z" clip-rule="evenodd"/>',
 'banknotes': '<path fill-rule="evenodd" d="M1 4a1 1 0 0 1 1-1h16a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V4Zm12 4a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM4 9a1 1 0 1 0 0-2 1 1 0 0 0 0 2Zm13-1a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM1.75 14.5a.75.75 0 0 0 0 1.5c4.417 0 8.693.603 12.749 1.73 1.111.309 2.251-.512 2.251-1.696v-.784a.75.75 0 0 0-1.5 0v.784a.272.272 0 0 1-.35.25A49.043 49.043 0 0 0 1.75 14.5Z" clip-rule="evenodd"/>',
 'sparkles': '<path d="M15.98 1.804a1 1 0 0 0-1.96 0l-.24 1.192a1 1 0 0 1-.784.785l-1.192.238a1 1 0 0 0 0 1.962l1.192.238a1 1 0 0 1 .785.785l.238 1.192a1 1 0 0 0 1.962 0l.238-1.192a1 1 0 0 1 .785-.785l1.192-.238a1 1 0 0 0 0-1.962l-1.192-.238a1 1 0 0 1-.785-.785l-.238-1.192ZM6.949 5.684a1 1 0 0 0-1.898 0l-.683 2.051a1 1 0 0 1-.633.633l-2.051.683a1 1 0 0 0 0 1.898l2.051.684a1 1 0 0 1 .633.632l.683 2.051a1 1 0 0 0 1.898 0l.683-2.051a1 1 0 0 1 .633-.633l2.051-.683a1 1 0 0 0 0-1.898l-2.051-.683a1 1 0 0 1-.633-.633L6.95 5.684ZM13.949 13.684a1 1 0 0 0-1.898 0l-.184.551a1 1 0 0 1-.632.633l-.551.183a1 1 0 0 0 0 1.898l.551.183a1 1 0 0 1 .633.633l.183.551a1 1 0 0 0 1.898 0l.184-.551a1 1 0 0 1 .632-.633l.551-.183a1 1 0 0 0 0-1.898l-.551-.184a1 1 0 0 1-.633-.632l-.183-.551Z"/>',
 'envelope': '<path d="M3 4a2 2 0 0 0-2 2v1.161l8.441 4.221a1.25 1.25 0 0 0 1.118 0L19 7.162V6a2 2 0 0 0-2-2H3Z"/><path d="m19 8.839-7.77 3.885a2.75 2.75 0 0 1-2.46 0L1 8.839V14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.839Z"/>',
 'user-circle': '<path fill-rule="evenodd" d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-5.5-2.5a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0ZM10 12a5.99 5.99 0 0 0-4.793 2.39A6.483 6.483 0 0 0 10 16.5a6.483 6.483 0 0 0 4.793-2.11A5.99 5.99 0 0 0 10 12Z" clip-rule="evenodd"/>',
 'paper-airplane': '<path d="M3.105 2.288a.75.75 0 0 0-.826.95l1.414 4.926A1.5 1.5 0 0 0 5.135 9.25h6.115a.75.75 0 0 1 0 1.5H5.135a1.5 1.5 0 0 0-1.442 1.086l-1.414 4.926a.75.75 0 0 0 .826.95 28.897 28.897 0 0 0 15.293-7.155.75.75 0 0 0 0-1.114A28.897 28.897 0 0 0 3.105 2.288Z"/>',
 'bars-3': '<path fill-rule="evenodd" d="M2 4.75A.75.75 0 0 1 2.75 4h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 4.75ZM2 10a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 10Zm0 5.25a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1-.75-.75Z" clip-rule="evenodd"/>',
 'chevron-down': '<path fill-rule="evenodd" d="M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z" clip-rule="evenodd"/>',
 # simple solid shapes drawn for this site (no heroicon exists for these fixtures)
 'bathtub': '<path d="M4 8.5V4.75a2.75 2.75 0 0 1 5.37-.83.75.75 0 1 1-1.43.45A1.25 1.25 0 0 0 5.5 4.75V8.5H17a1 1 0 0 1 1 1v1.25a5 5 0 0 1-3 4.58V16.5a.75.75 0 0 1-1.5 0v-.75h-7v.75a.75.75 0 0 1-1.5 0v-1.17a5 5 0 0 1-3-4.58V9.5a1 1 0 0 1 1-1h1Z"/>',
 'shower': '<path d="M10 2a.75.75 0 0 1 .75.75v1.3A6 6 0 0 1 16 10H4a6 6 0 0 1 5.25-5.95v-1.3A.75.75 0 0 1 10 2Z"/><circle cx="6" cy="13" r="1.1"/><circle cx="10" cy="13" r="1.1"/><circle cx="14" cy="13" r="1.1"/><circle cx="8" cy="16.5" r="1.1"/><circle cx="12" cy="16.5" r="1.1"/>',
 'squares': '<rect x="2.5" y="2.5" width="6.5" height="6.5" rx="1.5"/><rect x="11" y="2.5" width="6.5" height="6.5" rx="1.5"/><rect x="2.5" y="11" width="6.5" height="6.5" rx="1.5"/><rect x="11" y="11" width="6.5" height="6.5" rx="1.5"/>',
 'mirror': '<path fill-rule="evenodd" d="M10 1.5c3.04 0 5.5 2.91 5.5 6.5s-2.46 6.5-5.5 6.5S4.5 11.59 4.5 8 6.96 1.5 10 1.5Zm-1.9 3.1a.75.75 0 0 0-1.06.06A4.9 4.9 0 0 0 6 7.6a.75.75 0 0 0 1.5 0c0-.73.24-1.43.66-1.94a.75.75 0 0 0-.06-1.06Z" clip-rule="evenodd"/><path d="M9.25 14.9h1.5V17h2.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.5v-2.1Z"/>',
 'accessible': '<circle cx="9.5" cy="3.25" r="1.75"/><path d="M8.25 6.25a1 1 0 0 1 2 0v2.5h3a.75.75 0 0 1 0 1.5h-3v1.25h3.6a1 1 0 0 1 .95.68l1.35 4.06a.75.75 0 1 1-1.42.48l-1.2-3.72H9.25a1 1 0 0 1-1-1V6.25Z"/><path d="M6.04 8.9a.75.75 0 0 1 .4.98 4.25 4.25 0 0 0 6.06 5.32.75.75 0 1 1 .77 1.29A5.75 5.75 0 0 1 5.06 9.3a.75.75 0 0 1 .98-.4Z"/>',
 'diamond': '<path d="M5.6 3h8.8l3.6 4.6-8 9.4-8-9.4L5.6 3Z"/>',
}
def I(name, cls='ic'): return svg(P[name], cls)

PH = {'phone': 'phone', 'arrow-right': 'arrow-right', 'check-circle': 'check-circle', 'shield-check': 'shield-check',
      'calculator': 'calculator', 'star': 'star', 'clock': 'clock', 'calendar-check': 'calendar', 'clipboard': 'clipboard',
      'map-pin': 'map-pin', 'house': 'home', 'currency-dollar': 'banknotes', 'diamond': 'diamond', 'user-circle': 'user-circle',
      'envelope': 'envelope', 'paper-plane-tilt': 'paper-airplane', 'list': 'bars-3', 'bathtub': 'bathtub', 'shower': 'shower',
      'squares-four': 'squares', 'mirror': 'mirror', 'wheelchair': 'accessible', 'arrows-horizontal': 'arrow-right'}

SERVICES = [('full-bathroom-remodel', 'Full Bathroom Remodel', 'svc-full'), ('shower-remodel', 'Shower Remodel', 'svc-shower'),
            ('bathtub-replacement', 'Bathtub Replacement', 'svc-tub'), ('tile-installation', 'Tile Installation', 'svc-tile'),
            ('vanity-upgrade', 'Vanity Upgrade', 'svc-vanity'), ('accessibility-remodel', 'Accessibility Remodel', 'svc-access')]
SVC_IMG = {s: im for s, _, im in SERVICES}
AREAS = [('edmond', 'Edmond'), ('oklahoma-city', 'Oklahoma City'), ('yukon', 'Yukon'), ('mustang', 'Mustang'), ('piedmont', 'Piedmont'),
         ('norman', 'Norman'), ('moore', 'Moore'), ('midwest-city', 'Midwest City'), ('del-city', 'Del City'), ('el-reno', 'El Reno')]
LOC_IMG = {'edmond': 'site/okc-home', 'oklahoma-city': 'site/home-hero', 'yukon': 'site/svc-tub', 'mustang': 'site/svc-vanity',
           'piedmont': 'site/okc-home', 'norman': 'site/svc-shower', 'moore': 'before-after/ba1-after', 'midwest-city': 'site/svc-tile',
           'del-city': 'site/home-hero', 'el-reno': 'site/svc-vanity'}
PAGE_IMG = {'about.html': 'site/svc-full', 'contact.html': 'site/home-hero', 'faq.html': 'niche-3', 'privacy-policy.html': 'site/home-hero',
            'terms-of-service.html': 'site/home-hero', 'blog/index.html': 'site/svc-vanity',
            'blog/how-much-does-bathroom-remodeling-cost-edmond.html': 'site/svc-full'}

def img_url(key): return f'/images/{key}.jpg'

def nav(active):
    a = lambda k: ' class="active"' if k == active else ''
    svc = ''.join(f'<a href="/services/{s}.html">{t}</a>' for s, t, _ in SERVICES)
    loc = ''.join(f'<a href="/locations/{s}.html">{t}</a>' for s, t in AREAS)
    return (f'<nav class="header__nav" id="mainNav">\n'
            f'      <a href="/"{a("home")}>Home</a>\n'
            f'      <div class="nav-dd"><a href="/services/full-bathroom-remodel.html" aria-haspopup="true"{a("svc")}>Services {I("chevron-down")}</a><div class="nav-dd__menu">{svc}</div></div>\n'
            f'      <div class="nav-dd"><a href="/locations/edmond.html" aria-haspopup="true"{a("loc")}>Areas {I("chevron-down")}</a><div class="nav-dd__menu nav-dd__menu--cols">{loc}</div></div>\n'
            f'      <a href="/about.html"{a("about")}>About</a>\n'
            f'      <a href="/blog/"{a("blog")}>Blog</a>\n'
            f'      <a href="/faq.html"{a("faq")}>FAQ</a>\n'
            f'      <a href="/contact.html"{a("contact")}>Contact</a>\n'
            f'      <a href="{TEL}" class="header__phone header__phone--mobile-only">{I("phone")} {PHONE}</a>\n'
            f'    </nav>')

def hero_ctas():
    return (f'<div class="hero-ctas"><a href="{TEL}" class="st-btn">{I("phone")} Call {PHONE}</a>'
            f'<a href="/estimate/" class="st-btn st-btn--ghost">{I("calendar")} Free Estimate</a></div>')

def side_card(img, alt):
    return (f'<aside class="side-card"><img src="{img}" alt="{alt}" loading="lazy" width="1024" height="768">'
            f'<div class="side-card__body"><h3>Get a Free Estimate</h3>'
            f'<p>Call or send your project details and we will schedule your free in-home estimate.</p>'
            f'<a href="{TEL}" class="st-btn">{I("phone")} Call {PHONE}</a>'
            f'<a href="/estimate/" class="st-btn st-btn--line">{I("calendar")} Request a Free Quote</a></div></aside>')

KEEP_STYLE = re.compile(r'display:\s*none|-9999px|^--(?:hero|cta)-img')

def strip_styles(s):
    return re.sub(r'\s+style="([^"]*)"', lambda m: m.group(0) if KEEP_STYLE.search(m.group(1)) else '', s)

def faq_details(s):
    # button accordion -> native details
    s = re.sub(r'<div class="faq-item">\s*<button class="faq-item__q">(.*?)\s*(?:<i class="ph ph-caret-down"></i>)?</button>\s*'
               r'<div class="faq-item__a">\s*<div class="faq-item__a-inner">(.*?)</div>\s*</div>\s*</div>',
               lambda m: f'<details class="faq-item"><summary>{m.group(1).strip()}</summary><div class="faq-a"><p>{m.group(2).strip()}</p></div></details>', s, flags=re.S)
    # h3 + p blocks -> details (heading stays an h3)
    s = re.sub(r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*(.*?)\s*</div>',
               lambda m: f'<details class="faq-item"><summary><h3>{m.group(1)}</h3></summary><div class="faq-a">{m.group(2)}</div></details>', s, flags=re.S)
    return s

def breadcrumb_list(body):
    """Pull the breadcrumb out of its strip; return (body_without_strip, list_html)."""
    m = re.search(r'<nav class="breadcrumbs?"[^>]*>.*?</nav>\s*', body, flags=re.S)
    if not m: return body, ''
    inner = m.group(0)
    parts = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>|<span[^>]*>(?!/|&rsaquo;)([^<]+)</span>', inner)
    items = []
    for href, text, cur in parts:
        if href: items.append(f'<a href="{href}">{text.strip()}</a>')
        elif cur.strip() and cur.strip() not in ('/', '›'): items.append(f'<span aria-current="page">{cur.strip()}</span>')
    lst = '<nav class="breadcrumbs" aria-label="Breadcrumb"><div class="breadcrumbs__list">' + '<span aria-hidden="true">/</span>'.join(items) + '</div></nav>'
    return body.replace(m.group(0), '', 1), lst

def head_swap(head):
    head = re.sub(r'\s*<link rel="preload" href="[^"]*styles\.v1\.css" as="style">', '', head)
    head = re.sub(r'\s*<!-- Preload hero CSS -->', '', head)
    head = re.sub(r'\s*<script defer src="https://unpkg\.com/@phosphor-icons[^"]*"[^>]*></script>', '', head)
    head = re.sub(r'\s*<link rel="stylesheet" href="https://unpkg\.com/@phosphor-icons[^"]*"[^>]*>', '', head)
    head = re.sub(r'\s*<link rel="preconnect" href="https://unpkg\.com">', '', head)
    head = re.sub(r'\s*<!-- Phosphor Icons \(defer\) -->', '', head)
    head = re.sub(r'\s*<link rel="stylesheet" href="(?:\.\./|/)?css/(?:styles\.v1|style\.v2\.5|site-theme)\.css[^"]*">', '', head)
    head = re.sub(r'\s*<link href="https://fonts\.googleapis\.com/css2\?family=Space\+Grotesk[^"]*" rel="stylesheet">', '', head)
    if 'fonts.gstatic.com' not in head:
        head = head.replace('</head>', '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n</head>', 1)
    add = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=DM+Sans:wght@400;500;600;700;800&display=swap">\n'
           f'<link rel="stylesheet" href="/css/modern.css?v={V}">\n</head>')
    return head.replace('</head>', add, 1)

def common_body(body, kind, active):
    # header: brand + nav + icons
    body = re.sub(r'<a href="/" class="header__brand">Edmond <span>Bathroom Remodeling</span></a>',
                  '<a href="/" class="header__brand"><span class="brand-mark" aria-hidden="true">SB</span>Scissortail <span>Bath</span></a>', body)
    body = re.sub(r'<nav class="header__nav" id="mainNav">.*?</nav>', lambda m: nav(active), body, count=1, flags=re.S)
    body = body.replace('<button class="header__toggle" aria-label="Menu" aria-expanded="false"><i class="ph ph-list"></i></button>',
                        f'<button class="header__toggle" aria-label="Menu" aria-expanded="false" aria-controls="mainNav">{I("bars-3")}</button>')
    body = body.replace('<header class="header" id="header">', '<header class="header">')
    # footer brand
    body = body.replace('<div class="footer__brand">Edmond <span>Bathroom Remodeling</span></div>',
                        '<div class="footer__brand"><span class="brand-mark" aria-hidden="true">SB</span>Scissortail <span>Bath</span></div>')
    # phosphor icons -> inline svg
    def ph(m):
        n = m.group(1)
        if n == 'caret-down': return ''
        if n not in PH: raise SystemExit(f'unmapped icon ph-{n}')
        return I(PH[n])
    body = re.sub(r'<i class="ph(?:-fill)? ph-([a-z-]+)"[^>]*></i>', ph, body)
    return body

def kind_of(rel):
    if rel == 'index.html': return 'home', 'home'
    if rel.startswith('services/'): return 'svc', 'svc'
    if rel.startswith('locations/'): return 'loc', 'loc'
    if rel == 'blog/index.html': return 'blogidx', 'blog'
    if rel.startswith('blog/'): return 'post', 'blog'
    if rel in ('privacy-policy.html', 'terms-of-service.html'): return 'legal', ''
    if rel in ('thank-you.html', '404.html'): return 'msg', ''
    return 'page', rel.replace('.html', '')

# ---------------------------------------------------------------- home
def home(body):
    # hero: photo background; the placeholder before/after slider (two SVG data-URIs) goes
    body = re.sub(r'<section class="hero">\s*<div class="hero__overlay"></div>',
                  f'<section class="hero" style="--hero-img:url({img_url("site/home-hero")})">', body, count=1)
    body = re.sub(r'\s*<div class="hero__slider-wrap">.*?</div>\s*</div>\s*</div>\s*</section>', '\n  </div>\n</section>', body, count=1, flags=re.S)
    # trust bar items: icon badge
    # services: section header photo moves to the About block (it shows the team at work), cards get photos
    body = re.sub(r'\n<img src="/images/niche-4\.jpg" alt="[^"]*" loading="lazy" style="[^"]*">\n', '\n', body, count=1)
    body = body.replace('<section class="services" id="services">', '<section class="services home-first" id="services">', 1)
    # About: placeholder "Our Work" SVG -> real photo (same alt text)
    body = re.sub(r'<img src="data:image/svg\+xml[^"]*" alt="Scissortail Bath team at work" width="600" height="450">',
                  '<img src="/images/niche-4.jpg" alt="Scissortail Bath team at work" width="1024" height="1024" loading="lazy">', body, count=1)
    body = body.replace('<section class="about" id="about">', '<section class="about band--soft" id="about">', 1)
    # AGITATE -> 2 x 2 cards
    body = body.replace('<!-- AGITATE -->\n<section class="section" style="background:#fff;">', '<!-- AGITATE -->\n<section class="section band">', 1)
    body = body.replace('<ul style="max-width:800px;margin:0 auto;font-size:1.05rem;line-height:1.8;color:#374151;list-style:none;padding:0;">', '<ul class="pain-grid">', 1)
    # PROCESS -> numbered steps on a dark band
    def proc(m):
        steps = re.findall(r'<div style="flex-shrink:0;[^"]*">(\d)</div>\s*<div style="[^"]*">(.*?)</div>', m.group(2), flags=re.S)
        lis = ''.join(f'\n      <li class="step"><span class="step__num">{n}</span><div class="step__body">{t}</div></li>' for n, t in steps)
        return m.group(1) + f'<ol class="steps">{lis}\n    </ol>\n  </div>\n</section>'
    body = re.sub(r'(<!-- PROCESS -->\n<section class="section)" style="background:#f8fafc;">(.*?)</div>\s*</div>\s*</section>',
                  lambda m: proc(re.match(r'(.*?<div class="container">\s*<div class="section-header">.*?</div>\s*)<div style="max-width:800px;margin:0 auto;">(.*)', m.group(0), flags=re.S)), body, count=1, flags=re.S)
    body = body.replace('<!-- PROCESS -->\n<section class="section" style="background:#f8fafc;">', '<!-- PROCESS -->\n<section class="section band--dark" id="process">', 1)
    # TESTIMONIALS -> quote cards (text unchanged)
    body = body.replace('<!-- TESTIMONIALS -->\n<section class="section" style="background:#f8fafc;">', '<!-- TESTIMONIALS -->\n<section class="section band--soft">', 1)
    body = body.replace('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px;margin-top:32px;">', '<div class="quote-grid">', 1)
    body = body.replace('<div style="background:white;border-radius:12px;padding:28px;border:1px solid #e2e8f0;box-shadow:0 2px 8px rgba(0,0,0,0.06);">', '<div class="quote-card">')
    body = body.replace('<p style="font-style:italic;color:#374151;line-height:1.7;margin-bottom:16px;">', '<p class="quote-card__text">')
    body = body.replace('<p style="font-weight:600;color:var(--primary);">', '<p class="quote-card__by">')
    body = body.replace('&nbsp;<span style="color:#64748b;font-weight:400;">', '&nbsp;<span>')
    # BEFORE/AFTER gallery
    body = body.replace('<!-- BEFORE/AFTER GALLERY -->\n<section class="section" style="background:white;">', '<!-- BEFORE/AFTER GALLERY -->\n<section class="section band">', 1)
    body = body.replace('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:32px;margin-top:32px;">', '<div class="ba-grid">', 1)
    body = body.replace('<div style="border-radius:12px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.12);">', '<div class="ba-card">')
    body = body.replace('<div style="display:grid;grid-template-columns:1fr 1fr;gap:2px;">', '<div class="ba-pair">')
    body = body.replace('<div style="position:relative;">', '<div class="ba-fig">')
    body = re.sub(r'<span style="position:absolute;top:8px;left:8px;background:rgba\(0,0,0,0\.7\)[^"]*">', '<span class="ba-tag">', body)
    body = re.sub(r'<span style="position:absolute;top:8px;left:8px;background:var\(--accent[^"]*">', '<span class="ba-tag ba-tag--after">', body)
    body = body.replace('src="images/before-after/', 'src="/images/before-after/')
    # PRICING -> price cards
    body = body.replace('<!-- PRICING TRANSPARENCY -->\n<section class="section" style="background:white;">', '<!-- PRICING TRANSPARENCY -->\n<section class="section band--soft">', 1)
    body = body.replace('<div style="max-width:800px;margin:0 auto;display:grid;gap:20px;">', '<div class="price-grid">', 1)
    body = body.replace('<div style="background:#f8fafc;border-radius:12px;padding:28px;border:1px solid #e2e8f0;">', '<div class="price-card">')
    body = body.replace('<p style="font-size:1.2rem;font-weight:700;color:var(--accent,#c8102e);margin-bottom:8px;">', '<p class="price-card__price">')
    body = body.replace('<div style="background:#fff8f0;border-radius:12px;padding:20px 28px;border-left:4px solid var(--accent,#c8102e);">', '<div class="price-note">')
    body = re.sub(r'(<div class="price-note">.*?</div>)(\s*)</div>', r'</div>\2\1', body, count=1, flags=re.S)  # note sits under the 3 cards, not as a 4th grid cell
    body = card_photos(body)
    # FAQ + contact + local section
    body = body.replace('<section class="contact" id="contact">', '<section class="contact band--soft" id="contact">', 1)
    body = re.sub(r'<!-- LOCAL SPECIFICITY -->\n<section class="content-section">\n  <div class="container">\n(.*?)  </div>\n</section>',
                  lambda m: ('<!-- LOCAL SPECIFICITY -->\n<section class="content-section band">\n  <div class="container split split--wide">\n'
                             f'    <div>\n{m.group(1)}    </div>\n    <div class="split__img"><img src="{img_url("site/okc-home")}" alt="Brick ranch home in Edmond, Oklahoma" loading="lazy" width="1600" height="1095"></div>\n  </div>\n</section>'),
                  body, count=1, flags=re.S)
    return body

# ---------------------------------------------------------------- service + location pages
def card_photos(body):
    def add(m):
        slug = m.group(2)
        return (m.group(1) + f'<div class="service-card__img"><img src="{img_url("site/" + SVC_IMG[slug])}" alt="" loading="lazy" width="1200" height="821"></div>\n        ')
    return re.sub(r'(<div class="service-card">\s*)(?=<div class="service-card__icon">.*?href="/services/([a-z-]+)\.html")',
                  lambda m: m.group(1) + f'<div class="service-card__img"><img src="{img_url("site/" + SVC_IMG[m.group(2)])}" alt="" loading="lazy" width="1200" height="821"></div>\n        ',
                  body, flags=re.S)

def inner(body, rel, kind):
    body, crumbs = breadcrumb_list(body)
    slug = os.path.basename(rel)[:-5]
    if kind == 'svc': hero_img = img_url('site/' + SVC_IMG[slug])
    elif kind == 'loc': hero_img = img_url(LOC_IMG[slug])
    else: hero_img = img_url(PAGE_IMG.get(rel, 'site/home-hero'))
    # the injected square photo inside the hero moves to the side card (svc/loc) or is dropped (faq: it becomes the hero photo)
    side_img = None
    m = re.search(r'\n<img src="(/images/niche-\d\.jpg)" alt="([^"]*)" loading="lazy" style="[^"]*">\n', body)
    if m and kind in ('svc', 'loc'):
        side_img = (m.group(1), m.group(2)); body = body.replace(m.group(0), '\n', 1)
    if rel == 'faq.html' and m:
        body = body.replace(m.group(0), '\n', 1)
    # hero
    def hero(mm):
        inner_html = mm.group(1)
        cta = hero_ctas() if kind in ('svc', 'loc') else ''
        return f'<section class="page-hero" style="--hero-img:url({hero_img})">\n  <div class="container">\n    {crumbs}{inner_html.rstrip()}\n    {cta}\n  </div>\n</section>'
    if rel == 'contact.html':
        body = contact_fix(body, crumbs, hero_img)
    else:
        body = re.sub(r'<section class="page-hero">\s*<div class="container">(.*?)</div>\s*</section>', hero, body, count=1, flags=re.S)
    # article + side card
    if kind in ('svc', 'loc'):
        img, alt = side_img if side_img else (img_url('site/home-hero'), 'Remodeled bathroom')
        body = re.sub(r'<section class="page-content">\s*<div class="container">(.*?)\n  </div>\n</section>',
                      lambda mm: f'<section class="page-content">\n  <div class="container layout-split">\n    <div class="prose">{mm.group(1)}\n    </div>\n    {side_card(img, alt)}\n  </div>\n</section>',
                      body, count=1, flags=re.S)
        body = card_photos(body)
        body = body.replace('<section class="content-section">', '<section class="content-section band--soft">' if kind == 'svc' else '<section class="content-section">', 1)
    if rel == 'about.html':
        body = re.sub(r'<svg viewBox="0 0 600 450" xmlns="http://www\.w3\.org/2000/svg" role="img" aria-label="Bathroom remodeling team at work">.*?</svg>',
                      '<img src="/images/niche-3.jpg" alt="Bathroom remodeling team at work" width="1024" height="1024" loading="lazy">', body, count=1, flags=re.S)
        body = re.sub(r'(<img src="/images/niche-1\.jpg" alt="[^"]*" loading="lazy") style="[^"]*">', r'\1 width="1024" height="1024">', body)
        body = body.replace('<div class="services-grid" style="margin-top:1.5rem;margin-bottom:2.5rem">', '<div class="services-grid">')
        body = body.replace('<div class="locations-grid" style="margin-top:1.5rem">', '<div class="locations-grid">')
        body = body.replace('<section class="content-section">', '<section class="content-section band--soft">', 1)
    if rel == 'faq.html':
        body = body.replace('<section class="section section--alt">', '<section class="section band">', 1)
        body = body.replace('<section class="content-section">', '<section class="content-section band--soft has-faq">', 1)
    return body

def contact_fix(body, crumbs, hero_img):
    """The hero <section> never closed: every H2, list and FAQ rendered inside the dark hero and
    the page had no phone/email/hours block. Close the hero after the H1, move the copy into a
    content band with the contact details that the home page already lists."""
    m = re.search(r'<section class="page-hero">\s*<div class="container">\s*<h1>Contact Us</h1>\n(.*?)(?=<footer class="footer">)', body, flags=re.S)
    if not m: raise SystemExit('contact.html: hero pattern not found')
    copy = m.group(1).rstrip()
    details = ('<aside class="side-card"><img src="/images/site/svc-vanity.jpg" alt="Remodeled bathroom vanity" loading="lazy" width="1200" height="821">'
               '<div class="side-card__body"><h3>Get Your Free Estimate</h3>'
               f'<div class="detail-row">{I("phone")}<a href="{TEL}">{PHONE}</a></div>'
               f'<div class="detail-row">{I("envelope")}<a href="mailto:contact@scissortailbath.com">contact@scissortailbath.com</a></div>'
               f'<div class="detail-row">{I("map-pin")}<span>Edmond, Oklahoma</span></div>'
               f'<div class="detail-row">{I("clock")}<span>Mon&ndash;Sat: 7:00 AM &ndash; 6:00 PM</span></div>'
               f'<a href="/estimate/" class="st-btn">{I("calendar")} Request a Free Quote</a></div></aside>')
    new = (f'<section class="page-hero" style="--hero-img:url({hero_img})">\n  <div class="container">\n    {crumbs}<h1>Contact Us</h1>\n    {hero_ctas()}\n  </div>\n</section>\n\n'
           f'<section class="page-content">\n  <div class="container layout-split">\n    <div class="prose">\n{copy}\n    </div>\n    {details}\n  </div>\n</section>\n\n')
    return body.replace(m.group(0), new, 1)

# ---------------------------------------------------------------- blog
def blog_index(body):
    body, crumbs = breadcrumb_list(body)
    m = re.search(r'<section class="section"[^>]*>\s*<div class="container"[^>]*>\s*<div class="section-header"[^>]*>\s*(<h1[^>]*>.*?</h1>)\s*(<p[^>]*>.*?</p>)\s*</div>', body, flags=re.S)
    h1, p = strip_styles(m.group(1)), strip_styles(m.group(2))
    hero = (f'<section class="page-hero" style="--hero-img:url({img_url(PAGE_IMG["blog/index.html"])})">\n  <div class="container">\n    {crumbs}{h1}\n    {p}\n  </div>\n</section>\n\n'
            '<section class="section band--soft">\n  <div class="container">')
    body = body.replace(m.group(0), hero, 1)
    body = strip_styles(body)
    body = re.sub(r'<div>\s*<article>', '<div class="post-list">\n      <article class="post-card">', body, count=1)
    body = re.sub(r'(<article class="post-card">)\s*<p>(.*?)</p>\s*<h2>\s*(<a href="([^"]+)">.*?</a>)\s*</h2>\s*<p>(.*?)</p>\s*<a href="[^"]+">(.*?)</a>',
                  lambda mm: (f'{mm.group(1)}\n        <a class="post-card__img" href="{mm.group(4)}" tabindex="-1" aria-hidden="true"><img src="{img_url("site/svc-full")}" alt="" loading="lazy" width="1200" height="821"></a>\n'
                              f'        <div class="post-card__body"><p class="post-card__meta">{mm.group(2)}</p><h2>{mm.group(3)}</h2><p>{mm.group(5)}</p>'
                              f'<a class="post-card__more" href="{mm.group(4)}">{mm.group(6)}</a></div>'), body, count=1, flags=re.S)
    return body

def blog_post(body, rel):
    body, crumbs = breadcrumb_list(body)
    m = re.search(r'<article class="section"[^>]*>\s*<div class="container"[^>]*>\s*(<h1[^>]*>.*?</h1>)\s*(<p[^>]*>Updated.*?</p>)', body, flags=re.S)
    h1, meta = strip_styles(m.group(1)), strip_styles(m.group(2)).replace('<p>', '<p class="post-meta">', 1)
    body = body.replace(m.group(0), (f'<section class="page-hero" style="--hero-img:url({img_url(PAGE_IMG[rel])})">\n  <div class="container">\n    {crumbs}{h1}\n    {meta}\n  </div>\n</section>\n\n'
                                     '<article class="post">\n  <div class="container">'), 1)
    body = body.replace('<div style="overflow-x:auto;margin:24px 0;">', '<div class="table-wrap">', 1)
    body = re.sub(r'<details style="[^"]*">\s*<summary style="[^"]*">\s*(.*?)\s*</summary>\s*<div style="[^"]*">\s*(.*?)\s*</div>\s*</details>',
                  lambda mm: f'<details class="faq-item"><summary>{mm.group(1)}</summary><div class="faq-a"><p>{mm.group(2)}</p></div></details>', body, flags=re.S)
    body = body.replace('<div style="background:#f8fafc;border-radius:12px;padding:32px;text-align:center;margin-top:48px;border:1px solid #e2e8f0;">', '<div class="post-cta">', 1)
    body = body.replace('<div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">', '<div class="hero-ctas">', 1)
    body = body.replace('class="btn btn--accent" style="font-size:1.05rem;"', 'class="st-btn"').replace('class="btn btn--outline" style="font-size:1.05rem;"', 'class="st-btn st-btn--ghost"')
    return strip_styles(body)


# ---------------------------------------------------------------- copy fixes (round 2 B: spun template text, brand)
CONTACT_COPY = [
 ('<h2>Professional Contact in Edmond, OK</h2>', '<h2>Contact a Bathroom Remodeler in Edmond, OK</h2>'),
 (re.compile(r'<p>Initiating professional contact with Edmond Bathroom Remodeling is the pivotal first step.*?</p>', re.S),
  '<p>Reaching out to Scissortail Bath is the first step for Edmond, OK homeowners who want a bathroom that looks better and works better. Remodeling can feel like a big decision, so we keep getting started simple. Whether your bathroom has dated finishes, an awkward layout or everyday wear and tear, one call or message gets your questions answered and gives you a clear picture of what your project involves. We match the plan to your home and your budget, and the sooner we talk, the sooner we can offer advice and schedule your estimate.</p>'),
 ('<h2>What Is Contact?</h2>', '<h2>What Happens When You Contact Us</h2>'),
 (re.compile(r'<p>For Edmond Bathroom Remodeling, "contact" refers to.*?</p>', re.S),
  '<p>Getting in touch is the first phase of every remodeling project. You can call, email or send the inquiry form on this website. We ask about the scope of work, the style you want and any problems with your current bathroom. That first conversation helps us understand what you have in mind and helps you see how we would approach it.</p>'),
 ('<h2>Benefits of Professional Contact</h2>', '<h2>Benefits of Talking to Us Early</h2>'),
 (re.compile(r'(<strong>Access to Expert Guidance:</strong>).*?</li>', re.S),
  r'\1 By contacting Scissortail Bath, you get advice from experienced design and remodeling professionals on materials, layout options and current design trends, so your remodel works well and looks the way you want.</li>'),
 (re.compile(r'(<strong>Personalized Solutions for Edmond Homes:</strong>).*?</li>', re.S),
  r"\1 Every home in Edmond, OK is different. Our first conversation covers your preferences, your home's style and any local building considerations, so what we propose fits your property and the way you live.</li>"),
 (re.compile(r'(<strong>Transparent Process from the Start:</strong>).*?</li>', re.S),
  r'\1 From your first inquiry you get honest answers, realistic timelines and clear explanations of our services, with no hidden surprises.</li>'),
 (re.compile(r'(<strong>Stress-Free Project Planning:</strong>).*?</li>', re.S),
  r'\1 Contacting us starts a structured planning phase. We guide you from the first idea to the finished bathroom and handle design, material sourcing and scheduling, so the project stays smooth and predictable.</li>'),
 (re.compile(r"<p>At Edmond Bathroom Remodeling, we've refined our contact process.*?</p>", re.S),
  '<p>We keep our contact process simple so every Edmond homeowner starts on the right foot. Our goal is to understand your needs quickly and give you the support your project deserves, from your first call to the moment we present a design proposal.</p>'),
 ('<h2>Why Edmond, OK Properties Need Contact</h2>', '<h2>Why Edmond, OK Homes Benefit From a Local Remodeler</h2>'),
 (re.compile(r'<p>Edmond, OK properties have unique characteristics and demands.*?</p>', re.S),
  "<p>Edmond, OK homes range from older builds to new construction, and many benefit from bathrooms updated to current standards of efficiency and style. As a local remodeler, we understand issues specific to Edmond's climate, such as how humidity affects bathroom ventilation and materials, and we know the home styles common in areas like Oak Tree and Iron Horse Ranch. Many residents remodel to improve resale value, and an updated bathroom is a real draw in Edmond's competitive housing market. Working with a local team means your project follows local regulations and uses local suppliers and trades.</p>"),
 ('<h2>Common Questions About Contact</h2>', '<h2>Common Questions About Getting Started</h2>'),
 ('<h3>How much does Contact cost in Edmond, OK?</h3>', '<h3>How much does a consultation cost in Edmond, OK?</h3>'),
 ('<h3>How long does Contact take?</h3>', '<h3>How quickly will I hear back?</h3>'),
 ('<h3>How do I know if I need Contact?</h3>', '<h3>How do I know it is time to remodel?</h3>'),
 ('Ready to schedule Contact in Edmond, OK? Contact Edmond Bathroom Remodeling today', 'Ready to schedule a consultation in Edmond, OK? Contact Scissortail Bath today'),
 ('Edmond Bathroom Remodeling', 'Scissortail Bath'),
]
def copy_fixes(body, rel):
    if rel == 'contact.html':
        for a, b in CONTACT_COPY:
            n = a.subn(b, body) if hasattr(a, 'subn') else (body.replace(a, b), body.count(a))
            if n[1] == 0: raise SystemExit(f'contact copy fix not applied: {str(a)[:60]}')
            body = n[0]
    # template-junk alt text on the injected photos ("Bathroom remodeling — Shower Remodel")
    def alt(m):
        x = m.group(1)
        if rel.startswith('locations/'): return f'alt="Bathroom remodeling in {x}, OK"'
        if rel.startswith('services/'): return f'alt="{x} in Edmond, OK"'
        if rel == 'about.html': return 'alt="Walk-in tile shower with frameless glass"'
        return f'alt="Remodeled bathroom in Edmond, OK"'
    return re.sub(r'alt="Bathroom remodeling — ([^"]+)"', alt, body)


# ---------------------------------------------------------------- estimate/ (form page: brand, nav, phone sizing only; form untouched)
EST_CSS = """<style id="st-est">
.nav{gap:12px}.nav__logo{display:inline-flex;align-items:center;min-height:44px}.nav__links{display:flex;gap:4px;margin-left:auto}
.nav__links a{display:inline-flex;align-items:center;min-height:44px;padding:0 10px;border-radius:10px;color:#fff;font-size:.9rem;font-weight:600}
.nav__links a:hover{background:rgba(255,255,255,.1)}.nav__cta{display:inline-flex;align-items:center;min-height:44px}
.check-item input[type=checkbox]{-webkit-appearance:none;appearance:none;width:24px;min-width:24px;height:40px;margin:-10px 0;border-radius:0;
background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect x='1' y='1' width='18' height='18' rx='5' fill='white' stroke='%2394a3b8' stroke-width='1.5'/%3E%3C/svg%3E") center/20px no-repeat}
.check-item input[type=checkbox]:checked{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Crect x='.5' y='.5' width='19' height='19' rx='5' fill='%23e94560'/%3E%3Cpath d='M5.5 10.5l3 3 6-7' fill='none' stroke='white' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")}
.check-item input[type=checkbox]:focus-visible{outline:2px solid #e94560;outline-offset:2px}
.footer a{display:inline-flex;align-items:center;min-height:40px}
@media(max-width:640px){.nav{padding:8px 14px;flex-wrap:wrap;row-gap:0}.nav__links{order:3;width:100%;margin:0 -10px;justify-content:space-between}.nav__links a{padding:0 10px}.check-item span,.check-item label,label,.trust-item,.footer,.page-header p,.upload-zone p{font-size:15px}
.nav__logo{margin-right:auto}}
</style>
</head>"""
def estimate(root):
    f = os.path.join(root, 'estimate', 'index.html')
    if not os.path.exists(f): return
    h = open(f, encoding='utf-8').read()
    if 'id="st-est"' in h: print('estimate/index.html skip'); return
    form_before = re.search(r'<form.*?</form>', h, re.S).group(0)
    h = h.replace('</head>', EST_CSS, 1)
    h = h.replace('<div class="nav__logo">Bathroom <span>Pro</span></div>',
                  '<a href="/" class="nav__logo">Scissortail <span>Bath</span></a>\n  <div class="nav__links"><a href="/">Home</a><a href="/services/full-bathroom-remodel.html">Services</a><a href="/faq.html">FAQ</a><a href="/contact.html">Contact</a></div>', 1)
    h = h.replace('&copy; 2026 Bathroom Remodeling in Edmond, OK &nbsp;|', '&copy; 2026 Scissortail Bath &nbsp;|', 1)
    assert re.search(r'<form.*?</form>', h, re.S).group(0) == form_before, 'estimate form changed'
    open(f, 'w', encoding='utf-8').write(h); print('estimate/index.html ok (brand, nav, tap sizes)')

# ---------------------------------------------------------------- driver
def transform(path):
    html = open(path, encoding='utf-8').read()
    if re.search(r'<body[^>]*class="[^"]*\bst\b', html): return 'skip (already modern)'
    rel = os.path.relpath(path, ROOT)
    kind, active = kind_of(rel)
    head, body = html.split('<body', 1)
    head = head_swap(head)
    body = body.split('>', 1)[1]
    body = copy_fixes(body, rel)
    body = common_body(body, kind, active)
    if kind == 'home': body = home(body)
    elif kind == 'blogidx': body = blog_index(body)
    elif kind == 'post': body = blog_post(body, rel)
    elif kind in ('svc', 'loc', 'page', 'legal'): body = inner(body, rel, kind)
    elif kind == 'msg':
        body = re.sub(r'<svg class="ic"([^>]*)>(.*?)</svg>(?=\s*<h1>Thank You!</h1>)', r'<span class="msg-icon"><svg class="ic"\1>\2</svg></span>', body, count=1, flags=re.S)
        body = body.replace('class="btn btn--accent" style="margin-top:2rem"', 'class="btn"')
    body = faq_details(body)
    body = strip_styles(body)
    # the remaining CTA buttons inside bands
    body = body.replace('class="btn btn--accent"', 'class="btn"')
    body = body.replace('<script src="js/main.js" defer>', '<script src="/js/main.js" defer>')  # 404.html is served at any depth
    open(path, 'w', encoding='utf-8').write(head + f'<body class="st st-{kind}">' + body)
    return f'ok ({kind})'

SKIP = ('job/', 'lead', 'estimate/', '.git/', 'services/index.html', 'locations/index.html')
if __name__ == '__main__':
    for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith(SKIP): continue
        print(rel, transform(f))
    estimate(ROOT)
