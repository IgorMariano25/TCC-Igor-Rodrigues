# Artigo do TCC (template SciTePress / ICISSP)

Artigo escrito em inglês, conforme exige o template do orientador (`../Template/Example.tex`:
*"all the papers must be in English"*). Nenhum arquivo de `../Template/` foi alterado: os quatro
arquivos de estilo abaixo são cópias idênticas (mesmo SHA-1).

## Arquivos

| Arquivo | Papel |
|---|---|
| `main.tex` | texto do artigo |
| `references.bib` | 36 referências; metadados de cada DOI tirados do registro Crossref |
| `figures/fig_*.pdf` | figuras vetoriais (os `.png` de 300 dpi são só pré-visualização) |
| `scripts/make_figures.py` | regenera as figuras a partir dos CSVs do pipeline |
| `SCITEPRESS.sty`, `article.cls`, `apalike.sty`, `apalike.bst` | cópias do template |

## Como compilar

O artigo **não foi compilado nesta máquina** (não há LaTeX instalado, e o download de um
compilador foi bloqueado pela política de segurança da sessão). Para gerar o PDF:

- **Overleaf:** envie esta pasta inteira, defina `main.tex` como documento principal e use o
  compilador **pdfLaTeX** (as figuras são PDF, então não use `latex`/`dvips`).
- **Local (TeX Live ou MiKTeX):**
  ```
  pdflatex main
  bibtex main
  pdflatex main
  pdflatex main
  ```

Antes da entrega, confira no PDF: (1) **no máximo 12 páginas** (estimativa: 11 a 12);
(2) nenhum aviso de *overfull hbox* relevante nas tabelas; (3) todas as citações resolvidas.

### Se passar de 12 páginas, corte nesta ordem

1. Tabela 2 (os 30 repositórios), que pode ir para um apêndice ou sair;
2. subseção 5.2 *Lessons for Build-Free Pipelines*;
3. subseção 2.5 *Learning from Imbalanced Security Data*, que pode ser resumida em duas frases;
4. as 7 referências de ferramentas (`@misc`), que podem virar notas de rodapé com a URL.

## Pendências (marcadas com `TODO` no `main.tex`)

- **Autores e afiliação:** completar `[Advisor Name]`, `[University Name]`, `[City]` e o e-mail
  do orientador. O e-mail do autor usado é `igor-mariano@outlook.com`; o artigo da AP2 usava
  `igor-mariano@outlook.com.br`, então confirme qual é o correto. Confirme também se Filipe Gama,
  coautor do estudo da AP2, entra como autor.
- **Submissão às cegas (ICISSP):** remover nomes, afiliação, e-mail e a URL do repositório.
- **Disponibilidade dos dados:** hoje `data_nsa/`, `data_govbr/` e `reports_govbr/` estão no
  `.gitignore`. Faça o commit desses dados (e de `Artigo_TCC/Real/scripts/`) antes de trocar
  *"will be made available"* por *"are available"* nos agradecimentos.
- **Declaração de uso de IA:** as regras do ICISSP pedem que o uso de IA seja declarado nos
  agradecimentos. O texto já inclui essa declaração; revise-a.

## Origem dos números

Todos os números foram **recalculados dos CSVs do pipeline**, não copiados do slide:

| Corpus | Dados | Relatórios |
|---|---|---|
| NSA | `github-metrics-analyzer/data_nsa/` | `reports_nsa/` |
| OSS | `github-metrics-analyzer/data/` | `reports/` |
| GOV.BR | `github-metrics-analyzer/data_govbr/` | `reports_govbr/` |

> `reports_oss/` e `data_oss/` são cópias antigas (`reports_oss/` é idêntico ao da NSA) e
> **não** foram usados.

Diferenças em relação ao slide, todas de arredondamento: as métricas de ML foram recalculadas com
precisão total a partir de `ml_confusions.csv`, em vez de reaproveitar os valores já
arredondados de `ml_results.csv`.

| Métrica | Slide | Artigo |
|---|---|---|
| Recall da LR (OSS) | 0,754 | 0,753 |
| Recall da DT (OSS) | 0,398 | 0,399 |
| Precisão da LR (GOV.BR) | 0,097 | 0,096 |
| ROC-AUC do XGBoost (GOV.BR) | 0,902 | 0,903 |

O SIGA tem **1.072** achados do Semgrep no diretório do jQuery UI copiado; destes, **1.021**
estão na documentação HTML, que é o número citado no slide.

## Regenerar as figuras

```
python Artigo_TCC/Real/scripts/make_figures.py
```

O comando deve ser executado a partir da raiz do repositório, com o `.venv` do
`github-metrics-analyzer` (que tem pandas e matplotlib). As cores seguem uma paleta validada
para daltonismo, e o formato dos marcadores diferencia os corpora também em impressão em tons
de cinza.
