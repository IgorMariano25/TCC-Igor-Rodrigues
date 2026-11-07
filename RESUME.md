# RESUME.md — Contexto do Projeto (AP2 → TCC — Engenharia de Software)

> Documento de contexto destinado a **assistentes de IA**. Resume objetivo,
> arquitetura, metodologia, ferramentas, dados, ML e convenções do projeto,
> para que outro agente compreenda rapidamente o repositório sem precisar
> reexplorar tudo. Fonte: leitura real dos arquivos do workspace
> (`AP2_Trabalho_Final.md`, `github-metrics-analyzer/`, `Artigo/`,
> `Artigo_TCC/`). **Última atualização: 2026-11-07.**

---

## 1. O que é o projeto

Trabalho acadêmico (AP2) que aplica **Engenharia de Software + Ciência de Dados +
Machine Learning** à **mineração de repositórios de código-fonte** (MSR).

**Problema escolhido:** prever quais arquivos `.java` são **propensos a risco de
segurança**, a partir de métricas de qualidade/estrutura/processo, ancorando tudo
na norma **ISO/IEC 25010 / 25023**.

**Evolução:** o projeto começou como trabalho da disciplina (AP2, artigo SBC em
português, só com o corpus NSA) e virou o **TCC**. O pipeline é o mesmo, sem
alterações, aplicado a **três corpora** de 10 repositórios Java cada, e o
artigo está em inglês, no template SciTePress.

| Corpus | Lista | Repositórios | Linhas do dataset | Positivos |
|---|---|---|---|---|
| 1 — NSA | `repos_nsa.txt` | `NationalSecurityAgency/*` (ghidra, datawave, emissary, timely, …) | 31.622 | 560 (1,77%) |
| 2 — OSS | `repos.txt` | netty, shiro, nacos, rocketmq, zookeeper, dubbo, jenkins, httpcomponents-client, commons-compress, thingsboard | 64.415 | 839 (1,30%) |
| 3 — GOV.BR | `repos_govbr.txt` | demoiselle (framework, signer, behave, certificate), projetos-codic-ibict (3 forks DSpace + dataverse), lexml/eta-backend-services, projeto-siga/siga | 33.521 | 784 (2,34%) |

- O **Corpus 2 substituiu o NSA** como corpus principal: 4 dos 10 repos NSA
  são do ecossistema DataWave (variável de confusão). Os critérios estão em
  `github-metrics-analyzer/CRITERIOS_SELECAO_REPOSITORIOS.md`.
- O **Corpus 3** saiu de uma lista fornecida pelo autor.
  `projetos-codic-ibict/dataverse` é clonado no branch `master`
  (`BRANCH_OVERRIDES` em `clone_repositories.py`).
- As linhas do dataset incluem arquivos não-Java e caminhos `.java` que só
  existem no histórico git. O artigo do TCC conta 60.395 arquivos Java.

**Princípio central (crítico):** análise **100% estática** sobre o código-fonte
clonado. **Nenhum projeto é compilado, buildado ou executado.** Isso condiciona
todas as escolhas de ferramenta (ex.: CodeQL `--build-mode=none`, SonarScanner
source-only).

Entregas: (1) extração de métricas, (2) pipeline de ML, (3) artigo SBC da AP2
(`Artigo/`) e (4) artigo do TCC (`Artigo_TCC/Real/`).

---

## 2. Estrutura do workspace

```
AP2-Projeto-ES/
├── README.md                      # Visão geral do projeto
├── AP2_Trabalho_Final.md          # Enunciado oficial da AP2
├── RESUME.md                      # (este arquivo)
├── Artigo/                        # Artigo AP2: SBC, português, só NSA
├── Artigo_TCC/
│   ├── Template/                  # Template SciTePress do orientador — NÃO alterar
│   ├── Real/                      # Artigo do TCC (inglês, 3 corpora)
│   │   ├── main.tex, references.bib
│   │   ├── figures/               # fig_pipeline, fig_density, fig_performance (.pdf)
│   │   └── scripts/make_figures.py  # regenera as figuras a partir dos CSVs
│   └── pesquisa_citacoes.md       # Levantamento de referências
└── github-metrics-analyzer/       # Pipeline de coleta + ML (núcleo do projeto)
    ├── README.md, resumo.md, TOOLS_VERSIONS.md, requirements.txt
    ├── RETOMAR_CORPUS2.md         # Diário da execução do Corpus 2 por etapas
    ├── CRITERIOS_SELECAO_*.md     # Critérios de seleção dos repositórios
    ├── repos.txt / repos_nsa.txt / repos_govbr.txt
    ├── scripts/                   # Uma fase por arquivo + run_all.py + run_all_corpus.py
    ├── data/, reports/            # Saídas CANÔNICAS do Corpus 2 (OSS)
    ├── data_govbr/, reports_govbr/, repos_govbr/   # Corpus 3 (gitignored)
    ├── data_nsa/, reports_nsa/, repos_nsa/         # Corpus 1 (gitignored; versionado no commit b37ad22)
    ├── data_oss/, reports_oss/, repos_oss/         # ver aviso abaixo
    ├── developer-tools/           # Binários pesados (gitignored): CK, CodeQL, gitleaks, sonar-scanner
    └── tools/                     # Temporários do CK
```

> **Aviso sobre as pastas `*_oss/` (criadas no commit `567bb6d`):**
> `data_oss/` é uma cópia *intermediária* do Corpus 2, sem
> `pydriller_metrics.csv` nem `security_dataset.csv`. `reports_oss/` tem os
> resultados do **NSA** (iguais aos de `reports_nsa/`), não os do OSS. As
> saídas válidas do Corpus 2 estão em `data/` e `reports/`, e `repos_oss/`
> guarda os clones do Corpus 2.

---

## 3. Metodologia — "uma fonte por dimensão"

Cada dimensão de análise tem **uma única ferramenta canônica**, para evitar
multicolinearidade e não contaminar o ranking de importância de features (o
resultado que liga métricas às sub-características da ISO 25010).

| Dimensão | Ferramenta canônica | Fallback | ISO 25010 |
|---|---|---|---|
| **SAST (alvo do ML)** | **Semgrep ∪ CodeQL** (união) | — | Segurança |
| Estrutura / complexidade | **SonarQube** (Web API) | lizard (offline) | Manutenibilidade |
| Métricas OO | **CK** (Maurício Aniche) | — | Manutenibilidade |
| Processo (git) | **PyDriller** | — | Manutenibilidade |
| SCA (dependências) | **OSV API** | — | Segurança > Resistência |
| Segredos expostos | **Gitleaks + detect-secrets** (união dedup) | — | Segurança > Confidencialidade |
| Linhas de código | **cloc** | contador Python | normalização KLOC |

**Regras metodológicas importantes:**
- **Alvo = união Semgrep ∪ CodeQL:** arquivo é positivo (`has_security_risk=1`)
  se *qualquer* das duas SASTs o sinaliza. Maximiza recall (em segurança,
  falso-negativo é o pior erro).
- **Anti-vazamento:** `n_semgrep` e `n_codeql` entram no dataset apenas como
  descritivo e são **excluídos das features do ML** (derivam do alvo).
- **SonarQube NÃO é oráculo de segurança:** sem bytecode, regras de segurança
  não disparam; ele fornece apenas estrutura/manutenibilidade.
- **SonarQube OU lizard**, nunca ambos (fallback quando `sonarqube.csv` ausente).
- **Segredos e OSV** são descritivos (não são feature nem alvo do ML).
- **Degradação graciosa:** se uma ferramenta pesada faltar, a fase grava saída
  vazia e o pipeline continua.

---

## 4. Pipeline de execução

Orquestrado por `scripts/run_all.py` (lista `PHASES`). Cada fase é um módulo
independente com `main()`; falhas são logadas e não abortam o restante (exceto
`--strict`). Todos compartilham `scripts/common.py` (caminhos absolutos, logging,
`.env`, resolução de ferramentas, GitHub API com rate-limit/backoff).

```
clone ──► repos/ (clones git, sem build)
   ├─► loc          → data/loc.csv                 (normalização KLOC)
   ├─► complexity   → data/complexity.csv          (lizard; fallback estrutural)
   ├─► sonarqube    → data/sonarqube.csv           (estrutural canônico)
   ├─► semgrep      → data/semgrep_findings.csv     ┐ alvo do ML
   ├─► codeql       → data/codeql_findings.csv      ┘ (união)
   ├─► pydriller    → data/pydriller_metrics.csv    (processo, feature)
   ├─► ck           → data/ck_metrics.csv           (OO, feature)
   ├─► osv          → data/osv_*.csv                (descritivo SCA)
   └─► secrets      → data/secrets_*.csv            (descritivo)
                            │
   dataset ◄──────────────── (junta todos)  → data/security_dataset.csv + dataset_dictionary.md
                            │
   ml ◄───────────────────── (lê só security_dataset.csv) → reports/ml_results.csv, ml_confusions.csv, charts/*.png
                            │
   report ◄───────────────── → reports/comparative_report.md + charts/*.png
```

**Dependências reais:** `clone` primeiro; as 9 coletas são independentes entre
si; `dataset` é barreira (junta tudo); `ml` lê só o dataset; `report` lê os CSVs
de achados.

**Outros corpora:** `run_all_corpus.py --corpus <nome>` lê `repos_<nome>.txt`,
redireciona as saídas para `repos_<nome>/`, `data_<nome>/`, `reports_<nome>/`
e `metrics_<nome>.db` e então chama o `run_all.py`, repassando `--only` e
`--skip`. Scripts de apoio fora do `run_all.py`:
`collect_ck_ghidra.py`, `collect_native_resumable.py` (coletas
particionadas/retomáveis para o repo gigante `ghidra`).

---

## 5. Mapeamento script → fase

| Script | Fase | Saída |
|---|---|---|
| `clone_repositories.py` | clone | `repos/` |
| `collect_loc_metrics.py` | loc | `loc.csv` |
| `collect_complexity_metrics.py` | complexity | `complexity.csv` (lizard) |
| `collect_sonarqube_metrics.py` | sonarqube | `sonarqube.csv` |
| `collect_semgrep_metrics.py` | semgrep | `semgrep_findings.csv` |
| `collect_codeql_metrics.py` | codeql | `codeql_findings.csv` |
| `collect_pydriller_metrics.py` | pydriller | `pydriller_metrics.csv` |
| `collect_ck_metrics.py` | ck | `ck_metrics.csv` |
| `collect_osv_metrics.py` | osv | `osv_findings.csv`, `osv_summary.csv` |
| `collect_gitleaks_metrics.py` | secrets | `secrets_findings.csv`, `secrets_summary.csv` |
| `build_security_dataset.py` | dataset | `security_dataset.csv`, `dataset_dictionary.md` |
| `ml_security_pipeline.py` | ml | `ml_results.csv`, `ml_confusions.csv`, `charts/*.png` |
| `generate_comparative_report.py` | report | `comparative_report.md` |
| `run_all.py` | orquestrador | Corpus 2 (`data/`, `reports/`) |
| `run_all_corpus.py` | orquestrador por corpus | `data_<corpus>/`, `reports_<corpus>/` |
| `collect_ck_partitioned.py`, `collect_ck_ghidra.py` | apoio | CK por raiz de módulo |
| `recollect_codeql_repo.py` | apoio | recoleta o CodeQL de um único repo |
| `common.py` | — | utilitários compartilhados |
| `setup_dev_tools.ps1` | setup | instala binários em `developer-tools/` |

---

## 6. Dataset e ML

**Unidade de análise:** arquivo `.java` (contagens de cada corpus na §1).
As classes são muito desbalanceadas: só 1,3–2,3% dos arquivos são positivos.

**Target:** `has_security_risk` (binário; 1 = Semgrep OR CodeQL).

**Features** (ver `data/dataset_dictionary.md`):
- **Estruturais (SonarQube):** `sonar_ncloc`, `sonar_complexity`,
  `sonar_cognitive_complexity`, `sonar_duplicated_lines_density`,
  `sonar_code_smells`, `sonar_sqale_index`, etc.
- **OO (CK):** `wmc`, `dit`, `noc`, `cbo`, `rfc`, `lcom`, `lcom_star`, `tcc`,
  `lcc`, `num_methods`, `num_fields`, `num_classes`.
  - Agregação classe→arquivo: WMC/RFC/num_methods por **soma**;
    DIT/NOC/CBO/LCOM/TCC por **máximo**.
- **Processo (PyDriller):** `commits`, `distinct_authors`, `lines_added`,
  `lines_removed`, `churn`, `file_age_days`, `days_since_change`.
- **Excluídas (anti-vazamento):** `n_semgrep`, `n_codeql`.

**Modelagem** (`ml_security_pipeline.py`):
- **Validação:** `GroupKFold` **por repositório** (grupos = repos) para evitar
  vazamento entre treino/teste do mesmo projeto.
- **Desbalanceamento:** SMOTE (`imbalanced-learn`).
- **Modelos:** LogisticRegression, DecisionTree, RandomForest, XGBoost, LightGBM.
- **Métricas:** priorizar **ROC-AUC / Recall / F1** (não accuracy, dado o
  desbalanceamento).
- **Interpretabilidade:** SHAP + importância de features (RandomForest).

**Resultados (médias do GroupKFold por repositório, tiradas do `ml_results.csv` de cada corpus):**

| Modelo | ROC-AUC NSA | ROC-AUC OSS | ROC-AUC GOV.BR | Recall NSA / OSS / GOV.BR |
|---|---|---|---|---|
| LogisticRegression | 0.815 | 0.893 | 0.854 | 0.705 / 0.754 / 0.751 |
| DecisionTree | 0.762 | 0.806 | 0.804 | 0.426 / 0.399 / 0.553 |
| RandomForest | 0.854 | 0.891 | 0.895 | 0.172 / 0.099 / 0.430 |
| XGBoost | 0.829 | 0.862 | 0.903 | 0.131 / 0.062 / 0.387 |
| LightGBM | 0.845 | 0.872 | **0.910** | 0.133 / 0.062 / 0.330 |

> Os números do NSA vêm do re-run (`reports_nsa/`). A versão original da AP2
> (RandomForest com 0.859, citada em `Artigo/`) é anterior a esse re-run.

**Achados centrais do TCC:**
- O sinal é estável, mas modesto: ROC-AUC entre 0.76 e 0.91 e precisão de no
  máximo 0.45. A LogisticRegression é o modelo mais estável, com recall entre
  0.70 e 0.75.
- **O 0.910 do GOV.BR é artefato de vazamento.** Cerca de 80% dos `.java` de
  um fork DSpace são idênticos byte a byte aos de outro fork. Sem os folds 1 e
  3, o RandomForest cai para 0.834, em linha com os outros corpora. Agrupar os
  folds por repositório não basta: o grupo precisa ser a *linhagem de código*.
- Os achados do Semgrep vêm sobretudo de arquivos que não são Java: YAML de CI
  no OSS e um jQuery UI vendorizado no `siga`. Só 3,6% a 11,5% dos positivos
  são marcados pelas duas SASTs ao mesmo tempo.
- Importância no RandomForest: medidas estruturais 58–74%, OO 14–28% e
  processo 12–18%. A complexidade cognitiva lidera no NSA e no OSS, e o
  `ncloc` no GOV.BR.
- Rodado em lote único, o CK falhou no Ghidra, e a cobertura OO do NSA ficou
  em 26%. Rodado por raiz de módulo, cobriu 97% dos arquivos no OSS e no
  GOV.BR.

---

## 7. Ambiente e ferramentas (versões — `TOOLS_VERSIONS.md`)

- **Python** 3.10+ (testado com 3.12.0); **JDK** OpenJDK 24 (para o CK);
  **Git** e **Docker** (servidor SonarQube) no PATH.
- **Python libs** (`requirements.txt`, versões `>=`): pandas, numpy, requests,
  lizard, pydriller, detect-secrets, scikit-learn, xgboost, lightgbm, shap,
  imbalanced-learn, matplotlib, seaborn, tabulate, python-dotenv.
  - **Atenção:** `semgrep` é usado mas **não está** no `requirements.txt`
    (`pip install semgrep` à parte).
- **Binários pesados** (em `developer-tools/`, gitignored; resolvidos por
  `common.find_external_tool`: env var → PATH → `developer-tools/`):
  CK 0.7.0, Gitleaks 8.30.1, SonarScanner CLI 6.2.1, CodeQL 2.25.6.
- **SonarQube server** (Community) roda via Docker na porta 9000.
- **OSV** é API HTTP (sem binário).

**Credenciais (`.env`, não versionado, lido por `common.py`):**
`GITHUB_TOKEN` (ou `GH_TOKEN`), `SONAR_HOST_URL` (padrão `http://localhost:9000`),
`SONAR_TOKEN` (precisa ser **User Token**, não Global Analysis Token).

**Não há Dockerfile/compose no projeto** — Docker só sobe o SonarQube.

---

## 8. Como executar (resumo)

```powershell
# 1. Ferramentas pesadas → developer-tools/
pwsh -File scripts/setup_dev_tools.ps1

# 2. Servidor SonarQube (gere um USER TOKEN em My Account > Security)
docker run -d --name sonarqube -p 9000:9000 sonarqube:community

# 3. Ambiente Python
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install semgrep            # não está no requirements.txt

# 4. Credenciais
Copy-Item .env.example .env    # editar GITHUB_TOKEN, SONAR_HOST_URL, SONAR_TOKEN

# 5. Pipeline inteiro
python scripts/run_all.py                          # Corpus 2 → data/, reports/
python scripts/run_all_corpus.py --corpus govbr    # Corpus 3 → *_govbr/
#   pular fases:      python scripts/run_all.py --skip clone
#   só algumas fases: python scripts/run_all.py --only sonarqube,codeql,dataset,ml
#   só ML:            python scripts/run_all.py --only ml   (requer security_dataset.csv)
```

Os scripts resolvem caminhos de forma absoluta em `common.py` → funcionam de
qualquer diretório, mas assumem a raiz `github-metrics-analyzer/`.

---

## 9. Artigos

### 9.1 Artigo do TCC (`Artigo_TCC/Real/`) — atual

- Template **SciTePress** (ICISSP), em **inglês**, como exige o template do
  orientador. Título: *"Predicting Security-Prone Java Files from Quality
  Metrics: A Build-Free Three-Corpus Study and the Pitfall of Near-Duplicate
  Forks"*.
- `Artigo_TCC/Template/` é o template original e **não deve ser alterado**.
  Os arquivos de estilo em `Real/` são cópias idênticas dele.
- `references.bib` tem 44 referências, com metadados tirados do Crossref.
- As figuras são geradas por `scripts/make_figures.py` a partir dos CSVs do
  pipeline. Compile com pdfLaTeX, porque as figuras são PDF.
- Situação: primeira versão no commit `9e38a99` ("precisa de ajustes"). Não há
  LaTeX nesta máquina; compile no Overleaf.

### 9.2 Artigo da AP2 (`Artigo/`) — só corpus NSA

- Padrão **SBC** (6–10 páginas), pronto para Overleaf (pdfLaTeX).
- `main.tex` já contém os números reais do estudo; estrutura obrigatória:
  Introdução → Fundamentação → Metodologia → Resultados → Conclusão → Referências.
- Números vêm de `reports/comparative_report.md`, `reports/ml_results.csv` e
  `data/security_dataset.csv`.
- Compilar local: `pdflatex main && bibtex main && pdflatex main && pdflatex main`.
- **Referências** (`referencias.bib`) são obras reais (ISO 25000/25010/25023,
  McCabe 1976, Chidamber & Kemerer 1994, PyDriller/Spadini 2018, SMOTE/Chawla
  2002, Random Forest/Breiman 2001, XGBoost 2016, LightGBM 2017, SHAP 2017) —
  conferir autores/ano/DOI antes de submeter.

---

## 10. Convenções e decisões de projeto (para agentes)

- **Idempotência:** reexecutar qualquer fase regrava CSVs sem duplicar; clones
  existentes são atualizados via `git fetch`, não reclonados.
- **Robustez:** exceções capturadas por repo/arquivo; falhas logadas sem abortar.
- **Encoding:** saídas de subprocesso em `utf-8` com `errors="ignore"`.
- **Rate limit:** `common.github_get` respeita `Retry-After` e
  `X-RateLimit-Reset`, paginação `per_page=100`.
- **Sem build/compilação** — respeitar sempre esse princípio ao mexer em coletas.
- **Segurança:** nunca commitar tokens; `.env` está no `.gitignore`; escopo
  mínimo `public_repo`.
- **Limitações de validade:** 4 dos 10 repos NSA pertencem ao ecossistema
  **DataWave** (o que motivou o Corpus 2). No GOV.BR, forks DSpace quase
  idênticos vazam informação entre os folds.
- **Pastas por corpus:** nunca rode o Corpus 3 com o `run_all.py` puro, porque
  ele grava no `data/` do Corpus 2. Use o `run_all_corpus.py`.
- **Versionamento:** clones (`repos*/`), coletas parciais (`*/partial/`), logs
  e as pastas `*_nsa/` e `*_govbr/` estão no `.gitignore`. Arquivos acima de
  100 MB vão via Git LFS.
- **Branches:** `main` é o estável; `Artigo_TCC` concentra o trabalho atual do TCC.
- **Métrica não coletável** aparece como ausente/zero, **nunca estimada**.

---

## 11. Onde procurar mais detalhes

| Preciso de… | Arquivo |
|---|---|
| Enunciado/requisitos do trabalho | `AP2_Trabalho_Final.md` |
| Documentação de uso do pipeline | `github-metrics-analyzer/README.md` |
| Resumo técnico profundo (versões, decisões) | `github-metrics-analyzer/resumo.md` |
| Versões exatas das ferramentas | `github-metrics-analyzer/TOOLS_VERSIONS.md` |
| Dicionário de colunas do dataset | `github-metrics-analyzer/data/dataset_dictionary.md` |
| Resultados comparativos + ML (OSS) | `github-metrics-analyzer/reports/comparative_report.md` |
| Resultados GOV.BR / NSA | `github-metrics-analyzer/reports_govbr/`, `reports_nsa/` |
| Critérios de seleção dos repositórios | `github-metrics-analyzer/CRITERIOS_SELECAO_REPOSITORIOS.md` |
| Histórico da execução do Corpus 2 | `github-metrics-analyzer/RETOMAR_CORPUS2.md` |
| Artigo do TCC (SciTePress) | `Artigo_TCC/Real/main.tex`, `Artigo_TCC/Real/README.md` |
| Artigo da AP2 (SBC) | `Artigo/main.tex`, `Artigo/README.md` |
```