import fitz  # PyMuPDF
from io import BytesIO

def create_pdf(text):
    """Create a properly styled PDF document from formatted text using PyMuPDF"""
    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # US Letter size
    
    # Define styles
    title_font = "helvB"  # Helvetica-Bold in PyMuPDF
    heading_font = "helvB"
    normal_font = "helv"
    
    title_size = 18
    heading_size = 14
    normal_size = 11
    
    black = (0, 0, 0)
    dark_gray = (0.3, 0.3, 0.3)
    accent_color = (0.2, 0.4, 0.6)  # Dark blue for headings
    
    # Margins
    left_margin = 72  # 1 inch
    right_margin = 72
    top_margin = 72
    bottom_margin = 72
    current_y = top_margin
    
    lines = text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            current_y += 5
            i += 1
            continue
        
        # If line is all caps or ends with :, treat as heading
        if line.isupper() or line.endswith(':'):
            if current_y > top_margin + 30:
                current_y += 15
            
            page.insert_text(
                (left_margin, current_y),
                line,
                fontname=heading_font,
                fontsize=heading_size,
                color=accent_color
            )
            current_y += heading_size + 5
            
            # Draw underline
            page.draw_line(
                (left_margin, current_y),
                (612 - right_margin, current_y),
                color=accent_color,
                width=1
            )
            current_y += 15
        
        # If line is near the top & followed by blank line — treat as title
        elif i < 3 and (i + 1 < len(lines) and not lines[i + 1].strip()):
            text_width = page.get_text_length(line, fontsize=title_size, fontname=title_font)
            page.insert_text(
                ((612 - text_width) / 2, current_y),
                line,
                fontname=title_font,
                fontsize=title_size,
                color=black
            )
            current_y += title_size + 15
        
        # Bullet points
        elif line.startswith(('•', '-', '*')):
            # Insert bullet with indentation
            page.insert_textbox(
                (left_margin + 15, current_y, 612 - right_margin, current_y + 50),
                line,
                fontname=normal_font,
                fontsize=normal_size,
                color=dark_gray,
                align=0
            )
            current_y += normal_size + 8
        
        # Normal text
        else:
            page.insert_textbox(
                (left_margin, current_y, 612 - right_margin, current_y + 50),
                line,
                fontname=normal_font,
                fontsize=normal_size,
                color=black,
                align=0
            )
            current_y += normal_size + 8
        
        if current_y > 792 - bottom_margin - 50:
            page = doc.new_page(width=612, height=792)
            current_y = top_margin
        
        i += 1
    
    output = BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)
    return output

