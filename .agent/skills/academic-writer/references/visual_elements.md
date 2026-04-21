# Visual Elements Reference

Templates and best practices for creating tables, TikZ diagrams, figures,
and other visual elements in academic documents.

## Table of Contents

1. [Tables](#tables)
2. [TikZ Diagrams](#tikz-diagrams)
3. [Figures](#figures)
4. [Subfigures](#subfigures)
5. [Charts and Plots](#charts-and-plots)
6. [Generated Images](#generated-images)
7. [Grammar and Syntax Diagrams](#grammar-and-syntax-diagrams)

---

## Tables

### Basic comparison table (booktabs)

```latex
\begin{table}[htbp]
    \caption{Comparison of symbolic regression tools by key features}
    \centering
    \begin{tabular}{lccc}
        \toprule
        \textbf{Feature} & \textbf{TuringBot} & \textbf{HeuristicLab} & \textbf{Spectrum} \\
        \midrule
        Remote execution    & \texttimes & \texttimes & \checkmark \\
        Web interface       & \texttimes & \texttimes & \checkmark \\
        DSL support         & \texttimes & \texttimes & \checkmark \\
        Open source         & \texttimes & \checkmark & \checkmark \\
        Pipeline support    & \texttimes & Partial    & \checkmark \\
        E-graph backend     & \texttimes & \texttimes & \checkmark \\
        \bottomrule
    \end{tabular}
    \label{tab:tool_comparison}
\end{table}
```

### Wide table with auto-width columns (tabularx)

```latex
\begin{table}[htbp]
    \caption{Summary of user stories and their functional requirements}
    \centering
    \begin{tabularx}{\textwidth}{lXX}
        \toprule
        \textbf{ID} & \textbf{User Story} & \textbf{Acceptance Criteria} \\
        \midrule
        US1 & Upload CSV data files & User can upload files up to 100MB \\
        US2 & Generate random datasets & System creates valid CSV with
              configurable dimensions \\
        US3 & Configure training jobs & User can set all EGGP parameters \\
        \bottomrule
    \end{tabularx}
    \label{tab:user_stories}
\end{table}
```

### Numeric results table

Right-align numeric columns, use consistent decimal places:

```latex
\begin{table}[htbp]
    \caption{Training performance across benchmark datasets, showing MSE
    and R² scores with mean ± standard deviation over 5 runs}
    \centering
    \begin{tabular}{lrrrr}
        \toprule
        \textbf{Dataset} & \textbf{MSE} & \textbf{R²} &
        \textbf{Time (s)} & \textbf{Expressions} \\
        \midrule
        Feynman I.6.20  & 0.0023 ± 0.0005 & 0.998 ± 0.001 & 12.3 & 847 \\
        Feynman I.9.18  & 0.0156 ± 0.0031 & 0.984 ± 0.003 & 18.7 & 1203 \\
        Nguyen-1        & 0.0001 ± 0.0000 & 0.999 ± 0.000 &  5.2 & 312 \\
        Nguyen-4        & 0.0089 ± 0.0012 & 0.991 ± 0.001 &  8.9 & 594 \\
        \bottomrule
    \end{tabular}
    \label{tab:training_results}
\end{table}
```

### Table best practices

- Use `\toprule`, `\midrule`, `\bottomrule` from `booktabs` — never `\hline`
- No vertical rules (`|`) — they clutter the table
- Right-align numbers, left-align text, center short categorical values
- Use consistent decimal places within each column
- If a table is too wide, consider:
  - Rotating to landscape with `\begin{landscape}` (from `pdflscape`)
  - Using abbreviations with a note below the table
  - Splitting into two tables
  - Using `\resizebox{\textwidth}{!}{\begin{tabular}...}`

---

## TikZ Diagrams

### Flowchart / Pipeline

```latex
\begin{figure}[htbp]
    \caption{IQL query execution pipeline, from user input to stored results}
    \centering
    \begin{tikzpicture}[
        node distance=1.5cm,
        block/.style={
            rectangle, draw, rounded corners,
            minimum height=1cm, minimum width=2.5cm,
            text centered, font=\sffamily\small
        },
        arrow/.style={->, >=stealth, thick}
    ]
        \node[block] (input) {IQL Query};
        \node[block, right=of input] (tokenizer) {Tokenizer};
        \node[block, right=of tokenizer] (parser) {Pratt Parser};
        \node[block, right=of parser] (ast) {AST};
        \node[block, below=of ast] (executor) {Executor};
        \node[block, left=of executor] (egraph) {rEGGression};
        \node[block, left=of egraph] (results) {Results};

        \draw[arrow] (input) -- (tokenizer);
        \draw[arrow] (tokenizer) -- (parser);
        \draw[arrow] (parser) -- (ast);
        \draw[arrow] (ast) -- (executor);
        \draw[arrow] (executor) -- (egraph);
        \draw[arrow] (egraph) -- (results);
    \end{tikzpicture}
    \label{fig:iql_pipeline}
\end{figure}
```

### Entity Relationship Diagram

```latex
\begin{figure}[htbp]
    \caption{Relationship between Profile, Job, Run, and Model entities}
    \centering
    \begin{tikzpicture}[
        table/.style={
            draw, thick, rectangle split, rectangle split parts=2,
            rectangle split part fill={gray!20, white},
            align=left, font=\sffamily\footnotesize,
            rounded corners=2pt
        },
        relation/.style={->, >=stealth, thick, draw=gray!70}
    ]
        \node[table] (profile) {
            \textbf{Profile}
            \nodepart{two}
            id (uuid) PK\\
            name (varchar)\\
            owner\_id (uuid) FK
        };

        \node[table, right=3cm of profile] (job) {
            \textbf{Job}
            \nodepart{two}
            id (uuid) PK\\
            profile\_id (uuid) FK\\
            name (varchar)
        };

        \draw[relation] (job.west) -- node[above, font=\tiny] {profile\_id} (profile.east);
    \end{tikzpicture}
    \label{fig:entity_relations}
\end{figure}
```

### Architecture Diagram

```latex
\begin{figure}[htbp]
    \caption{System architecture showing the client-server separation with
    asynchronous worker processing via RabbitMQ message queues}
    \centering
    \begin{tikzpicture}[
        node distance=2cm,
        component/.style={
            rectangle, draw, thick, rounded corners=4pt,
            minimum height=1.2cm, minimum width=3cm,
            text centered, font=\sffamily\small
        },
        db/.style={
            cylinder, draw, thick, shape border rotate=90,
            minimum height=1cm, minimum width=1.5cm,
            font=\sffamily\small, aspect=0.3
        },
        queue/.style={
            rectangle, draw, thick, dashed,
            minimum height=0.8cm, minimum width=2.5cm,
            font=\sffamily\small
        },
        arrow/.style={->, >=stealth, thick},
        label/.style={font=\tiny, text=gray}
    ]
        % Frontend
        \node[component, fill=blue!10] (frontend) {React Frontend};

        % Backend
        \node[component, fill=green!10, below=of frontend] (backend) {FastAPI Backend};

        % Database
        \node[db, fill=orange!10, right=3cm of backend] (db) {PostgreSQL};

        % Message Queue
        \node[queue, below=of backend] (queue) {RabbitMQ};

        % Workers
        \node[component, fill=red!10, below left=1.5cm and 0cm of queue] (worker1) {Training Worker};
        \node[component, fill=red!10, below right=1.5cm and 0cm of queue] (worker2) {IQL Worker};

        % Connections
        \draw[arrow] (frontend) -- node[right, label] {HTTP/SSE} (backend);
        \draw[arrow, <->] (backend) -- node[above, label] {async} (db);
        \draw[arrow] (backend) -- node[right, label] {publish} (queue);
        \draw[arrow] (queue) -- node[left, label] {consume} (worker1);
        \draw[arrow] (queue) -- node[right, label] {consume} (worker2);
        \draw[arrow, <->] (worker1.east) -- ++(1,0) |- node[near start, above, label] {async} (db);
        \draw[arrow, <->] (worker2.west) -- ++(-1,0) |- (db);
    \end{tikzpicture}
    \label{fig:architecture}
\end{figure}
```

### TikZ best practices

- Match existing diagram styles in the project (colors, fonts, arrow types)
- Use `\sffamily` for diagram labels (sans-serif reads better in diagrams)
- Use `\footnotesize` or `\small` for text in complex diagrams
- Define reusable styles at the tikzpicture level
- Use `\resizebox{\textwidth}{!}{...}` if the diagram is too wide
- For complex diagrams, use `on background layer` for edges that cross nodes

---

## Figures

### Standard figure (ABNT)

In ABNT, captions go **above** the figure content:

```latex
\begin{figure}[htbp]
    \caption{Description of what the figure shows, self-contained enough
    to understand without reading the surrounding text}
    \centering
    \includegraphics[width=0.8\textwidth]{images/filename.png}
    \label{fig:identifier}
\end{figure}
```

### Width guidelines

| Content type | Recommended width |
|---|---|
| Screenshots (full page) | `width=0.8\textwidth` |
| Screenshots (partial) | `width=0.5\textwidth` to `0.6\textwidth` |
| Diagrams | `width=\textwidth` with `\resizebox` |
| Narrow elements (sidebar) | `width=0.2\textwidth` to `0.3\textwidth` |

---

## Subfigures

For multiple related images displayed together:

```latex
\begin{figure}[htbp]
    \caption{Comparison of the application interface across different views}
    \centering
    \begin{subfigure}[b]{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{images/view_a.png}
        \subcaption{Profile view showing active experiments}
        \label{fig:view_a}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{images/view_b.png}
        \subcaption{Dataset view with artifact management}
        \label{fig:view_b}
    \end{subfigure}
    \label{fig:views_comparison}
\end{figure}
```

---

## Charts and Plots

When the user provides data or the document needs data-driven visualizations:

### Option 1: pgfplots (pure LaTeX)

```latex
\begin{figure}[htbp]
    \caption{Training convergence over generations for the Feynman I.6.20
    dataset, showing MSE decrease on a logarithmic scale}
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            xlabel={Generation},
            ylabel={MSE},
            ymode=log,
            grid=major,
            width=0.8\textwidth,
            height=6cm,
            legend pos=north east
        ]
            \addplot coordinates {(0,1.5) (10,0.8) (20,0.3) (50,0.05) (100,0.002)};
            \addlegendentry{EGGP}
        \end{axis}
    \end{tikzpicture}
    \label{fig:convergence}
\end{figure>
```

### Option 2: Generated image (via generate_image tool or matplotlib script)

When charts involve complex data or the user provides a CSV/dataset:

1. Generate the chart as a PNG/PDF using a script or the image generation tool
2. Save to the project's images directory
3. Include with `\includegraphics`

---

## Generated Images (Fallback)

TikZ should be the first choice for all diagrams. Fall back to the `generate_image`
tool only when TikZ cannot reasonably express the visual:

- Conceptual illustrations requiring rich visual detail or textures
- Diagrams with 50+ nodes where manual TikZ positioning is impractical
- Infographics or visual summaries that need design-heavy treatment
- Images where photorealistic or artistic quality is required

When generating, aim for:
- Clean, professional style suitable for academic documents
- White or transparent background
- No decorative elements that would look out of place in a thesis
- Resolution high enough for print (at least 300 DPI)
- Consistent style with other figures in the document

Save generated images with descriptive names:
```
images/iql_execution_pipeline.png  ✓
images/diagram1.png                 ✗
images/system_overview.png          ✓
images/fig3.png                     ✗
```

---

## Grammar and Syntax Diagrams

For documenting formal languages (grammars, DSLs, query languages):

### EBNF in LaTeX

```latex
\begin{figure}[htbp]
    \caption{Formal EBNF grammar for the Inference Query Language (IQL),
    defining the syntax for declarative queries over e-graph models}
    \centering
    \begin{tabular}{rcl}
        \toprule
        \textit{query} & ::= & \texttt{SELECT} \textit{quantifier}
            \textit{fields} \texttt{FROM} \textit{source}
            [\textit{where-clause}] \\
        \textit{quantifier} & ::= & \texttt{TOP} \textit{number}
            $\mid$ \texttt{PARETO} \\
        \textit{fields} & ::= & \texttt{*} $\mid$ \textit{field-list} \\
        \textit{field-list} & ::= & \textit{field}
            (\texttt{,} \textit{field})* \\
        \textit{field} & ::= & \texttt{expression} $\mid$ \texttt{error}
            $\mid$ \texttt{size} $\mid$ \texttt{dl}
            $\mid$ \texttt{fitness} \\
        \textit{source} & ::= & \textit{model-name} \\
        \textit{where-clause} & ::= & \texttt{WHERE} \textit{condition}
            (\texttt{AND} \textit{condition})* \\
        \textit{condition} & ::= & \textit{field} \textit{comparator}
            \textit{value} \\
        & & $\mid$ \texttt{PATTERN IS LIKE} \textit{pattern-string} \\
        \textit{comparator} & ::= & \texttt{=} $\mid$ \texttt{!=}
            $\mid$ \texttt{<} $\mid$ \texttt{>}
            $\mid$ \texttt{<=} $\mid$ \texttt{>=} \\
        \bottomrule
    \end{tabular}
    \label{fig:iql_grammar}
\end{figure}
```

### Syntax tree using forest

```latex
\begin{figure}[htbp]
    \caption{Abstract syntax tree for the IQL query
    \texttt{SELECT TOP 5 expression, error FROM model1
    WHERE size < 10}}
    \centering
    \begin{forest}
        [Query
            [SELECT
                [TOP [5]]
                [Fields
                    [expression]
                    [error]
                ]
            ]
            [FROM [model1]]
            [WHERE
                [Condition
                    [size]
                    [{$<$}]
                    [10]
                ]
            ]
        ]
    \end{forest}
    \label{fig:iql_ast_example}
\end{figure>
```
