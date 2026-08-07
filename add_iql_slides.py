from bs4 import BeautifulSoup

with open('presentation/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find slide 15
slide_15 = soup.find('section', {'data-slide': '15'})

# Create new slide 16
new_slide_16_html = """
    <!-- SLIDE 16: PIPELINE IQL -->
    <section class="slide" data-slide="16">
      <div class="slide-content">
        <h2>O Pipeline de Execução da IQL</h2>
        <p class="mb">A execução das consultas IQL roda em um interpretador e compilador próprio (Parser) construído do zero na plataforma:</p>
        <div class="box box-highlight">
          <ul class="spaced-list">
            <li><strong>Análise Léxica (Tokenização):</strong> Converte a consulta textual em tokens validando a sintaxe e a semântica de forma robusta.</li>
            <li><strong>Análise Sintática (Pratt Parser):</strong> Transforma os tokens em uma Árvore de Sintaxe Abstrata (AST) representativa da própria consulta do usuário.</li>
            <li><strong>Integração Nativa:</strong> O motor executa a AST compilada diretamente contra o <em>e-graph</em> carregado em memória, garantindo altíssimo desempenho na extração massiva.</li>
          </ul>
        </div>
      </div>
    </section>
"""
slide_16 = BeautifulSoup(new_slide_16_html, 'html.parser').section

# Create new slide 17
new_slide_17_html = """
    <!-- SLIDE 17: PATTERN MATCHING IQL -->
    <section class="slide" data-slide="17">
      <div class="slide-content">
        <h2>Casamento de Padrões (Pattern Matching)</h2>
        <div class="split">
          <div>
            <ul class="spaced-list">
              <li>O verdadeiro poder da IQL reside na sua integração com algoritmos de <em>Pattern Matching</em> aplicados em grafos.</li>
              <li>A diretiva <code>PATTERN IS LIKE</code> instrui o motor a varrer o e-graph procurando equações que respeitem um <strong>esqueleto matemático específico</strong> (ex: <code>sin(v0) * v1</code>).</li>
              <li>Garante que as expressões extraídas façam total sentido para as regras de negócio ou físicas do especialista, injetando conhecimento humano na filtragem.</li>
            </ul>
          </div>
          <div class="box box-highlight" style="display: flex; align-items: center; justify-content: center; padding: 2rem;">
            <p style="font-size: 1.3rem; line-height: 1.8; text-align: center;">"A capacidade de filtrar expressões que respeitem características estruturais pré-estabelecidas torna o processo alinhado aos conhecimentos prévios do especialista de domínio."</p>
          </div>
        </div>
      </div>
    </section>
"""
slide_17 = BeautifulSoup(new_slide_17_html, 'html.parser').section

# Insert after slide 15
slide_15.insert_after(slide_17)
slide_15.insert_after(slide_16)

# Update data-slide attributes for all slides
slides = soup.find_all('section', class_='slide')
for i, slide in enumerate(slides):
    slide['data-slide'] = str(i + 1)

# Update slide counter
counter = soup.find(id='slideCounter')
if counter:
    counter.string = f"1 / {len(slides)}"

with open('presentation/index.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Slides added successfully!")
