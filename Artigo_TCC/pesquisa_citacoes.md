# Pesquisa de referências e análise dos artigos premiados do ICISSP

> Levantamento feito em 07/11/2026. Só entram artigos verificados: os 34 PDFs premiados foram baixados e analisados por script, e todos os artigos citados foram confirmados por DOI ou pelo rodapé do PDF.

---

## 1. Resumo do tema

O TCC é um estudo empírico de **mineração de repositórios de software (MSR)** que tenta **prever quais arquivos Java têm risco de segurança** a partir de métricas de código.

- **Pipeline:** 13 fases, **100% estática** (nada é compilado nem executado), aplicada a três corpora de 10 repositórios cada: NSA, OSS e GOV.BR.
- **Alvo (rótulo):** o arquivo é positivo se **Semgrep ou CodeQL** apontam algum achado.
- **Features:** métricas de estrutura (SonarQube/lizard), de orientação a objetos (CK) e de processo (PyDriller).
- **Dados descritivos:** OSV (dependências com CVE) e Gitleaks/detect-secrets (segredos expostos).
- **Ancoragem teórica:** a ISO/IEC 25010/25023.
- **Modelos:** 5, avaliados com GroupKFold por repositório e SMOTE.
- **Achado central do corpus GOV.BR:** o ROC-AUC de 0,91 é inflado por **vazamento entre forks quase idênticos do DSpace**. 80% dos arquivos são idênticos byte a byte. Sem essas dobras, o desempenho volta ao nível dos outros corpora (≈0,83).
- **Distorção secundária:** **código de terceiros copiado** (o jQuery UI dentro do SIGA) infla a densidade de achados.

---

## 2. Palavras-chave

| PT | EN | Sinônimos / variações | Origem |
|---|---|---|---|
| Predição de vulnerabilidades | Vulnerability prediction | vulnerable component/file prediction, VPM | slide (alvo de ML) |
| Mineração de repositórios de software | Mining software repositories | MSR, repository mining | slide (eyebrow) + `github-metrics-analyzer/resumo.md:14` |
| Análise estática de segurança | Static application security testing | SAST, static analysis, code scanning | slide + `README.md` |
| Análise de composição de software | Software composition analysis | SCA, vulnerable dependencies, CVE | `README.md` (tabela de fontes) |
| Segredos expostos | Secret leakage | hard-coded credentials, API keys | slide + `README.md` |
| Métricas orientadas a objetos | Object-oriented metrics | CK metrics, WMC, CBO, RFC, LCOM, DIT | slide (CK) + `data/dataset_dictionary.md` |
| Métricas de processo | Process / change metrics | code churn, developer activity, commits, autores | `RESUME.md` §6 (PyDriller) |
| Complexidade ciclomática / cognitiva | Cyclomatic / cognitive complexity | McCabe, NLOC | `RESUME.md` §6, `resumo.md` |
| Dívida técnica / code smells | Technical debt / code smells | sqale_index, duplicação | `resumo.md:221,276-278` (**não está no slide**) |
| Qualidade de produto ISO/IEC 25010 | Software product quality | SQuaRE, ISO/IEC 25023, segurança | slide (25010); **25023 só em** `README.md` |
| Confidencialidade, Integridade, Autenticidade, Resistência | Confidentiality, integrity, authenticity, resistance | subcaracterísticas de segurança | `reports/comparative_report.md:22-64` (**não está no slide**) |
| CWE / OWASP Top 10 | CWE / OWASP Top 10 | weakness taxonomy | slide (CWE); **OWASP só em** `scripts/collect_semgrep_metrics.py:8-10` |
| Fluxo de dados / consultas sobre AST | Data-flow / query-based analysis | CodeQL `java-security-extended`, `--build-mode=none`, SARIF | `scripts/collect_codeql_metrics.py:10-14,44` (**não está no slide**) |
| Desbalanceamento de classes | Class imbalance | SMOTE, `class_weight=balanced`, oversampling | slide (SMOTE) + `scripts/ml_security_pipeline.py:12,163-166` |
| Validação agrupada / entre projetos | Grouped / cross-project validation | GroupKFold, leave-project-out | slide + `ml_security_pipeline.py:9,139` |
| Vazamento de dados | Data leakage | target leakage, train-test contamination | slide (anti-vazamento, forks) + `README.md` |
| Duplicação de código / forks | Code duplication / near-duplicates | clones, forks, vendored code | slide (DSpace, jQuery UI) + `CRITERIOS_SELECAO_REPOSITORIOS.md:183` |
| Explicabilidade | Explainability | SHAP, TreeExplainer, Gini importance | `ml_security_pipeline.py:16,279-282` (**não está no slide**) |
| Multicolinearidade / "uma fonte por dimensão" | Multicollinearity / feature redundancy | — | `README.md` (**não está no slide**) |
| Variável de confusão / validade externa | Confounding / external validity | threats to validity | `CRITERIOS_SELECAO_REPOSITORIOS.md:204-206`, `comparative_report.md:20` |
| Critérios de seleção de repositórios | Repository selection criteria | ≥300 commits, ≥5 autores, 200–5.000 arquivos | `CRITERIOS_SELECAO_RESUMO.md` (**não está no slide**) |
| Reprodutibilidade | Reproducibility | versões fixas, idempotência | `TOOLS_VERSIONS.md`, `README.md` "Decisões de projeto" |
| Software do setor público | Public sector / e-government software | software público, governo | slide (Corpus 3) |

**Técnicas e algoritmos:** Regressão Logística, Árvore de Decisão, Random Forest, XGBoost, LightGBM, SMOTE, StandardScaler, GroupKFold, SHAP. **Métricas de avaliação:** ROC-AUC, precisão, recall e F1.

---

## 3. Strings de busca

Os eixos são: **E0** geral · **E1** predição com métricas · **E2** ferramentas SAST como rótulo · **E3** dados e validação (duplicação, vazamento, desbalanceamento) · **E4** ISO 25010 · **E5** dependências e segredos · **E6** setor público. Cada string tem uma linha `# busca` (o que procura) e uma linha `# filtro` (período e tipo).

### SciTePress / ICISSP (primeiro)

Os mecanismos de busca na web indexam mal os anais do ICISSP. O método que funcionou foi a API do OpenAlex filtrada pela fonte do ICISSP (id `S7407087899`, que cobre 2015–2026, com 971 artigos). Para a caixa de busca da SciTePress Digital Library, use de 2 a 3 termos simples: não foi confirmado se ela aceita operadores booleanos.

```text
# E0 · busca: tudo do ICISSP sobre vulnerabilidades/código | filtro: 2015–2026, todos os tipos
https://api.openalex.org/works?filter=primary_location.source.id:S7407087899&search=(vulnerability OR "static analysis" OR "source code")&per-page=200

# E1 · busca: predição de vulnerabilidades no ICISSP | filtro: 2015–2026
https://api.openalex.org/works?filter=primary_location.source.id:S7407087899&search=("vulnerability prediction" OR "attack prone" OR "vulnerable code") AND (metrics OR "machine learning")

# E2/E5 · busca: SAST, scanners e segredos no ICISSP (Google)
site:scitepress.org "ICISSP" ("static analysis" OR scanner OR "source code") (vulnerability OR leak OR secret)

# E3 · busca: duplicação/qualidade de dataset no ICISSP (Google)
site:scitepress.org "ICISSP" (duplication OR duplicated OR "dataset" OR "data quality") (vulnerab* OR "machine learning")

# E6 · busca: setor público no ICISSP (Google)
site:scitepress.org "Information Systems Security and Privacy" ("public sector" OR "public administration" OR "e-government")
```

### Google Scholar

```text
# E0 · amplo | filtro: 2010–2026
("vulnerability prediction" OR "vulnerable components") "mining software repositories" "machine learning"

# E0-ICISSP · só os anais do ICISSP (operador source:)
source:"Information Systems Security and Privacy" (vulnerability OR "static analysis" OR "source code")

# E1 · métricas como preditores | filtro: 2010–2026, artigos e anais
"vulnerability prediction" ("software metrics" OR "code churn" OR "complexity metrics") (Java OR "open source")

# E2 · SAST como rótulo/oráculo | filtro: 2018–2026
("static application security testing" OR SAST) (Semgrep OR CodeQL OR SonarQube) (evaluation OR comparison) Java

# E3 · duplicação e vazamento em ML de código | filtro: 2017–2026
("code duplication" OR "near-duplicate" OR forks) ("data leakage" OR "overestimat*") "machine learning" code

# E3 · rótulos e realismo da avaliação
"vulnerability prediction" ("realistic labelling" OR "time-based" OR "cross-project") evaluation

# E4/E6 · PT · busca: trabalhos brasileiros | filtro: 2010–2026
("análise estática" OR "predição de vulnerabilidades") (segurança OR vulnerabilidade) ("aprendizado de máquina" OR "software público")
```

### IEEE Xplore (Command Search)

```text
# E1 · busca: VPMs baseados em métricas | filtro: 2010–2026; Conferences + Journals
("All Metadata":"vulnerability prediction" OR "All Metadata":"vulnerable component*")
 AND ("All Metadata":"software metric*" OR "All Metadata":"code churn" OR "All Metadata":"complexity metric*")

# E2 · busca: avaliação de SAST em Java | filtro: 2018–2026
("Abstract":"static analysis" OR "Abstract":"SAST") AND ("Abstract":security OR "Abstract":vulnerabilit*)
 AND ("Abstract":Java) AND ("Abstract":evaluat* OR "Abstract":compar*) NOT ("Abstract":"smart contract*")

# E3 · busca: vazamento/duplicação em datasets de código | filtro: 2017–2026
("All Metadata":"data quality" OR "All Metadata":duplicat* OR "All Metadata":leakage)
 AND ("All Metadata":"vulnerability dataset*" OR "All Metadata":"defect prediction")

# E4 · busca: ISO 25010 e segurança medida no código | filtro: 2011–2026
("All Metadata":"ISO/IEC 25010" OR "All Metadata":"ISO 25010") AND ("All Metadata":security) AND ("All Metadata":metric*)
```

### ACM Digital Library

```text
# E1 · busca: predição com métricas de código/processo | filtro: 2010–2026; Research Article
[[Abstract: "vulnerability prediction"] OR [Abstract: "vulnerable component*"]]
 AND [[Abstract: "software metric*"] OR [Abstract: "code metric*"] OR [Abstract: churn]]

# E3 · busca: duplicação de código afetando ML | filtro: 2017–2026
[[Abstract: "code duplication"] OR [Abstract: "duplicate*"] OR [Abstract: fork*]]
 AND [Abstract: "machine learning"] AND [[Abstract: code] OR [Abstract: repositor*]]

# E5 · busca: segredos e dependências vulneráveis em GitHub/MSR | filtro: 2017–2026
[[Abstract: "secret*"] OR [Abstract: "vulnerable dependenc*"]] AND [[Abstract: GitHub] OR [Abstract: "open source"]]
```

### Scopus

```text
# E0 · amplo | filtro: 2010–2026; DOCTYPE cp/ar; área COMP
TITLE-ABS-KEY ( ( vulnerab* OR "security risk" ) AND ( "mining software repositories" OR "software metric*" ) AND "machine learning" )
 AND PUBYEAR > 2009 AND ( LIMIT-TO ( SUBJAREA , "COMP" ) )

# E1 · específico (Java/arquivo)
TITLE-ABS-KEY ( ( "vulnerability prediction" OR "vulnerable file*" OR "vulnerable component*" )
 AND ( "code churn" OR "object-oriented metric*" OR "CK metric*" OR "complexity metric*" ) AND java )

# E2 · SAST como rótulo e concordância entre ferramentas
TITLE-ABS-KEY ( ( SAST OR "static analysis tool*" ) AND ( Semgrep OR CodeQL OR SonarQube ) AND ( agreement OR "false positive*" OR comparison ) )

# E3 · vazamento por duplicação (operador de proximidade)
TITLE-ABS-KEY ( ( duplicat* OR clone* OR fork* ) W/3 ( leak* OR overestimat* OR bias ) AND ( "machine learning" OR "deep learning" ) AND code )

# E6 · governo
TITLE-ABS-KEY ( ( "e-government" OR "public sector" OR governmental ) AND ( "static analysis" OR "source code" ) AND security )
```

### SciELO (search.scielo.org)

```text
# E0/E6 · PT+EN | filtro: 2010–2026; artigos
(ti:(vulnerabilidade$ OR vulnerabilit$) OR ab:(vulnerabilidade$ OR vulnerabilit$)) AND (software OR "código-fonte" OR "source code")

# E1/E4 · métricas e qualidade
ab:("métricas de software" OR "software metrics" OR "ISO/IEC 25010") AND ab:(segurança OR security)
```

Nas buscas feitas, o SciELO **não trouxe artigos relevantes** para o tema. A produção brasileira da área está no SBC OpenLib (SBSeg, SBES), que não é indexado pelo SciELO.

### Portal de Periódicos CAPES (busca avançada)

```text
# E0 · PT/EN | filtros: "Revisados por pares", 2010–2026, tipo Artigo
("predição de vulnerabilidades" OR "vulnerability prediction") AND ("métricas" OR metrics) AND ("aprendizado de máquina" OR "machine learning")

# E2 · ferramentas SAST
("análise estática" OR "static analysis" OR SAST) AND (segurança OR security) AND (Java OR "código aberto" OR "open source")

# E6 · setor público
("governo eletrônico" OR "e-government" OR "setor público" OR "software público") AND (segurança OR security) AND ("código-fonte" OR "source code")
```

---

## 4. Artigos encontrados

### 4.1 ICISSP (todos confirmados pelo rodapé do PDF ou pela fonte no OpenAlex)

**Mais próximos do trabalho**

1. **Predicting Attack Prone Software Components using Repository Mined Change Metrics**. Hein & Saiedian, **2016**. [DOI](https://doi.org/10.5220/0005812905540563). O mais próximo do desenho do TCC: prevê componentes propensos a ataque usando métricas mineradas do controle de versão, como as features do PyDriller.
2. **Machine Learning Based Prediction of Vulnerability Information Subject to a Security Alert**. Watanabe, Matsunaka, Kubota, Urakawa, **2023**. [DOI](https://doi.org/10.5220/0011613700003405). Compara Regressão Logística, Random Forest e XGBoost com ROC-AUC e PR-AUC; serve de referência no ICISSP para os modelos usados e para justificar PR-AUC em base desbalanceada.
3. **Prioritization of Exploit Codes on GitHub for Better Vulnerability Triage**. Kita et al., **2025**. [DOI](https://doi.org/10.5220/0013100800003899). Mostra que o GitHub tem códigos diferentes mas semanticamente duplicados e propõe deduplicá-los, o que apoia o achado de vazamento entre forks.
4. **DeDup.js: Discovering Malicious and Vulnerable Extensions by Detecting Duplication**. Picazo-Sanchez, Algehed, Sabelfeld, **2022**. [DOI](https://doi.org/10.5220/0010900600003120). Trata recursos de terceiros copiados (bibliotecas JS) em cada artefato, análogo ao jQuery UI copiado dentro do SIGA.
5. **Enhancing Continual Learning for Software Vulnerability Prediction**. Dou, Bahşi, Guerra-Manzanares, **2026**. [DOI](https://doi.org/10.5220/0014640400004061). Critica divisões aleatórias de treino/teste que "superestimam o desempenho real", o mesmo argumento do GroupKFold e da crítica ao vazamento.
6. **Optimizing Leak Detection in Open-source Platforms with Machine Learning Techniques**. Lounici et al., **2021**. [DOI](https://doi.org/10.5220/0010238101450159). Segredos no GitHub e o problema de falsos positivos dos scanners de regex; fundamenta a fase Gitleaks + detect-secrets.
7. **An Asynchronous Federated Learning Approach for a Security Source Code Scanner**. Kall & Trabelsi, **2021**. [DOI](https://doi.org/10.5220/0010300305720579). Scanner de segredos com ML e a falta de dados rotulados para treiná-lo.
8. **Windows Malware Binaries in C/C++ GitHub Repositories**. La Cholter, Elder, Stalick, **2021**. [DOI](https://doi.org/10.5220/0010237904750484). Estudo de mineração de segurança em 1.835 repositórios; mostra que o ICISSP aceita metodologia MSR.

**SAST e análise estática**

9. **CASTL: A Composable Source Code Query Language for Security and Vulnerability Analysis**. Johnson & Simha, **2025**. [DOI](https://doi.org/10.5220/0013176200003899). Consultas sobre árvores sintáticas (AST) para auditoria de segurança, a mesma família do CodeQL.
10. **Real-Time Detection of Multi-File DOM-Based XSS Vulnerabilities Using Static Analysis**. Kanaoka & Hiura, **2025**. [DOI](https://doi.org/10.5220/0013109300003899). SAST para XSS (CWE-79) entre arquivos, perfil web parecido com o do GOV.BR; aponta a falta de datasets.
11. **Cryptographic Vulnerability Detection in Code: A Hybrid Syntactic and Semantic Analysis Framework**. Vellamchety et al., **2026**. [DOI](https://doi.org/10.5220/0014393100004061). Contrasta casamento de padrões com fluxo de dados e controle, o mesmo contraste Semgrep × CodeQL.
12. **A Lightweight Static Analysis Method for Identifying Hardcoded Vulnerabilities in Android Applications**. Kanaoka, **2026**. [DOI](https://doi.org/10.5220/0014576500004061). Valores fixos no código encontrados por análise estática em escala; discute o custo de processar bibliotecas de terceiros.
13. **Comparing the Detection of XSS Vulnerabilities in Node.js and a Multi-tier JavaScript-based Language via Deep Learning**. Maurel, Vidal, Rezk, **2022**. [DOI](https://doi.org/10.5220/0010980800003120). Constrói 144 modelos para XSS e discute dataset e representação do código.
14. **The Comparison of Word Embedding Techniques in RNNs for Vulnerability Detection**. Nguyen et al., **2021**. [DOI](https://doi.org/10.5220/0010232301090120). Abordagem por texto do código, que serve de contraponto à abordagem por métricas.

**CVE, CWE e dependências**

15. **Security Issue Classification for Vulnerability Management with Semi-supervised Learning**. Wåreus et al., **2022**. [DOI](https://doi.org/10.5220/0010813000003120). Vulnerabilidades em bibliotecas open source e cobertura incompleta do NVD; conecta com a fase OSV.
16. **Vulnerabilities in IoT Devices, Backends, Applications, and Components**. Kaksonen, Halunen, Röning, **2023**. [DOI](https://doi.org/10.5220/0011784400003405). Análise quantitativa de CVE/CWE/CVSS; modelo para a seção de perfil de CWEs.
17. **The Common Vulnerability Scoring System vs. Rock Star Vulnerabilities**. Fall & Kadobayashi, **2019**. [DOI](https://doi.org/10.5220/0007387704050411). Limitações do CVSS; o CVSS médio é usado em `comparative_report.md`.
18. **Identifying Personal Data Processing for Code Review**. Tang, Østvold, Bruntink, **2023**. [DOI](https://doi.org/10.5220/0011725700003405). Análise estática voltada à confidencialidade e privacidade.

**Setor público**

19. **Cybersecurity Maturity Assessment of the Northern Portugal: A NIST CSF–Aligned Baseline of SMEs and Public Bodies**. Silva et al., **2026**. [DOI](https://doi.org/10.5220/0014252900004061). Diagnóstico de segurança em órgãos públicos (108 organizações).
20. **Cloud Inspector**. Diener & Bolz, **2023**. [DOI](https://doi.org/10.5220/0011694900003405). Gestão de segurança da informação em administrações públicas.

**Premiados do ICISSP próximos ao tema:**
- Heid et al. **2025** (Best Paper): análise estática nos 1.000 apps mais populares do Google Play.
- Heid et al. **2023** (Best Paper): análise estática de agilidade criptográfica em apps.
- Rosay et al. **2022** (Best Student): mostra falhas num dataset muito usado (CIC-IDS2017) e como elas afetam os resultados de ML. É o **modelo narrativo mais parecido com o achado dos forks**.
- Pacheco & Sun **2021** (Best Paper): estudo comparativo de modelos de ML.

**Outros eventos da SciTePress (não são ICISSP; não citar como ICISSP):**
- Halepmollası et al., *A Comparison of Source Code Representation Methods to Predict Vulnerability Inducing Code Changes*, **ENASE 2023**. [PDF](https://www.scitepress.org/Papers/2023/118593/118593.pdf)
- Farrapo, Rodrigues, Monteiro, Machado (grupo brasileiro), *Evaluating the Use of Open-Source and Standalone SAST Tools… C/C++*, **ICEIS 2025**. [PDF](https://www.scitepress.org/Papers/2025/134835/134835.pdf)
- Moreira, Canedo et al. (UnB), *Cybersecurity Risk Assessment Through AHP…* (órgão federal brasileiro), **ICEIS 2025**. [PDF](https://www.scitepress.org/Papers/2025/131973/131973.pdf)
- Konygin et al., *Using Bigrams to Detect Leaked Secrets in Source Code*, **ENASE 2023**. [PDF](https://www.scitepress.org/Papers/2023/119836/119836.pdf)
- Wagner & Sametinger, *Using the Juliet Test Suite to Compare Static Security Scanners*, **SECRYPT 2014**. [PDF](https://www.scitepress.org/Papers/2014/50329/50329.pdf)
- Hosseini et al., *Automated Search for Leaked Private Keys on the Internet*, **ICSOFT 2022**. [PDF](https://www.scitepress.org/Papers/2022/113080/113080.pdf)

### 4.2 Outras bases (DOIs confirmados no OpenAlex; "cit." = citações no OpenAlex em 07/11/2026)

| Eixo | Referência | Relação com o trabalho |
|---|---|---|
| E1 | Shin, Meneely, Williams, Osborne (2011), *Evaluating Complexity, Code Churn, and Developer Activity Metrics…*, IEEE TSE. [10.1109/TSE.2010.81](https://doi.org/10.1109/TSE.2010.81), cit. 620 | Base da hipótese: complexidade, churn e atividade como preditores |
| E1 | Zimmermann, Nagappan, Williams (2010), *Searching for a Needle in a Haystack…*, ICST. [10.1109/ICST.2010.32](https://doi.org/10.1109/ICST.2010.32), cit. 216 | VPM clássico; poucos positivos (como os 1–2% do dataset) |
| E1 | Chowdhury & Zulkernine (2011), *Using complexity, coupling, and cohesion metrics…*, JSA. [10.1016/j.sysarc.2010.06.003](https://doi.org/10.1016/j.sysarc.2010.06.003), cit. 295 | Justifica CBO, LCOM e acoplamento do CK |
| E1 | Walden, Stuckman, Scandariato (2014), *Software Metrics vs Text Mining*, ISSRE. [10.1109/ISSRE.2014.32](https://doi.org/10.1109/ISSRE.2014.32), cit. 216 | Métricas × texto (já está no `.bib`) |
| E1 | Scandariato et al. (2014), *Predicting Vulnerable Software Components via Text Mining*, IEEE TSE. [10.1109/TSE.2014.2340398](https://doi.org/10.1109/TSE.2014.2340398), cit. 347 | Abordagem alternativa de referência |
| E1 | Morrison et al. (2015), *Challenges with applying vulnerability prediction models*, HotSoS. [10.1145/2746194.2746198](https://doi.org/10.1145/2746194.2746198), cit. 136 | Limites práticos dos VPMs, útil para a discussão |
| E1 | Siavvas et al. (2020), *Technical debt as an indicator of software security risk…*, Enterprise Inf. Systems. [10.1080/17517575.2020.1824017](https://doi.org/10.1080/17517575.2020.1824017), cit. 40 | Dívida técnica (sqale_index) × segurança com ML |
| E2 | Li et al. (2023), *Comparison and Evaluation on SAST Tools for Java*, ESEC/FSE. [10.1145/3611643.3616262](https://doi.org/10.1145/3611643.3616262), cit. 71 | Validade do rótulo Semgrep ∪ CodeQL |
| E2 | Johnson et al. (2013), *Why don't software developers use static analysis tools…*, ICSE. [10.1109/ICSE.2013.6606613](https://doi.org/10.1109/ICSE.2013.6606613), cit. 635 | Falsos positivos de SAST |
| E2/E6 | Nguyen-Duc et al. (2021), *On the adoption of static analysis for software security assessment – A case study of an open-source e-government project*, Computers & Security. [10.1016/j.cose.2021.102470](https://doi.org/10.1016/j.cose.2021.102470), cit. 42 | **SAST combinado em software de governo**, o mais próximo do Corpus 3 |
| E3 | Allamanis (2019), *The adverse effects of code duplication in machine learning models of code*, Onward!. [10.1145/3359591.3359735](https://doi.org/10.1145/3359591.3359735), cit. 321 | **Fundamenta diretamente o vazamento entre forks** |
| E3 | Lopes et al. (2017), *DéjàVu: a map of code duplicates on GitHub*, PACMPL. [10.1145/3133908](https://doi.org/10.1145/3133908), cit. 200 | Escala da duplicação no GitHub |
| E3 | Kalliamvakou et al. (2014), *The promises and perils of mining GitHub*, MSR. [10.1145/2597073.2597074](https://doi.org/10.1145/2597073.2597074), cit. 886 | Riscos de forks e seleção de repositórios |
| E3 | Jimenez et al. (2019), *…accounting for real-world labelling when predicting software vulnerabilities*, ESEC/FSE. [10.1145/3338906.3338941](https://doi.org/10.1145/3338906.3338941), cit. 86 | Avaliação realista de VPMs |
| E3 | Croft, Babar, Kholoosi (2023), *Data Quality for Software Vulnerability Datasets*, ICSE. [10.1109/ICSE48619.2023.00022](https://doi.org/10.1109/ICSE48619.2023.00022), cit. 231 | Duplicação e rótulos ruidosos em datasets de vulnerabilidade |
| E3 | Chakraborty et al. (2021), *Deep Learning Based Vulnerability Detection: Are We There Yet?*, IEEE TSE. [10.1109/TSE.2021.3087402](https://doi.org/10.1109/TSE.2021.3087402), cit. 970 | Desempenho irrealista causado por duplicatas e desbalanceamento |
| E3 | Tantithamthavorn et al. (2016), *Empirical Comparison of Model Validation Techniques…*, IEEE TSE. [10.1109/TSE.2016.2584050](https://doi.org/10.1109/TSE.2016.2584050), cit. 591 | Justifica o esquema de validação |
| E3 | Arp et al. (2022), *Dos and Don'ts of Machine Learning in Computer Security*, USENIX Security. [arXiv 2010.09470](https://arxiv.org/abs/2010.09470) (não confirmado no OpenAlex) | Armadilhas de avaliação: data snooping, viés de taxa-base |
| E5 | Meli, McNiece, Reaves (2019), *How Bad Can It Git?*, NDSS. [10.14722/ndss.2019.23418](https://doi.org/10.14722/ndss.2019.23418), cit. 133 | Segredos em repositórios públicos |
| E5 | Pashchenko et al. (2018), *Vulnerable open source dependencies: counting those that matter*, ESEM. [10.1145/3239235.3268920](https://doi.org/10.1145/3239235.3268920), cit. 129 | Validade dos CVEs declarados (OSV) |
| E5 | Decan, Mens, Constantinou (2018), *…security vulnerabilities in the npm package dependency network*, MSR. [10.1145/3196398.3196401](https://doi.org/10.1145/3196398.3196401), cit. 287 | SCA em ecossistemas |
| Base | Chidamber & Kemerer (1994), IEEE TSE [10.1109/32.295895](https://doi.org/10.1109/32.295895) · McCabe (1976) [10.1109/TSE.1976.233837](https://doi.org/10.1109/TSE.1976.233837) · Spadini et al. (2018), PyDriller [10.1145/3236024.3264598](https://doi.org/10.1145/3236024.3264598) · Ghaffarian & Shahriari (2017), ACM CSUR [10.1145/3092566](https://doi.org/10.1145/3092566) | Fundamentação das métricas e um survey geral de ML para vulnerabilidades |

**Brasil (SBC OpenLib e UnB):**
- Sousa et al., *Mapeamento Sistemático de Comparativos de Ferramentas de Análise Estática de Código com Foco na Segurança*, SBSeg 2025 (anais estendidos). [10.5753/sbseg_estendido.2025.11875](https://doi.org/10.5753/sbseg_estendido.2025.11875)
- Campos et al., *Testes de Segurança Estáticos na Esteira de Desenvolvimento de Aplicações: Um Estudo de Caso na SEPLAG-CE*. [SOL](https://sol.sbc.org.br/index.php/sbseg_estendido/article/view/41953). SAST (Semgrep) num **órgão público brasileiro**.
- Pimentel & Progetti, *Avaliação comparativa… IAs generativas e ferramentas tradicionais… JavaScript*, SBSeg 2025. [10.5753/sbseg_estendido.2025.11655](https://doi.org/10.5753/sbseg_estendido.2025.11655)
- Chaves (2023), *Segurança de software open source: impacto das melhores práticas nos indicadores de vulnerabilidade do código*, TCC UnB. [BDM](https://bdm.unb.br/bitstream/10483/39345/1/2023_JoaoPedroAlvesSilvaChaves_tcc.pdf)

---

## 5. Artigos premiados do ICISSP

**Método:** a página de prêmios lista 34 artigos com DOI (2015–2026) e mais 3 prêmios de PhD Project **sem artigo publicado**, que não foram analisados. Os **34 PDFs completos** foram baixados da SciTePress e as medidas extraídas por script, com estas ressalvas:
- **Referências:** contagem automática (≈). Nos casos em que o Semantic Scholar tem a contagem, ela bate com a do script com diferença de ±3 na maioria.
- **Citações:** o **Google Scholar bloqueia consultas automáticas**. Foi usado o **OpenAlex** para os 34 e, depois da barra, o Semantic Scholar quando estava disponível. O Google Scholar costuma mostrar números maiores, então trate estes como piso. Artigos de 2026 ainda têm 0 citações por serem recentes.

**Legenda das seções:** I = Introdução · B = Background · RW = Trabalhos relacionados · TM = Modelo de ameaça · M = Método/projeto · E = Avaliação/resultados · D = Discussão · L = Limitações · C = Conclusão · ? = título não extraído do PDF.

| Título (abrev.) | Ano | Prêmio | Págs | Seções | Fig | Tab | Código | Palavras-chave | Refs | Citações OA / S2 |
|---|---|---|---|---|---|---|---|---|---|---|
| Avatar Motion Signatures | 2026 | Best Paper | 7 | 5: I→M→E+D→L→C | 4 | 2 | — | Re-Identification, Avatarization, Facial De-Identification, Linkability | ≈20 | 0 / 0 |
| Sequential Pattern Recognition Attacks… | 2026 | Best Student | 12 | 7: I→RW→M→E→E→D→C | 5 | 9 | Alg×1 | Privacy-Preserving Advertising, Re-Identification Attacks, Topics API, … (10) | ≈25 | 0 |
| Similarity Is Not Enough… (IDS) | 2026 | Best Poster | 8 | 7: I→RW→M→E→E→E→D | 5 | 1 | — | Intrusion Detection, Deep Learning, Adversarial Attacks, Denial of Service, Security | ≈20 | 3 |
| Revisiting Permission Piggybacking… | 2025 | Best Paper | 8 | 6: I→RW→M→M→E→C | 4 | 3 | — | Permission, Third-Party Libraries, Android, Static Analysis | ≈18 | 3 / 4 |
| CyLLM-DAP | 2025 | Best Student | 12 | 6: I→B+RW→M→M→E→C | 4 | 5 | — | Large Language Models (LLMs), Domain-Adaptive Pre-Training, … (5) | ≈33 | 0 |
| Randomizing Forger Selection (PoS) | 2025 | Best Poster | 8 | 8: I→M→M→B→M→E→E→C | 9 | 2 | — | Consensus Protocol, Blockchain, Proof-of-Stake, Decentralization | ≈20 | 0 / 0 |
| Supporting CAN Bus Anomaly Detection… | 2024 | Best Paper | 12 | 7: I→RW→B→TM→M→E→C | 8 | 2 | — | CAN, Anomaly Detection, TCN, Correlation | ≈23 | 3 |
| RoomKey | 2024 | Best Student | 12 | 7: I→M→M→E→E→D→C | 4 | 3 | — | Fuzzy Extraction from WiFi Data, Volatile Key Extraction, … (3) | ≈19 | 1 / 1 |
| Security and Privacy Risk Postures of Virtual Assistants | 2024 | Best Position | 8 | 7: I→RW→M→E→D→L→C | 1 | 2 | — | Virtual Assistants, Privacy and Security, Vulnerability Analysis, … (5) | ≈43 | 5 |
| Tracing Cryptographic Agility… | 2023 | Best Paper | 8 | 5: I→RW→M→E→C | 3 | 1 | — | Cryptography, Agility, Android, Static Analysis | ≈18 | 3 |
| Dark Ending | 2023 | Best Student | 12 | 6: I→RW→M→E→D→C | 7 | 3 | — | Cybercrime, Dark Web, … (8) | ≈30 | 5 / 4 |
| SCANTRAP | 2023 | Best Poster | 8 | 6: I→M→M→D→RW→C | 1 | 1 | — | CMS, Penetration Testing, Vulnerability Scanner, … (8) | ≈33 | 6 |
| Implementing Post-quantum Cryptography… | 2022 | Best Paper | 11 | 6: I→B→M→E→D→C | 0 | 4 | — | Post-quantum Cryptography, Lattice Cryptography, C++, Programming Library | ≈23 | 11 |
| Network Intrusion Detection: … CIC-IDS2017 | 2022 | Best Student | 12 | 8: I→RW→M→M→M→E→E→C | 1 | 4 | Alg×2 | Network Intrusion Detection, CIC-IDS2017, …, Machine Learning (7) | ≈28 | **97 / 93** |
| PREUNN | 2022 | Best Poster | 12 | 6: I→B→M→E→RW→C | 9 | 3 | — | Protocol Reverse Engineering, AI, Machine Learning, Neural Networks, Fuzzing | ≈33 | 14 / 11 |
| Adversarial ML: Comparative Study… IDS Datasets | 2021 | Best Paper | 12 | 7: I→B→RW→E→E→D→C | 10 | 9 | — | Adversarial Machine Learning, Deep Learning, Deep Neural Networks, Intrusion Detection Datasets | ≈25 | 45 / 42 |
| Hydra | 2021 | Best Student | 13 | 6: I→TM→RW→M→E→C | 7 | 2 | — | Strong Anonymity, Onion Encryption, Circuits, Messaging | ≈23 | 2 / 6 |
| Remote WebAuthn | 2021 | Best Poster | 8 | 5: I→M→M→E→C | 6 | 2 | — | FIDO2, Security, Authentication, Remote, Webauthn | ≈13 | 9 / 6 |
| Host Fingerprinting… | 2020 | Best Paper | 7 | 5: I→RW→M→E→C | 7 | 0 | — | Authentication, Clock Skew, Database Security, Fingerprint | ≈18 | 0 |
| Secure Ownership Transfer for IoT | 2020 | Best Student | 12 | 8: I→RW→M→TM→?→E→E→C | 2 | 1 | — | IoT, Ownership Transfer, Constrained Devices | ≈30 | 3 |
| Kerberoasting… | 2020 | Best Poster | 8 | 4: I→B→M→C | 3 | 2 | List×5 | MS Active Directory, Kerberos Security, … (5) | ≈11 | 8 / 5 |
| Transparency within the GDPR | 2019 | Best Paper | 12 | 7: I→RW→M→M→M→D→C | 0 | 4 | — | Transparency, Transparency Enhancing Tools, GDPR, Compliance | ≈29 | 26 / 24 |
| Are You Ready When It Counts? | 2019 | Best Student | 12 | 6: I→M→M→M→D→C | 2 | 6 | — | Security Awareness, ISIM, IT Consulting, GDPR, NIS Directive | ≈25 | 8 |
| Business Process Modelling… Data Protection | 2019 | Best Poster | 8 | 6: I→B→M→E→RW→C | 5 | 0 | — | Business Processes, BPMN, GDPR, … (6) | ≈34 | 19 |
| Inferring Handwritten Patterns… | 2018 | Best Paper | 10 | 8: I→RW→M→E→M→E→D→C | 2 | 1 | Alg×1 | Smartphone Sensors, Handwritten Pattern, Dynamic Timing Warping, Majority Voting | ≈41 | 6 / 7 |
| App-based Matrix Code Authentication… | 2018 | Best Student | 12 | 6: I→M→M→M→M→C | 3 | 1 | — | Mobile Banking, App-based Authentication, Malware, PSD2, Compliance | ≈31 | 14 / 13 |
| Back to the Drawing Board | 2018 | Best Poster | 9 | 4: I→M→RW→D | 2 | 0 | — | Software Architecture, Security by Design, … (10) | ≈58 | 1 |
| Secure Wireless Channel for Implantable Medical Devices | 2017 | Best Paper | 10 | 7: I→M→M→M→M→E→C | 7 | 3 | — | Implantable Medical Devices, Security, … (12) | ≈24 | 5 / 5 |
| Attribute Permutation Steganography… | 2017 | Best Student | 6 | 6: I→RW→M→M→E→C | 0 | 3 | Alg×1 | Steganography, Attribute Permutation, Classification | ≈13 | 1 / 1 |
| Identity Deception Detection… | 2017 | Best Poster | 6 | 5: I→M→E→M→C | 2 | 2 | — | Deception, Big Data, Cyber Security, Social Media, Cyber Crime | ≈10 | 4 / 5 |
| Injecting CSP for Fun and Security | 2016 | Best Paper | 11 | 8: I→TM→M→M→E→D→RW→C | 6 | 1 | Alg×2 | Web Browser Security, CSP, XSS | ≈25 | 15 |
| Differential Security Evaluation of Simeck… | 2016 | Best Student | 11 | 5: I→M→M→M→C | 0 | 9 | Alg×1 | Simeck, Dynamic Key-guessing, Differential Cryptanalysis | ≈24 | 26 / 28 |
| Model-driven Privacy Assessment in the Smart Grid | 2015 | Best Paper | 9 | 5: I→RW→M→E→C | 3 | 0 | — | Smart Grid, Privacy, Model-based, Assessment | ≈22 | 13 |
| Anonymous Authenticated Key Agreement for VANETs | 2015 | Best Student | 11 | 6: I→M→RW→M→E→C | 6 | 1 | — | Anonymous Authentication, VANETs, Key Agreement, Ring Signatures | ≈17 | 12 / 15 |

Os DOIs de todos estão na lista de [Previous Awards](https://icissp.scitevents.org/PreviousAwards.aspx).

### Estatísticas (34 artigos)

| Medida | Mín. | Máx. | Média | Mediana |
|---|---|---|---|---|
| **Referências** (todos) | 10 | 58 | **25,3** | 24 |
| Referências: só Best Paper (12) | 18 | 41 | 23,8 | 23 |
| Referências: só Best Student (12) | 13 | 33 | 24,8 | 25 |
| **Citações recebidas** (OpenAlex, todos) | 0 | 97 | **10,8** | 5 |
| Citações: só Best Paper | 0 | 45 | 10,8 | 5,5 |
| Citações: só Best Student | 0 | 97 | 14,1 | 4 |
| Páginas | 6 | 13 | 9,9 | 10,5 |
| Seções numeradas | 4 | 8 | 6,2 | 6 |
| Figuras | 0 | 10 | 4,1 | 4 |
| Tabelas | 0 | 9 | 2,7 | 2 |
| Palavras-chave | 3 | 12 | 5,1 | 4 |

### O que os premiados fazem de diferente

- **Espaço por seção** (média em % do texto): Introdução 11% · Background/Trabalhos relacionados 13% · Método 23% · Resultados 20% · Discussão 4% · Conclusão **só 3%** · Referências 12%.
  - Os trabalhos relacionados vêm logo após a introdução em 15 de 34 artigos; ficam no fim em 4; e 11 não têm uma seção separada (são absorvidos em Background).
- **Problema e contribuição:**
  - O padrão é parágrafos de contexto → lacuna → contribuições, muitas vezes enumeradas (Rosay et al. 2022: *"Our main contributions consist of four parts. First…"*) → parágrafo dizendo o que cada seção traz (em cerca de 15 de 34).
  - Perguntas de pesquisa (RQs) explícitas são raras: 3 de 34.
- **Limitações:**
  - Seção própria só em 2 artigos (2024 Position e 2026 Best Paper); 14 têm seção de Discussão.
  - Cerca de 18 mencionam limitações no texto e cerca de 23 citam trabalhos futuros.
  - **Nenhum usa "Threats to Validity"**, o padrão da área de Engenharia de Software/MSR.
- **Figuras:**
  - O tipo mais comum é o **diagrama geral do sistema ou pipeline como Figura 1 ou 2** (cerca de 13 artigos; ex.: *"Analysis tool flow chart"*, Heid 2025).
  - Depois vêm gráficos de resultado: curvas ROC (2021 BP, 2026 BP), CDFs, barras, heatmaps, t-SNE e matrizes de confusão.
  - Também aparecem diagramas de sequência ou protocolo e árvores de ataque.
  - As legendas são descritivas e se explicam sozinhas (2026 BP: *"ROC curves for three attack scenarios: the baseline attacker refM (AUC 0.921)…"*).
  - As figuras são referenciadas no texto em média 2 a 3 vezes cada.
- **Código:** quase nada. **27 de 34 não têm nenhum algoritmo nem listing.**
  - 6 usam algoritmos numerados em pseudocódigo (algorithm2e), geralmente só 1 ou 2.
  - 1 usa listings curtos marcados como *"(snippet)"* (Kerberoasting 2020).
  - O resto põe nomes de API em fonte monoespaçada dentro do texto (ex.: `checkPermission(...)` em Heid 2025).
- **Palavras-chave:** de 4 a 5, em Title Case, misturando área ampla e termos específicos. As que se repetem entre os premiados são *Security, Authentication, Machine Learning, Static Analysis, Android, Privacy by Design, Deep Learning, Adversarial Machine Learning*.
- **Citações:** o premiado mais citado (97) é justamente um **artigo que mostra falhas num dataset muito usado e como elas mudam os resultados de ML** (Rosay et al. 2022). Ele publicou a ferramenta e o dataset corrigido.

---

## 6. Comparação com o template (`Artigo_TCC/Template/Example.tex`)

| Aspecto | O template exige | O que os premiados fazem | Encaixa? / Adaptação |
|---|---|---|---|
| Tamanho | ICISSP: full paper até 12 págs, short até 8 (+4 pagas) ([GuideLines](https://icissp.scitevents.org/GuideLines.aspx)) | Mediana de 10,5; Best Student usa 12 | ✅ Mirar em 10–12 |
| Resumo | 70–200 palavras, 9 pt | Contexto → lacuna → proposta → resultado numérico | ✅ Pôr o número principal (ROC-AUC com e sem as dobras DSpace) |
| Palavras-chave | ≥1, Title Case, vírgulas, termina em ponto | 4–5 | ✅ |
| Seções | `\section{\uppercase{…}}`, subseções em Title Case | 6 seções numeradas | ⚠️ O roteiro "Introdução / Fundamentação / Metodologia / Resultados / Conclusão" cabe em 6 seções se a Fundamentação virar "Background and Related Work" (como 2018 BP e 2025 BSP) |
| Citações | APA autor-data (`apalike`), sem números | Igual | ⚠️ O `Artigo/main.tex` usa estilo SBC (`\citeonline`, numérico): **precisa ser convertido** |
| Autocitação | ≤ 20% | — | ✅ |
| Tabelas | Legenda **acima**, 9 pt; `table*` para duas colunas | Tabelas largas de resultado ocupam duas colunas | ✅ Usar `table*` para a tabela dos 5 modelos × 3 corpora |
| Figuras | Legenda **abaixo**, ≥300 dpi, `figure*` para duas colunas | Diagrama do pipeline + 2–4 gráficos | ⚠️ Gerar os PNGs de `reports/charts/` em 300 dpi (o script usa `dpi=150` em `ml_security_pipeline.py:274`) ou em PDF vetorial |
| Algoritmos | `algorithm2e` já incluído; legenda com ":" | 1–2 no máximo | ✅ Um algoritmo para a regra de rótulo + GroupKFold |
| Código | `verbatim` em 9 pt, alinhado à esquerda | Quase nunca usado | ✅ Evitar listar código Python |
| Idioma e revisão | Inglês; revisão duplo-cega; uso de IA declarado nos agradecimentos | — | ⚠️ Se for submeter ao ICISSP: escrever em inglês, anonimizar o link do repositório e declarar o uso de IA. Para o TCC, confirmar o idioma com o orientador |
| Limitações | Não exigidas | Raramente têm seção própria | ➕ Diferencial possível: "Threats to Validity" (ver abaixo) |

---

## 7. Recomendações práticas

1. **Fazer do vazamento entre forks a contribuição principal**, no modelo de Rosay et al. 2022 (o premiado mais citado): "mostramos que forks quase idênticos inflam o ROC-AUC de 0,83 para 0,91 mesmo com GroupKFold". Fundamentar com Allamanis (2019), Lopes et al. (2017) e Croft et al. (2023).
2. **Introdução** em cerca de 1 página: contexto → lacuna → 3 ou 4 contribuições numeradas → parágrafo dizendo o que cada seção traz.
3. **Seis seções:** Introduction · Background and Related Work · Methodology (pipeline, corpora, rótulo, validação) · Results · Discussion and Threats to Validity · Conclusion. A conclusão deve ser curta, cerca de 3% do texto.
4. **Figura 1 = diagrama do pipeline de 13 fases**, como fazem cerca de 13 premiados. Usar mais 3 ou 4 figuras de resultado (ROC ou o gráfico de halteres dos 3 corpora, densidade por KLOC, precisão por dobra) e 2 ou 3 tabelas.
5. **Código mínimo:** no máximo um `algorithm` (rótulo Semgrep ∪ CodeQL + GroupKFold + SMOTE só nas dobras de treino). Nomes de ferramentas e flags (`--build-mode=none`) em fonte monoespaçada no texto.
6. **Incluir "Threats to Validity"** (construto: SAST como rótulo; interna: forks e código de terceiros; externa: 30 repositórios Java). Nenhum premiado do ICISSP faz isso, e é o padrão em MSR.
7. **De 25 a 30 referências** (média dos premiados: 25; faixa: 10–58), em APA. Hoje o `.bib` tem cerca de 15 obras acadêmicas mais entradas `@misc` dos repositórios NSA; Shin, Zimmermann e Walden já estão lá.
8. **Palavras-chave (4–6), sugestão:** *Software Vulnerability Prediction, Static Application Security Testing, Mining Software Repositories, Machine Learning, Data Leakage, ISO/IEC 25010.*
9. **Disponibilizar o pipeline e o dataset**, como fazem os premiados com artefato. Na submissão às cegas, usar um link anonimizado.
10. **Resultados numéricos no resumo e nas legendas**: os premiados citam o valor principal já no resumo e nas legendas.

---

### Limites deste levantamento

- Citações vêm do OpenAlex/Semantic Scholar, não do Google Scholar (bloqueado para consultas automáticas).
- A contagem de referências e as porcentagens de espaço por seção são automáticas e aproximadas (±10%).
- Não foram encontrados artigos relevantes no SciELO.
- Não foi confirmado se a caixa de busca da SciTePress Digital Library aceita operadores booleanos.

### Fontes

- ICISSP: [Previous Awards](https://icissp.scitevents.org/PreviousAwards.aspx) · [Proceedings](https://icissp.scitevents.org/BooksPublishedScitepress.aspx) · [GuideLines](https://icissp.scitevents.org/GuideLines.aspx)
- APIs: [OpenAlex](https://api.openalex.org) · [Semantic Scholar API](https://api.semanticscholar.org)
- Artigos da SciTePress fora do ICISSP: [ICEIS 2025 SAST](https://www.scitepress.org/Papers/2025/134835/134835.pdf) · [ENASE 2023](https://www.scitepress.org/Papers/2023/118593/118593.pdf)
- SBC OpenLib: [SBSeg 2025 mapeamento](https://sol.sbc.org.br/index.php/sbseg_estendido/article/view/36762) · [SEPLAG-CE](https://sol.sbc.org.br/index.php/sbseg_estendido/article/view/41953) · [TCC UnB](https://bdm.unb.br/bitstream/10483/39345/1/2023_JoaoPedroAlvesSilvaChaves_tcc.pdf)
- Outros: [Arp et al. (arXiv)](https://arxiv.org/abs/2010.09470) · [Nguyen-Duc et al. e-government (arXiv)](https://arxiv.org/pdf/2103.08010)
