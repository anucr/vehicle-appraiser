import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf():
    pdf_filename = "vehicle_appraiser_tech_stack.pdf"
    
    # Page setup
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Modern professional typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=20
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0D9488"),
        spaceBefore=14,
        spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )
    
    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#2D3748")
    )
    
    table_body_bold_style = ParagraphStyle(
        'TableBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1A365D")
    )

    story = []
    
    # Title Header Block
    story.append(Paragraph("🇱🇰 Sri Lankan Vehicle Appraiser", title_style))
    story.append(Paragraph("System Architecture & Tech Stack Reference Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#CBD5E1"), spaceAfter=15))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", h1_style))
    summary_text = (
        "The <b>Sri Lankan Vehicle Appraiser</b> is a localized, data-driven valuation and analytics platform. "
        "It replaces static guesswork with real-time secondary market intelligence by combining automated web scraping "
        "pipelines with dynamic statistical processing. The system evaluates asset worth, adjusts for mileage "
        "and age depreciation factor adjustments relative to regional peer data clusters, and renders interactive reports."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 5))
    
    # Core Architecture & Layers
    story.append(Paragraph("1. System Architecture Layers", h1_style))
    
    layers = [
        ("User Interface Layer (Frontend)", "Provides a highly interactive, responsive dashboard built using <b>Streamlit</b> for inputting vehicle specs, launching dynamic valuation queries, and inspecting statistical reports."),
        ("Data Scraping & Mining Layer (Ingestion)", "Employs <b>Playwright</b> for dynamic, browser-rendered listing extractions, alongside a multi-page static crawler using <b>BeautifulSoup4</b> & <b>Requests</b> (featuring polite 2-second delays for rate-limit protection)."),
        ("Data Cleaning & Engineering Layer", "Uses <b>Pandas</b> dataframes combined with python <b>Regular Expressions (re)</b> to parse unformatted price tags (e.g. <i>'Rs. 8,750,000'</i>) and mileage strings (e.g. <i>'165,000 km'</i>) into numeric structures."),
        ("Analytics & Modeling Layer (Statistical Engine)", "Leverages <b>NumPy</b> to compute peer-group averages and bounds (20th percentile budget floor and 80th percentile premium ceiling), adjusting value dynamically according to mileage deviation from cluster averages."),
        ("Persistence & Storage Layer", "Utilizes local structured file storage including <b>.xlsx</b> (for broad historical indexes), <b>.csv</b> (actively compiled outputs), and <b>.json</b> (cached market rates and model-specific annual depreciation ratios).")
    ]
    
    for layer_title, desc in layers:
        bullet_text = f"&bull; <b>{layer_title}:</b> {desc}"
        story.append(Paragraph(bullet_text, bullet_style))
        
    story.append(Spacer(1, 10))
    
    # Technology Stack Table
    story.append(Paragraph("2. Detailed Technology Component Inventory", h1_style))
    
    # Table headers
    table_data = [
        [Paragraph("Component", table_header_style), Paragraph("Technology / Lib", table_header_style), Paragraph("Role / Usage in Project", table_header_style)]
    ]
    
    # Table rows
    components = [
        ("Frontend UI", "Streamlit", "Constructs interactive web app dashboard, tables, controls, and report display cards."),
        ("Dynamic Scraping", "Playwright", "Launches headless Chromium instances to fetch active, client-rendered listing elements."),
        ("Static Scraping", "BeautifulSoup4 / Requests", "Downloads and parses HTML indexes across paginated marketplace sections."),
        ("Data Engineering", "Pandas", "Cleans raw spreadsheets, renames columns, drops NaNs, and handles filtering."),
        ("Data Extraction", "Regex (re)", "Parses price digits and mileage text labels (e.g. 'Rs. 8.75M' or '165,000 km')."),
        ("Statistical Modeling", "NumPy", "Calculates mean rates, 20% budget floor, 80% premium ceiling, and user mile-variance bounds."),
        ("Data Caching", "JSON / CSV", "Stores baseline configurations, depreciation matrices, and extracted listings records.")
    ]
    
    for comp, tech, role in components:
        table_data.append([
            Paragraph(comp, table_body_bold_style),
            Paragraph(tech, table_body_style),
            Paragraph(role, table_body_style)
        ])
        
    # Table Column Widths: 504 points total (matching letter width 612 - 108 margins)
    col_widths = [100, 110, 294]
    
    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#F7FAFC"), colors.HexColor("#EDF2F7")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    story.append(t)
    
    # Document compilation
    doc.build(story)
    print(f"Successfully generated {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
