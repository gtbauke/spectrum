# Spectrum: Interface Web para Regressão Simbólica - Defesa de TCC

Esta é uma apresentação web interativa de altíssima qualidade (State-of-the-Art) criada puramente em HTML5, CSS3 e JavaScript para a sua defesa de TCC na UFABC. Ela é *self-contained*, não requer instalação de pacotes npm, e utiliza CDNs para renderização de fórmulas matemáticas (KaTeX), syntax highlighting (Prism), ícones (Lucide) e gráficos interativos (Chart.js).

## 🚀 Como Executar

Você pode visualizar a apresentação de várias formas:

### Opção 1: Via Navegador (Recomendado para visualização rápida)
Basta abrir o arquivo `index.html` diretamente em qualquer navegador moderno (Chrome, Edge, Firefox, Safari). O carregamento é instantâneo.

### Opção 2: Servidor Local (Recomendado para apresentação ao vivo)
Para evitar bloqueios de CORS (caso ocorram) e ter uma experiência perfeita, você pode rodar um servidor local utilizando Python (que já está instalado no seu ambiente):
```bash
cd /home/gusta/dev/spectrum/presentation/
python3 -m http.server 8000
```
Em seguida, acesse `http://localhost:8000` no seu navegador.

## ⌨️ Teclas de Atalho (Navegação & Controles)

A apresentação conta com um robusto sistema de navegação por teclado para facilitar sua defesa:

* **Seta para Direita (`→`) / Espaço / PageDown:** Próximo slide
* **Seta para Esquerda (`←`) / Backspace / PageUp:** Slide anterior
* **Home / End:** Ir para o primeiro / último slide
* **`O` ou `ESC`:** Abre a **Visão Geral (Overview Grid)**. Permite que você ou a banca selecionem visualmente um slide específico.
* **`S`:** Abre o painel de **Notas do Palestrante (Speaker Notes)**. Excelente para você ler seu roteiro enquanto apresenta.
* **`F`:** Ativa o modo de **Tela Cheia (Fullscreen)**.

*Nota para Tablet/iPad:* Suporta gestos de *Swipe* para esquerda/direita.

## 🖨️ Como Exportar para PDF

Se a UFABC ou os membros da banca exigirem o arquivo `.pdf` da apresentação:
1. Abra a apresentação no navegador (de preferência Google Chrome ou Edge).
2. Pressione `Ctrl + P` (ou `Cmd + P` no Mac) para abrir a caixa de impressão.
3. Nas opções, selecione **Destino:** "Salvar como PDF".
4. Verifique se o tamanho do papel está como **A4 ou Paisagem** e as "Margens" estão como "Nenhuma".
5. A folha de estilo customizada (Print CSS) será ativada, formatando a apresentação limpa, slide a slide, removendo a barra de progresso e preparando-a para PDF.

## 📊 Gráfico de Pareto Interativo (Slide 12)
O slide 12 implementa o *Chart.js* comparando a escala logarítmica do Erro Quadrático Médio (MSE) entre os três cenários com a complexidade e precisão alcançadas pelo **eggp**. Basta passar o mouse por cima das barras para ver o *tooltip* dinâmico com a métrica exata.

Muito sucesso na sua defesa! A apresentação foi arquitetada para impressionar a banca visualmente enquanto destaca a alta engenharia e abstração matemática (IQL e e-graphs) do seu TCC.
