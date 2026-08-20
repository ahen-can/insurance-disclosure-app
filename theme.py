"""Shared look and feel.

Three brand colours, used consistently: FD5108 for anything actionable, FE7C39
for accents and highlights, B5BCC4 for structure and secondary text.
"""

from nicegui import ui

ORANGE = "#FD5108"        # primary actions
ORANGE_LIGHT = "#FE7C39"  # accents, hover, highlights
GREY = "#B5BCC4"          # borders, muted text
INK = "#2B2F33"           # body text
PAPER = "#FFFFFF"
CANVAS = "#F7F8F9"


def apply():
    """Set the palette and page-wide styles. Call once per page."""
    ui.colors(primary=ORANGE, secondary=ORANGE_LIGHT, accent=ORANGE_LIGHT)
    ui.add_head_html(f"""
    <style>
      body {{ background: {CANVAS}; color: {INK};
              font-family: Inter, -apple-system, "Segoe UI", Roboto, sans-serif; }}
      .brand-title {{ font-weight: 700; letter-spacing: -0.02em; color: {ORANGE}; }}
      .panel {{ background: {PAPER}; border: 1px solid {GREY}55; border-radius: 10px; }}
      .step {{ color: {INK}; font-size: 13px; line-height: 1.5; }}
      .step-num {{ background: {ORANGE_LIGHT}; color: white; border-radius: 50%;
                   width: 20px; height: 20px; display: inline-flex;
                   align-items: center; justify-content: center;
                   font-size: 11px; font-weight: 700; flex: none; }}
      .muted {{ color: {GREY}; font-size: 12px; }}
      .sheet-name {{ font-weight: 600; color: {INK}; font-size: 14px; }}
      .datagrid {{ border-collapse: collapse; font-size: 12px; width: max-content; }}
      .datagrid th {{ background: {ORANGE}10; color: {INK}; font-weight: 600;
                      text-align: left; padding: 5px 10px;
                      border: 1px solid {GREY}55; white-space: nowrap; }}
      .datagrid td {{ padding: 5px 10px; border: 1px solid {GREY}55;
                      white-space: nowrap; }}
      .scroll-x {{ overflow-x: auto; max-width: 100%; }}
    </style>
    """)
