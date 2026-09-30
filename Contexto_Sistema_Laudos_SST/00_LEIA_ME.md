# Pacote de Contexto Estruturado para o Sistema de Laudos e SST

Este pacote documenta o resultado de uma análise recursiva e estruturada de um grande acervo técnico de perícias judiciais, laudos de insalubridade, periculosidade, laudos previdenciários, LTCAT, PGR e SST.

> **Portfolio Edition:** o acervo original não é publicado neste repositório. Este documento preserva apenas o mapa conceitual do pacote de pesquisa.

## Objetivo do Pacote

Fornecer base documental, esquemas de dados, padrões de capítulos, catálogo de riscos, tabelas de medições quantitativas, modelos de quesitos, templates e regras de negócio para apoiar a construção de um sistema de geração assistida de laudos técnicos e previdenciários.

## Mapa conceitual dos artefatos

| Artefato | Tipo | Finalidade |
| :--- | :--- | :--- |
| Resumo executivo | Markdown | Visão da base documental e conclusões de engenharia |
| Catálogo de documentos | CSV | Metadados e hashes do acervo analisado |
| Tipos de documentos | JSON | Estruturas recorrentes por categoria |
| Estruturas de capítulos | JSON | Capítulos, variações e dependências |
| Campos de questionários | JSON | Mapeamento de dados de campo para o laudo |
| Modelo de dados | JSON | Entidades e relacionamentos sugeridos |
| Biblioteca de riscos | JSON | Catálogo de riscos físicos, químicos, biológicos e periculosidade |
| Biblioteca de textos | JSONL | Trechos técnicos anonimizados e reutilizáveis |
| Tabelas quantitativas | JSON | Estruturas para ruído, calor, vibração e agentes químicos |
| EPIs / EPCs / treinamentos | JSON | Catálogos de suporte |
| Quesitos | JSONL | Perguntas recorrentes por origem |
| Templates | Markdown | Convenções de geração de documentos |
| Regras de geração | Markdown | Regras condicionais para composição |
| Fluxo do sistema | Markdown | Pipeline ponta a ponta |
| Requisitos | Markdown | Requisitos funcionais e não funcionais |
| Alertas e validações | JSON | Regras de consistência |
| Estatísticas | JSON | Métricas consolidadas do estudo |

## Anonimização e conformidade

A edição pública não inclui os documentos originais. As ferramentas de pesquisa contêm rotinas para substituir identificadores como CPF, CNPJ, RG, PIS/NIT e número de processo por marcadores semânticos antes da geração de amostras.
