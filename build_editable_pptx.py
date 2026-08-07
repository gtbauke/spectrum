import asyncio
from playwright.async_api import async_playwright
from pptx import Presentation
from pptx.util import Inches, Pt
from bs4 import BeautifulSoup
import os
import re

async def capture_interactive_steps():
    # Captures screenshots of only the visual elements of interactive slides
    steps = {'ga': [], 'egraph': []}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        file_path = f"file://{os.path.abspath('presentation/index.html')}"
        await page.goto(file_path)
        await page.wait_for_timeout(2000)
        
        # Go to slide 4 (GA) - Index 3
        for _ in range(3):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(300)
            
        for step in range(4):
            path = f"/tmp/ga_step_{step+1}.png"
            await page.locator('.ga-canvas').screenshot(path=path)
            steps['ga'].append(path)
            if step < 3:
                await page.keyboard.press("ArrowRight")
                await page.wait_for_timeout(600)
                
        # Go to slide 12 (E-graph) - from 8 to 12 is 4 presses
        for _ in range(4):
            await page.keyboard.press("ArrowRight")
            await page.wait_for_timeout(300)
            
        for step in range(4):
            path = f"/tmp/egraph_step_{step+1}.png"
            await page.locator('.egraph-canvas').screenshot(path=path)
            steps['egraph'].append(path)
            if step < 3:
                await page.keyboard.press("ArrowRight")
                await page.wait_for_timeout(600)
                
        await browser.close()
    return steps

def clean_text(html_text):
    if not html_text: return ""
    text = re.sub(r'\s+', ' ', html_text)
    text = text.replace('\\(', '').replace('\\)', '')
    return text.strip()

def build_pptx(ga_images, egraph_images):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    with open('presentation/index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
    slides = soup.find_all('section', class_='slide')
    
    # Textos do GA e Egraph (from app.js logic)
    ga_texts = [
        "1. População Inicial: Um conjunto de indivíduos contendo árvores sintáticas (AST) é inicializado e sua aptidão de validação avaliada (ex. MSE).",
        "2. Seleção: Os indivíduos que apresentam os melhores resultados de aptidão e menor número de nós (parcimônia) são selecionados para cruzamento.",
        "3. Reprodução: As ramificações selecionadas sofrem operações genéticas (Cruzamento de nós estruturais ou Mutação probabilística).",
        "4. Nova Geração: Pela estratégia de Elitismo, parcelas altamente viáveis são preservadas, enquanto as novas descendências substituem o restante populacional."
    ]
    
    eg_texts = [
        "1. Inclusão: Expressões matemáticas base como x * 2 e x + x são instanciadas, formando e-classes independentes.",
        "2. Reescrita: As regras de reescrita são aplicadas, conectando e-classes distintas com base em equivalências matemáticas (ex. a * 2 = a + a).",
        "3. Saturação de Igualdade: As equivalências sofrem fusão, englobando os e-nodes em uma única estrutura representacional.",
        "4. Extração: Durante a inferência, a árvore sintática é inspecionada para retornar a rota representacional mais parcimoniosa do grafo."
    ]
    
    for idx, slide_html in enumerate(slides):
        title_el = slide_html.find(['h1', 'h2'])
        title_text = clean_text(title_el.get_text()) if title_el else f"Slide {idx+1}"
        
        # Check if interactive GA
        if slide_html.find('div', class_='ga-interactive-container'):
            for step in range(4):
                slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title only
                slide.shapes.title.text = f"{title_text} - Etapa {step+1}"
                
                # Add text box
                txBox = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(1))
                tf = txBox.text_frame
                tf.word_wrap = True
                p = tf.add_paragraph()
                p.text = ga_texts[step]
                p.font.size = Pt(24)
                
                # Add image
                slide.shapes.add_picture(ga_images[step], Inches(2.5), Inches(3), width=Inches(8))
            continue
            
        # Check if interactive Egraph
        if slide_html.find('div', class_='egraph-interactive-container'):
            for step in range(4):
                slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title only
                slide.shapes.title.text = f"{title_text} - Etapa {step+1}"
                
                # Add text box
                txBox = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11), Inches(1))
                tf = txBox.text_frame
                tf.word_wrap = True
                p = tf.add_paragraph()
                p.text = eg_texts[step]
                p.font.size = Pt(24)
                
                # Add image
                slide.shapes.add_picture(egraph_images[step], Inches(2.5), Inches(3), width=Inches(8))
            continue
            
        # Normal Slide
        layout = prs.slide_layouts[1] # Title and Content
        slide = prs.slides.add_slide(layout)
        if slide.shapes.title:
            slide.shapes.title.text = title_text
            
        content_shape = slide.placeholders[1]
        tf = content_shape.text_frame
        tf.clear()
        
        # Find paragraphs, lists, and images
        elements = slide_html.find_all(['p', 'li', 'img', 'pre'])
        for el in elements:
            if el.name in ['p', 'li', 'pre']:
                text = clean_text(el.get_text())
                if text:
                    p = tf.add_paragraph()
                    p.text = text
                    p.level = 1 if el.name == 'li' else 0
                    p.font.size = Pt(20) if el.name == 'li' else Pt(22)
            elif el.name == 'img':
                img_src = el.get('src')
                if img_src and not img_src.startswith('http'):
                    img_path = os.path.join('presentation', img_src)
                    if os.path.exists(img_path):
                        # Add picture logic, placing it approximately
                        try:
                            slide.shapes.add_picture(img_path, Inches(7), Inches(2), width=Inches(5))
                        except Exception as e:
                            print(f"Error adding image {img_path}: {e}")

    output_path = os.path.abspath('presentation/Apresentacao_Spectrum_Editavel.pptx')
    prs.save(output_path)
    print(f"Done! Editable PPTX saved at {output_path}")

async def run():
    print("Capturing interactive steps...")
    steps = await capture_interactive_steps()
    print("Building PPTX...")
    build_pptx(steps['ga'], steps['egraph'])

if __name__ == "__main__":
    asyncio.run(run())
