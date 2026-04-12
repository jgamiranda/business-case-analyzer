from fpdf import FPDF

pdf = FPDF(orientation='L', unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)
pdf.add_page()

W, H = 297, 210

# --- TITLE ---
pdf.set_font('Helvetica', 'B', 16)
pdf.set_xy(0, 8)
pdf.cell(W, 10, 'Corpet MVP | Team Org Chart', align='C')
pdf.set_font('Helvetica', '', 9)
pdf.set_xy(0, 17)
pdf.cell(W, 5, 'April 2026 | Streamlit MVP | 3 Agents + Coordinator', align='C')


def box(x, y, w, h, title, lines, color=(230, 240, 255), border_color=(26, 86, 219)):
    pdf.set_fill_color(*color)
    pdf.set_draw_color(*border_color)
    pdf.set_line_width(0.6)
    pdf.rect(x, y, w, h, style='DF')
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(x, y + 2)
    pdf.cell(w, 5, title, align='C')
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(60, 60, 60)
    for i, line in enumerate(lines):
        pdf.set_xy(x + 3, y + 9 + i * 4)
        pdf.cell(w - 6, 4, line, align='L')


def arrow_down(x1, y1, x2, y2):
    pdf.set_draw_color(100, 100, 100)
    pdf.set_line_width(0.4)
    pdf.line(x1, y1, x2, y2)
    pdf.line(x2 - 2, y2 - 3, x2, y2)
    pdf.line(x2 + 2, y2 - 3, x2, y2)


def dashed_line(x1, y1, x2, y2):
    pdf.set_draw_color(150, 150, 150)
    pdf.set_line_width(0.3)
    pdf.set_dash_pattern(dash=2, gap=1.5)
    pdf.line(x1, y1, x2, y2)
    pdf.set_dash_pattern(dash=0, gap=0)


# ===== COORDINATOR (top) =====
box(108, 28, 80, 28,
    'Coordinator (User)',
    ['Role: Product owner, final decisions',
     'Invokes agents via /slash commands',
     'Reviews diffs, approves commits'],
    color=(255, 243, 205), border_color=(180, 140, 20))

# ===== 3 AGENTS (middle row) =====
# Boobinho
box(10, 80, 82, 45,
    '/boobinho (Research)',
    ['Role: Knowledge base curator',
     'Owns: boobinho_knowledge_base.json',
     '       boobinho/ (research, summaries)',
     'KB: v13.1, 162 topics, 18 sections',
     'Skills: formulas, benchmarks, specs',
     'Does NOT write code or UI',
     'Passes specs to other agents'],
    color=(220, 237, 254), border_color=(26, 86, 219))

# Zedobackend
box(108, 80, 82, 45,
    '/zedobackend (Backend)',
    ['Role: Calculation engine',
     'Owns: backend.py, pf_models.py,',
     '       minutes_generator.py, slides.py,',
     '       constants.py, pf_export.py',
     'Skills: IRR, WACC, DSCR, Monte Carlo',
     'Pure Python functions (no UI)',
     'Reusable for future migration'],
    color=(220, 254, 230), border_color=(22, 163, 74))

# Zedofrontend
box(206, 80, 82, 45,
    '/zedofrontend (Frontend)',
    ['Role: UI/UX specialist',
     'Owns: app.py (CSS/layout),',
     '       pages/*.py (presentation),',
     '       _design_tokens.py',
     'Skills: Streamlit, Plotly, i18n,',
     '        dark mode, responsive layout',
     'Post-MVP: migration to React.js'],
    color=(254, 226, 226), border_color=(220, 38, 38))

# ===== ARROWS from coordinator to agents =====
arrow_down(130, 56, 51, 80)
arrow_down(148, 56, 148, 80)
arrow_down(166, 56, 247, 80)

# ===== SHARED ENVIRONMENT (bottom — single rounded box) =====
pdf.set_fill_color(245, 245, 245)
pdf.set_draw_color(120, 120, 120)
pdf.set_line_width(0.6)
pdf.rect(35, 145, 228, 48, style='DF')

pdf.set_font('Helvetica', 'B', 11)
pdf.set_text_color(0, 0, 0)
pdf.set_xy(35, 147)
pdf.cell(228, 5, 'Git Repository (master)', align='C')

pdf.set_font('Helvetica', '', 7.5)
pdf.set_text_color(60, 60, 60)

# Left column — shared docs
col1_x = 42
col1_y = 155
col1 = [
    'Shared Documents:',
    '  COORDINATION.md - async channel',
    '  CLAUDE.md - token efficiency rules',
    '  translations.py - i18n PT/EN',
    '  requirements.txt - dependencies',
    '  .claude/commands/*.md - agent defs',
]
for i, line in enumerate(col1):
    if i == 0:
        pdf.set_font('Helvetica', 'B', 7.5)
    else:
        pdf.set_font('Helvetica', '', 7.5)
    pdf.set_xy(col1_x, col1_y + i * 4)
    pdf.cell(100, 4, line, align='L')

# Right column — app structure
col2_x = 165
col2_y = 155
col2 = [
    'Application (7 pages):',
    '  01 Business Case  |  05 Startup',
    '  02 M&A            |  06 Hedging',
    '  03 Project Finance |  07 LBO',
    '  04 Valuation DCF',
    'Stack: Python + Streamlit + Plotly',
]
for i, line in enumerate(col2):
    if i == 0:
        pdf.set_font('Helvetica', 'B', 7.5)
    else:
        pdf.set_font('Helvetica', '', 7.5)
    pdf.set_xy(col2_x, col2_y + i * 4)
    pdf.cell(90, 4, line, align='L')

# ===== ARROWS from agents to shared env =====
dashed_line(51, 125, 80, 145)
dashed_line(148, 125, 148, 145)
dashed_line(247, 125, 215, 145)

# ===== FLOW LABELS =====
pdf.set_font('Helvetica', 'I', 7)
pdf.set_text_color(100, 100, 100)

pdf.set_xy(12, 130)
pdf.cell(60, 4, 'writes KB, specs, research', align='C')
pdf.set_xy(118, 130)
pdf.cell(60, 4, 'writes backend.py, models', align='C')
pdf.set_xy(215, 130)
pdf.cell(60, 4, 'writes pages/*.py, CSS', align='C')

# horizontal dashed lines between agents (collaboration)
pdf.set_draw_color(26, 86, 219)
pdf.set_line_width(0.3)
pdf.set_dash_pattern(dash=1.5, gap=1.5)
pdf.line(92, 102, 108, 102)
pdf.line(190, 102, 206, 102)
pdf.set_dash_pattern(dash=0, gap=0)

pdf.set_font('Helvetica', 'I', 6)
pdf.set_text_color(26, 86, 219)
pdf.set_xy(88, 96)
pdf.cell(24, 4, 'specs', align='C')
pdf.set_xy(186, 96)
pdf.cell(24, 4, 'calc API', align='C')

# ===== FOOTER =====
pdf.set_font('Helvetica', '', 7)
pdf.set_text_color(150, 150, 150)
pdf.set_xy(0, 198)
pdf.cell(W, 4, 'Generated by /boobinho | business-case-analyzer | April 2026', align='C')

out = r'C:\Users\jgrac\Desktop\business-case-analyzer\boobinho\team_orgchart.pdf'
pdf.output(out)
print(f'OK: {out}')
