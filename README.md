# Data Cleaning & Segmentation with Python

Projeto em Python para limpeza, padronização, deduplicação e segmentação de bases cadastrais.

A ideia aqui é reproduzir, com dados fictícios, um tipo de trabalho que faço com frequência em bases operacionais: receber arquivos com formatos inconsistentes, corrigir os campos, eliminar duplicidades e gerar grupos prontos para análise ou campanhas.

## O que o pipeline faz

- padroniza nomes de colunas;
- normaliza e-mails;
- remove registros sem e-mail válido;
- elimina duplicidades por e-mail;
- trata empresa, cargo e segmento;
- classifica cargos em proprietário, diretor, gerente ou outros;
- cria flags de interesse por segmento;
- gera um resumo com indicadores da base;
- exporta uma base limpa em CSV.

## Estrutura

```text
data/
  sample_contacts.csv

src/
  pipeline.py

output/
  gerado ao executar o projeto
```

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
python src/pipeline.py
```

O script lê `data/sample_contacts.csv` e gera:

- `output/contacts_clean.csv`
- `output/summary.csv`

## Exemplo de regras

A classificação de cargo usa o início do texto normalizado:

- `PROP...` → Proprietário
- `DIR...` → Diretor
- `GER...` → Gerente

Os dados deste repositório são fictícios e servem apenas para demonstração do pipeline.

## Stack

Python 3 + pandas
