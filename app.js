/* ==========================================================================
   PRESENTATION CONTROLLER (RESPONSIVE + E-GRAPH INTERCEPT LOGIC)
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // Inicialização (Math e Ícones)
  if (window.lucide) window.lucide.createIcons();
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '\\(', right: '\\)', display: false }
      ],
      throwOnError: false
    });
  }

  // --- RESPONSIVIDADE ESTRITA VIA CSS TRANSFORM (SCALE) ---
  function resizeSlides() {
    const slidesContent = document.querySelectorAll('.slide-content');
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    // Canvas lógico base para todo o design (1200x800)
    const logicalWidth = 1200;
    const logicalHeight = 800;
    
    // Escala calculada mantendo a proporção 100% sem cortes
    const scale = Math.min(windowWidth / logicalWidth, windowHeight / logicalHeight) * 0.98;

    slidesContent.forEach(el => {
      el.style.transform = `scale(${scale})`;
      el.style.transformOrigin = 'center center';
    });
  }
  window.addEventListener('resize', resizeSlides);
  resizeSlides(); // Aplica imediatamente ao carregar

  // --- NAVEGAÇÃO DE SLIDES ---
  const slides = Array.from(document.querySelectorAll('.slide'));
  const totalSlides = slides.length;
  let currentSlideIndex = 0;
  const slideCounter = document.getElementById('slideCounter');

  function updateCounter() {
    if (slideCounter) slideCounter.textContent = `${currentSlideIndex + 1} / ${totalSlides}`;
  }

  function goToSlide(index) {
    if (index < 0) index = 0;
    if (index >= totalSlides) index = totalSlides - 1;
    slides[currentSlideIndex].classList.remove('active');
    currentSlideIndex = index;
    slides[currentSlideIndex].classList.add('active');
    updateCounter();
  }

  // --- LÓGICA DO COMPONENTE E-GRAPH ---
  const egBtns = Array.from(document.querySelectorAll('.eg-btn'));
  const egraphVisual = document.getElementById('egraphVisual');
  const egraphDesc = document.getElementById('egraphDesc');
  let currentEgraphStep = 0;

  const egDescriptions = [
    "<strong>1. Inclusão:</strong> Expressões como \\(x \\times 2\\) e \\(x + x\\) formam <em>e-classes</em> isoladas na primeira iteração.",
    "<strong>2. Reescrita:</strong> Pela regra matemática (\\(a \\times 2 = a + a\\)), identifica-se que ambas as classes são equivalentes.",
    "<strong>3. Saturação (União):</strong> As duas <em>e-classes</em> são unidas. Agora, uma única classe engloba os dois <em>e-nodes</em> representando a equivalência.",
    "<strong>4. Extração:</strong> Ao avaliar a melhor expressão, a operação de multiplicação (\\(\\times\\)) é extraída como a solução ótima e parcimoniosa."
  ];

  function setEgraphStep(idx) {
    if (!egraphVisual) return;
    currentEgraphStep = idx;
    
    egBtns.forEach((btn, i) => {
      if (btn) btn.classList.toggle('active', i === idx);
    });

    egraphVisual.className = `egraph-visual step-${idx + 1} mt`;
    
    if(egraphDesc) {
      egraphDesc.innerHTML = egDescriptions[idx];
      // Force KaTeX to parse the newly inserted text
      if (window.renderMathInElement) {
        window.renderMathInElement(egraphDesc, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false
        });
      }
    }
  }

  egBtns.forEach((btn, idx) => {
    if (btn) btn.addEventListener('click', () => setEgraphStep(idx));
  });

  // --- LÓGICA DO COMPONENTE ALGORITMO GENÉTICO ---
  const gaBtns = Array.from(document.querySelectorAll('.ga-btn'));
  const gaVisual = document.getElementById('gaVisual');
  const gaDesc = document.getElementById('gaDesc');
  let currentGaStep = 0;

  const gaDescriptions = [
    "<strong>1. População Inicial:</strong> Um conjunto de árvores sintáticas aleatórias é instanciado. O algoritmo avalia a aptidão (ex: erro MSE) de cada indivíduo da geração.",
    "<strong>2. Seleção:</strong> Indivíduos com menor erro ou maior parcimônia (como \\(x + 1\\) e \\(x^2\\)) são selecionados pelo método de torneio para reprodução.",
    "<strong>3. Reprodução (Cruzamento/Mutação):</strong> Subárvores selecionadas sofrem cruzamento (troca de ramos) ou mutação probabilística de nós isolados para gerar descendentes.",
    "<strong>4. Nova Geração:</strong> Os melhores indivíduos são mantidos (elitismo) e os novos descendentes substituem os inaptos, elevando a aptidão geral da população."
  ];

  function setGaStep(idx) {
    if (!gaVisual) return;
    currentGaStep = idx;
    
    gaBtns.forEach((btn, i) => {
      if (btn) btn.classList.toggle('active', i === idx);
    });

    gaVisual.className = `ga-visual step-${idx + 1} mt`;
    
    if(gaDesc) {
      gaDesc.innerHTML = gaDescriptions[idx];
      if (window.renderMathInElement) {
        window.renderMathInElement(gaDesc, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false
        });
      }
    }
  }

  gaBtns.forEach((btn, idx) => {
    if (btn) btn.addEventListener('click', () => setGaStep(idx));
  });

  // --- CONTROLES DE TECLADO INTELIGENTES ---
  document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    // Detecta se o slide atual possui a interatividade de E-graph ou GA
    const currentSlideEl = slides[currentSlideIndex];
    const isEgraphSlide = currentSlideEl.querySelector('.egraph-interactive-container') !== null;
    const isGaSlide = currentSlideEl.querySelector('.ga-interactive-container') !== null;

    if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      
      if (isEgraphSlide && currentEgraphStep < 3) {
        setEgraphStep(currentEgraphStep + 1);
      } else if (isGaSlide && currentGaStep < 3) {
        setGaStep(currentGaStep + 1);
      } else {
        goToSlide(currentSlideIndex + 1);
      }
      
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp' || e.key === 'Backspace') {
      e.preventDefault();
      
      if (isEgraphSlide && currentEgraphStep > 0) {
        setEgraphStep(currentEgraphStep - 1);
      } else if (isGaSlide && currentGaStep > 0) {
        setGaStep(currentGaStep - 1);
      } else {
        goToSlide(currentSlideIndex - 1);
      }
      
    } else if (e.key === 'Home') {
      e.preventDefault();
      goToSlide(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      goToSlide(totalSlides - 1);
    }
  });

  // Controles de Toque (Mobile/Tablet Swipe)
  let touchStartX = 0;
  document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    let touchEndX = e.changedTouches[0].screenX;
    const threshold = 50;
    const currentSlideEl = slides[currentSlideIndex];
    const isEgraphSlide = currentSlideEl.querySelector('.egraph-interactive-container') !== null;
    const isGaSlide = currentSlideEl.querySelector('.ga-interactive-container') !== null;

    if (touchEndX < touchStartX - threshold) {
      if (isEgraphSlide && currentEgraphStep < 3) setEgraphStep(currentEgraphStep + 1);
      else if (isGaSlide && currentGaStep < 3) setGaStep(currentGaStep + 1);
      else goToSlide(currentSlideIndex + 1);
    } else if (touchEndX > touchStartX + threshold) {
      if (isEgraphSlide && currentEgraphStep > 0) setEgraphStep(currentEgraphStep - 1);
      else if (isGaSlide && currentGaStep > 0) setGaStep(currentGaStep - 1);
      else goToSlide(currentSlideIndex - 1);
    }
  }, { passive: true });

  // Iniciar Contador
  updateCounter();
});
