> **Language:** English · [Português (Brasil)](README.pt-BR.md)

<div align="center">

# SST Report Automation Lab

### Python · corpus analysis · anonymization · document research

**Research utilities used to inspect, anonymize and structure a technical-report corpus before building a production report-generation workflow.**

![Python](https://img.shields.io/badge/Python-20232A?style=for-the-badge&logo=python&logoColor=3776AB)
![Documents](https://img.shields.io/badge/Document-Research-20232A?style=for-the-badge&logo=microsoftword&logoColor=2B579A)
![Portfolio Edition](https://img.shields.io/badge/Portfolio-Edition-20232A?style=for-the-badge)

</div>

---

## About

This repository documents the **research and preprocessing stage** that preceded a structured SST report-generation product.

The tooling was designed to study a large local corpus without publishing the corpus itself. It focuses on extracting recurring report structure, rules, headings, evidence patterns and anonymized samples that can later inform templates and automation.

## What it demonstrates

- local corpus inventory and metadata analysis;
- DOCX/PDF-oriented text extraction helpers;
- recurring rule and heading analysis;
- anonymization-oriented preprocessing;
- sample packaging for controlled review;
- dataset splitting and validation utilities;
- generation of system-context documentation from corpus findings;
- separation between research corpus and production application.

## Public scope

The public repository does **not** contain the original technical-report corpus, real case documents or client data.

Large internal packaging scripts that were only useful for moving private corpus subsets between development environments are intentionally omitted from the public edition. The repository keeps the reusable research/anonymization modules and the sanitized system-context documentation.

## Relationship to Peritus SST

This lab represents an earlier research layer. The resulting product workflow is represented separately in [Peritus SST](https://github.com/EduSchorr/peritus-sst).

## Running

Most utilities are standalone Python scripts and use local directories configured by command-line arguments or constants documented in the source.

Run the public validation suite with:

```bash
python -m unittest discover -s tests -v
```

## Privacy

No real case, claimant/respondent identity, production database, professional contact information or private document is included.

See [`PORTFOLIO_EDITION.md`](PORTFOLIO_EDITION.md).

---

<div align="center">Built by **Eduardo Lima** · [GitHub](https://github.com/EduSchorr)</div>
