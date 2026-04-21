# LaTeX Patterns Reference

Common LaTeX environments, formatting commands, and convention-specific patterns
for academic documents.

## Table of Contents

1. [Document Class (abnTeX2)](#document-class-abntex2)
2. [ABNT Conventions](#abnt-conventions)
3. [Float Management](#float-management)
4. [Code Listings](#code-listings)
5. [Math Environments](#math-environments)
6. [Cross-References](#cross-references)
7. [BibTeX Patterns](#bibtex-patterns)
8. [Common Packages](#common-packages)
9. [Debugging Tips](#debugging-tips)

---

## Document Class (abnTeX2)

```latex
\documentclass[12pt, oneside, a4paper, chapter=TITLE, english, brazil]{abntex2}
```

Key commands:
- `\titulo{}`, `\autor{}`, `\orientador{}`, `\instituicao{}`
- `\imprimircapa`, `\imprimirfolhaderosto`
- `\begin{resumo}...\end{resumo}` for abstracts
- `\textual` marks the start of body content
- `\printbibliography` or `\bibliography{}` for references

---

## ABNT Conventions

### Caption placement

In ABNT NBR 14724, figure and table captions go **above** the content:

```latex
\begin{figure}[htbp]
    \caption{Descriptive caption text}  % ABOVE the image
    \centering
    \includegraphics[width=0.8\textwidth]{images/name.png}
    \label{fig:name}
\end{figure}
```

For tables:
```latex
\begin{table}[htbp]
    \caption{Descriptive table caption}  % ABOVE the table
    \centering
    \begin{tabular}{lcc}
        \toprule
        ...
    \end{tabular}
    \label{tab:name}
\end{table>
```

If the project uses `\fonte{}` (source attribution, common in ABNT), place it below:

```latex
\begin{figure}[htbp]
    \caption{Caption text}
    \centering
    \includegraphics[width=0.8\textwidth]{images/example.png}
    \fonte{Elaborated by the author.}
    \label{fig:example}
\end{figure}
```

### List environments

Always use proper LaTeX list environments, never raw dashes:

```latex
% WRONG
- Item one
- Item two

% RIGHT
\begin{itemize}
    \item Item one
    \item Item two
\end{itemize}
```

For numbered lists:
```latex
\begin{enumerate}
    \item First item
    \item Second item
\end{enumerate}
```

### Section hierarchy (abnTeX2)

```latex
\chapter{Chapter Title}       % \chapter only in book/report/abntex2
\section{Section Title}
\subsection{Subsection Title}
\subsubsection{Subsubsection Title}
```

### Foreign terms

Italicize foreign terms on first use:

```latex
\textit{software}    % English term in Portuguese text
\textit{e-graph}     % Technical English term
```

After first use with italics, subsequent uses can drop the formatting (though
consistency is preferred in many Brazilian institutions).

---

## Float Management

Floats (figures, tables) in LaTeX often drift from where you placed them. Control
this with placement specifiers:

```latex
\begin{figure}[htbp]  % h=here, t=top, b=bottom, p=float page
```

- Always use `[htbp]` unless you have a specific reason not to
- If a float drifts too far, add `\FloatBarrier` (from `placeins` package) before
  the float to force pending floats to be placed
- Use `\clearpage` to force all pending floats out before starting a new section

### Reference before appearance

Always reference a float before it appears in the text:

```latex
A Tabela \ref{tab:comparison} apresenta uma comparação...

\begin{table}[htbp]
    \caption{...}
    ...
    \label{tab:comparison}
\end{table}
```

---

## Code Listings

### Using lstlisting

```latex
\begin{lstlisting}[
    language=Python,
    caption={Descriptive caption},
    label={code:identifier},
    style=code_style  % if a style is defined in the project
]
class Example:
    def __init__(self):
        self.value = 42
\end{lstlisting}
```

### Using minted (if available)

```latex
\begin{minted}[
    linenos,
    frame=lines,
    fontsize=\small
]{python}
class Example:
    def __init__(self):
        self.value = 42
\end{minted}
```

### Inline code

```latex
\texttt{variable\_name}   % Note: escape underscores in normal text
\lstinline|variable_name|  % lstlisting inline (no need to escape)
```

---

## Math Environments

### Inline math

```latex
The expression $f(x) = \log(x/2) + 3x$ represents...
```

### Display math (unnumbered)

```latex
\[
    f(x) = \sum_{i=1}^{n} w_i \cdot x_i + b
\]
```

### Display math (numbered)

```latex
\begin{equation}
    \text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2
    \label{eq:mse}
\end{equation}
```

### Aligned equations

```latex
\begin{align}
    \text{fitness}(e) &= 1 - R^2(e) \label{eq:fitness} \\
    R^2(e) &= 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}
    \label{eq:r_squared}
\end{align}
```

---

## Cross-References

### Label naming conventions

```latex
\label{ch:introduction}      % chapters
\label{sec:methodology}      % sections
\label{subsec:datasets}      % subsections
\label{fig:architecture}     % figures
\label{tab:comparison}        % tables
\label{code:user_domain}      % code listings
\label{eq:mse}                % equations
```

### Referencing

```latex
% In Portuguese (ABNT)
O Capítulo \ref{ch:introduction} apresenta...
A Seção \ref{sec:methodology} descreve...
A Figura \ref{fig:architecture} ilustra...
A Tabela \ref{tab:comparison} compara...
O Código \ref{code:user_domain} mostra...
A Equação \ref{eq:mse} define...

% In English
Chapter \ref{ch:introduction} presents...
Section \ref{sec:methodology} describes...
Figure \ref{fig:architecture} illustrates...
Table \ref{tab:comparison} compares...
Listing \ref{code:user_domain} shows...
Equation \ref{eq:mse} defines...
```

---

## BibTeX Patterns

### Article (journal paper)

```bibtex
@article{koza1994genetic,
  author  = {Koza, John R.},
  title   = {Genetic Programming as a Means for Programming Computers by Natural Selection},
  journal = {Statistics and Computing},
  year    = {1994},
  volume  = {4},
  number  = {2},
  pages   = {87--112},
  doi     = {10.1007/BF00175355}
}
```

### Conference paper (inproceedings)

```bibtex
@inproceedings{de2024reducing,
  author    = {de Fran\c{c}a, Fabr\'{i}cio Olivetti},
  title     = {Reducing Redundancy with Equality Graphs},
  booktitle = {Proceedings of the GECCO Conference},
  year      = {2024},
  pages     = {100--108},
  publisher = {ACM}
}
```

### Book

```bibtex
@book{sommerville2011software,
  author    = {Sommerville, Ian},
  title     = {Software Engineering},
  edition   = {9th},
  year      = {2011},
  publisher = {Pearson Education}
}
```

### Website / Online resource

```bibtex
@online{turingbot2020,
  author  = {{TuringBot}},
  title   = {TuringBot: Symbolic Regression Software},
  year    = {2020},
  url     = {https://turingbot.com},
  urldate = {2025-01-15}
}
```

### Software

```bibtex
@software{rEGGression,
  author  = {de Fran\c{c}a, Fabr\'{i}cio Olivetti},
  title   = {rEGGression: A Rust Library for Symbolic Regression with e-graphs},
  year    = {2024},
  url     = {https://github.com/folivetti/rEGGression}
}
```

---

## Common Packages

| Package | Purpose | Key commands |
|---|---|---|
| `graphicx` | Include images | `\includegraphics[width=...]{path}` |
| `booktabs` | Professional tables | `\toprule`, `\midrule`, `\bottomrule` |
| `amsmath` | Math environments | `\begin{align}`, `\text{}` in math |
| `amssymb` | Math symbols | `\mathbb{R}`, `\forall`, `\exists` |
| `hyperref` | Clickable references | Auto-links `\ref`, `\cite` |
| `listings` | Code listings | `\begin{lstlisting}`, `\lstinline` |
| `tikz` | Diagrams | `\begin{tikzpicture}` |
| `subcaption` | Subfigures | `\begin{subfigure}`, `\subcaption` |
| `tabularx` | Auto-width tables | `\begin{tabularx}{\textwidth}{lXX}` |
| `placeins` | Float control | `\FloatBarrier` |
| `adjustbox` | Resize content | `\adjustbox{max width=\textwidth}` |
| `forest` | Tree diagrams | `\begin{forest}` |

---

## Debugging Tips

### "Undefined reference" warnings

A `\ref{}` or `\cite{}` points to a non-existent label. Check:
1. The label exists and is spelled correctly (case-sensitive)
2. You've compiled twice (LaTeX needs two passes for references)
3. The label is in a file that's actually included (`\input` or `\include`)

### Floats drifting to end of chapter

LaTeX accumulates unplaced floats. Solutions:
1. Add `[htbp]` to all float environments
2. Insert `\FloatBarrier` at section boundaries
3. Use `\clearpage` before major sections
4. Reduce the number of floats or make them smaller

### Overfull hbox warnings

Line too wide for the column. Solutions:
1. Rephrase the text to allow better line breaks
2. For code: use `breaklines=true` in listings
3. For URLs: use `\url{}` with `breakurl` package
4. For tables: use `p{width}` columns or `\resizebox`

### BibTeX/Biber errors

- "I couldn't open file X.bib": Check `\addbibresource{filename.bib}` spelling
- Missing fields: Some styles require specific fields (year, author). Add them
  or use `@misc` for informal sources
