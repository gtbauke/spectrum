# Academic Review: Interface Web para Regressão Simbólica

> **Document type**: Trabalho de Conclusão de Curso (Monograph/Thesis)
> **Reviewed file(s)**: `symbolic_regression_web_interface.tex` e arquivos em `chapters/`
> **Review date**: 2026-05-05

## Executive Summary

O projeto "Interface Web para Regressão Simbólica" (Spectrum) apresenta uma solução muito robusta e bem arquitetada para um problema real na área de aprendizado de máquina: a dificuldade de explorar modelos de regressão simbólica. O texto demonstra maturidade técnica excepcional, especialmente na adoção dos princípios de *Domain-Driven Design* (DDD) e no desenvolvimento inovador da *Inference Query Language* (IQL).

O texto possui uma boa estrutura argumentativa e de organização. No entanto, há lacunas que precisam ser tratadas antes da submissão final, sendo a principal delas a ausência do capítulo de Resultados (que está comentado no código-fonte, mas é referenciado na introdução). Além disso, pequenos ajustes de formatação LaTeX e adequações às normas ABNT (como a nomenclatura de referências visuais) elevarão ainda mais o nível de profissionalismo do trabalho.

## Structure

### Strengths
- A organização dos capítulos segue uma progressão lógica excelente: introduz o problema, aprofunda a teoria subjacente (e-graphs, programação genética), justifica as escolhas arquiteturais (DDD) e culmina com as propostas práticas da plataforma e da linguagem de domínio (IQL).
- A separação em subseções para explicar o pipeline de execução da IQL (Tokenizer -> Parser -> Execução) torna o processo de compilação muito claro para o leitor.

### Suggestions
- **Capítulo de Resultados Ausente**: Na Introdução (linha 27), você afirma que "O capítulo 6 apresenta os resultados obtidos com a implementação da plataforma". Contudo, no arquivo principal (`symbolic_regression_web_interface.tex`, linha 220), o `\include{chapters/results}` está comentado, e a Conclusão acaba se tornando o Capítulo 6. A ausência de resultados impede que a eficácia da ferramenta seja comprovada na prática.
- **Listas em texto bruto**: No capítulo de Introdução (linhas 10-17) e na Revisão Bibliográfica (linhas 129-131), foram utilizadas listas com hifens (ex: `- Gerenciamento de pipelines...`) sem um ambiente LaTeX apropriado. O LaTeX não processará isso como uma lista indentada. **Ação recomendada**: envolva esses itens em um ambiente `\begin{itemize} ... \end{itemize}`.

## Writing

### Strengths
- O tom do texto é formal e perfeitamente adequado para uma monografia acadêmica.
- As explicações teóricas sobre regressão simbólica e *equality graphs* estão acessíveis e bem fundamentadas com literatura pertinente.

### Suggestions
- **Consistência de Termos em Inglês**: Os termos *front-end* e *back-end* são escritos de diversas formas ao longo do texto (ex: backend, back-end). É recomendável adotar uma única grafia (com hífen e em itálico, como `\textit{back-end}`).
- **Gênero de Termos Estrangeiros**: O texto utiliza "Profile" como um substantivo feminino ("uma Profile", "das Profiles"). Em português do Brasil, é mais comum o uso no masculino (o Profile, o perfil). Avalie se não seria melhor traduzir para "Perfil" ou adotar o gênero masculino para soar mais natural.
- **Erros gramaticais pontuais**:
  - `introduction.tex` (linha 6): "outras técnicas de IA... **tem** ganhado" $\rightarrow$ "**têm** ganhado" (o sujeito "técnicas" está no plural).
  - `platform.tex` (linha 34): "A interface em **blocs**" $\rightarrow$ "A interface em **blocos**".
  - `platform.tex` (linha 746): "web,o servidor" $\rightarrow$ "web, o servidor" (espaço faltando).
  - `methodology.tex` (linhas 204 e 206): Foi utilizado o comando `\text{back-end}` em modo de texto, que pertence ao pacote `amsmath` e é destinado a uso em equações matemáticas. Use `\textit{back-end}` ou formato de texto simples.

## Figures & Visualization

### Strengths
- Os diagramas gerados nativamente em TikZ (ex: o diagrama de entidades do banco de dados e o pipeline de execução IQL) demonstram enorme zelo pelo trabalho, tendo altíssima qualidade visual.
- Os trechos de código (Listings) estão bem formatados, com paletas de sintaxe que facilitam a leitura.

### Suggestions
- **Nomenclatura ABNT para Referências Visuais**: De acordo com a norma ABNT, toda referência a uma ilustração (seja um esquema, imagem ou gráfico) no corpo do texto deve usar a palavra "Figura", "Quadro" ou "Tabela". Em `platform.tex`, existem trechos como "A imagem \ref{...} apresenta..." e "O diagrama \ref{...}". Substitua todas as ocorrências de "imagem" ou "diagrama" referenciadas no texto por "Figura".
- **Legenda excessivamente prolixa**: Em `query_language.tex` (linha 241), a legenda da Figura da AST está com vocabulário muito artificial/inflado: *"Visualização gráfica representativa consolidada limitante da Árvore de Sintaxe Abstrata (AST) compilada sequencial e contígua pelas classes iterativas do modo de leitura descendente restrito..."*. **Ação recomendada**: simplifique para focar na clareza. Exemplo: *"Árvore de Sintaxe Abstrata (AST) correspondente à consulta IQL de exemplo, gerada pelo Pratt Parser."*
- **Árvore de Diretórios (dirtree)**: Em `methodology.tex` (linha 67), o `\dirtree` foi inserido diretamente no texto. Pode ser mais elegante colocá-lo dentro de um ambiente `figure` ou `quadro` com `\caption` e um `\label` para referenciá-lo formalmente no texto.

## Technical Presentation

### Strengths
- A analogia entre IQL e SQL é brilhante. A Tabela de comparação (Tabela 1.1 ou semelhante no seu documento) ajuda consideravelmente um leitor da área de Computação a compreender a DSL.
- A descrição de arquitetura, como a separação dos pacotes em `core`, `db_core`, etc. demonstra profundo conhecimento prático de engenharia de software e não apenas de IA.

### Suggestions
- **Validação Prática da Ferramenta**: Toda a base teórica e de engenharia foi explicada, porém falta a comprovação prática de que a integração ocorreu com sucesso e gerou valor. Isso reforça a urgência de redigir o capítulo de **Resultados**. Sem ele, o leitor não consegue avaliar a experiência real da interface nem o custo computacional remoto versus local proposto na justificativa.

## Priority Actions

Abaixo estão listadas as ações de maior impacto para refinar sua monografia, em ordem de importância:

1. **Escrever e descomentar o capítulo de Resultados (`chapters/results.tex`)**: Mostrar a plataforma em ação (telas da plataforma em funcionamento, resultados de um treinamento Eggp utilizando um dataset de exemplo no Spectrum, demonstração de streaming de consultas IQL). Isso cumpre os objetivos descritos no capítulo de introdução.
2. **Corrigir os ambientes de lista (`itemize`)**: Nas linhas 10 de `introduction.tex` e 129 de `literature_review.tex`, os hifens usados diretamente no texto não quebrarão a formatação LaTeX corretamente e poluem a diagramação.
3. **Revisar referências cruzadas das Figuras**: Padronizar as chamadas textuais ("A imagem \ref...", "O diagrama \ref...") para a norma ABNT ("A Figura \ref...").
4. **Padronizar e corrigir inconsistências léxicas**: Revisar os plurais com acento circunflexo (tem vs têm), unificar o padrão de escrita de *back-end*/*front-end*, e reescrever a legenda inflada na Figura do AST.

## Detailed Notes

| Arquivo | Localização | Problema | Sugestão |
|---|---|---|---|
| `introduction.tex` | L6 | "outras técnicas ... tem ganhado" | Alterar para "têm ganhado" |
| `introduction.tex` | L10 | Uso de hífen no texto plano para listas | Envolver em ambiente `\begin{itemize} \item ... \end{itemize}` |
| `platform.tex` | L34 | "... A interface em blocs ..." | Corrigir para "blocos" |
| `platform.tex` | L155 | Diagrama de arquitetura referenciado sem "Figura" | O texto diz "O diagrama \ref{fig:high_level}". Mudar para "A Figura \ref{...}" |
| `platform.tex` | L746 | "interface web,o servidor" | "interface web, o servidor" (Falta espaço) |
| `query_language.tex` | L241 | Legenda extremamente verbosa e artificial | Substituir por texto mais conciso e direto |
| `methodology.tex` | L204 | `\text{back-end}` fora de contexto matemático | Substituir por `\textit{back-end}` |
