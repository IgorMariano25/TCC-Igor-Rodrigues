# AP2 — Segurança em Repositórios Java (ISO/IEC 25010 + Machine Learning)

Estudo de **Mineração de Repositórios de Software (MSR)** que mede a postura de
segurança de projetos Java no GitHub. Cada repositório passa por análise
estática, as métricas são mapeadas para a **ISO/IEC 25010/25023**, e modelos de
**Machine Learning** tentam prever quais arquivos têm achados de segurança.

O projeto começou como trabalho final da disciplina de Engenharia de Software
(AP2, ver [AP2_Trabalho_Final.md](AP2_Trabalho_Final.md)) e evoluiu para o
artigo de TCC.

> **Princípio central:** a análise é só estática, feita sobre o código clonado.
> Nenhum projeto é compilado ou executado.

---

## Corpora analisados

| Corpus | Lista | Pastas | Situação |
|---|---|---|---|
| 1 — NSA | `repos_nsa.txt` | `*_nsa/` | Encerrado (preservado no commit `b37ad22`) |
| 2 — OSS | `repos.txt` | `repos_oss/` (clones), `data/`, `reports/` | Principal |
| 3 — gov.br | `repos_govbr.txt` | `*_govbr/` | Repositórios do governo brasileiro |

Todos estão dentro de [github-metrics-analyzer/](github-metrics-analyzer/).

---

## Estrutura do repositório

```
AP2-Projeto-ES/
├── github-metrics-analyzer/   # pipeline de coleta, dataset e ML (Python)
│   ├── scripts/               # uma fase por script + run_all_corpus.py
│   ├── repos*.txt             # listas de repositórios de cada corpus
│   ├── data_*/  reports_*/    # resultados (CSVs, relatórios, gráficos)
│   └── README.md              # documentação detalhada do pipeline
├── Artigo/                    # artigo da AP2, padrão SBC (português)
├── Artigo_TCC/
│   ├── Template/              # template SciTePress do orientador (não alterar)
│   ├── Real/                  # artigo do TCC (inglês) + figuras
│   └── pesquisa_citacoes.md   # levantamento de referências
├── AP2_Trabalho_Final.md      # enunciado do trabalho
├── RESUME.md                  # contexto do projeto para assistentes de IA
└── github-metrics-analyzer-apresentacao.pdf
```

---

## Ferramentas do pipeline

| Dimensão | Ferramenta | ISO 25010 |
|---|---|---|
| SAST (alvo do ML) | Semgrep ∪ CodeQL | Segurança |
| Estrutura/complexidade | SonarQube (lizard como fallback) | Manutenibilidade / Confiabilidade |
| Métricas OO | CK | Manutenibilidade |
| Processo (histórico git) | PyDriller | Manutenibilidade |
| Dependências (SCA) | OSV API | Segurança › Resistência |
| Segredos expostos | Gitleaks + detect-secrets | Segurança › Confidencialidade |
| Linhas de código | cloc | Normalização |

---

## Como executar

```powershell
cd github-metrics-analyzer
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\scripts\setup_dev_tools.ps1          # baixa CK, CodeQL, SonarScanner, Gitleaks
copy .env.example .env                 # preencha o token do GitHub

python scripts/run_all.py                         # Corpus 2 (repos.txt)
python scripts/run_all_corpus.py --corpus govbr   # Corpus 3 (repos_govbr.txt)
```

As instruções completas (fases, retomada de coletas, versões das ferramentas)
estão em [github-metrics-analyzer/README.md](github-metrics-analyzer/README.md),
[TOOLS_VERSIONS.md](github-metrics-analyzer/TOOLS_VERSIONS.md) e
[RETOMAR_CORPUS2.md](github-metrics-analyzer/RETOMAR_CORPUS2.md).

Para compilar os artigos, veja [Artigo/README.md](Artigo/README.md) e
[Artigo_TCC/Real/README.md](Artigo_TCC/Real/README.md).

---

## O que não é versionado

Os clones dos repositórios, as ferramentas externas (~1 GB), as coletas
parciais, os logs e o `.env` ficam fora do Git (ver os `.gitignore`). Os
arquivos maiores que 100 MB (`data/complexity.csv`, `metrics.db`) vão via
**Git LFS**.

---

## Autor

Igor Mariano — Engenharia de Software.
