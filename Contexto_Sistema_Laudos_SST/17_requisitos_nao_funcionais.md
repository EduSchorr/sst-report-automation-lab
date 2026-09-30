# Requisitos Não Funcionais — Segurança, Privacidade e Confiabilidade

## 1. Segurança e privacidade

- Tráfego protegido em implantações de rede.
- Tratamento mínimo necessário de dados pessoais.
- Controle de acesso por papéis.
- Separação entre dados de produção, corpus de pesquisa e exemplos de demonstração.
- Segredos e credenciais fora do repositório.

## 2. Desempenho

- Geração de documentos deve ocorrer em tempo compatível com uso interativo.
- OCR de documentos grandes deve ser executado fora do fluxo principal quando necessário.
- Imagens e anexos devem ser tratados de forma eficiente.

## 3. Confiabilidade

- Backup e restauração da base local.
- Rastreabilidade das regras e fórmulas utilizadas.
- Logs de erro e validação de integridade.
- Capacidade de reprocessar o corpus sem duplicar documentos já identificados por hash.
