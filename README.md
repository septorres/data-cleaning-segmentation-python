# Limpeza e segmentação de contatos com Python

Este projeto é uma versão simplificada de uma rotina que uso em bases operacionais: receber um CSV com cadastros inconsistentes e gerar uma base mais organizada para análise ou campanhas.

Os contatos são fictícios. O objetivo é mostrar as regras de tratamento e facilitar a reprodução do exemplo, não simular uma plataforma completa.

## O que o script faz

1. Padroniza os nomes das colunas e remove espaços desnecessários.
2. Coloca os e-mails em letras minúsculas, filtra formatos inválidos e remove duplicidades por e-mail (mantendo o primeiro registro).
3. Classifica cargos em proprietário, diretor, gerente ou outros.
4. Marca interesses em alimentos, pizza, confeitaria e café com base nas colunas de setor e atividade.
5. Exporta o CSV tratado e um resumo com indicadores.

## Como executar

Requisitos: Python 3.10+.

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale a dependência:

```bash
pip install -r requirements.txt
python src/pipeline.py
```

O script lê `data/sample_contacts.csv` e cria dois arquivos na pasta `output/`:

- `contacts_clean.csv`: registros válidos, sem e-mails duplicados, com colunas de classificação;
- `summary.csv`: quantidade de registros, empresas, cargos e interesses.

Na base de exemplo, são **7 linhas de entrada** e **5 contatos na saída**: um registro tem e-mail inválido e outro é duplicado.

## Executar os testes

```bash
pip install -r requirements-dev.txt
python -m pytest
```

Os testes cobrem normalização, classificação de cargo, remoção de duplicados e validação das colunas esperadas.

## Estrutura

```text
data/sample_contacts.csv    # Dados fictícios
src/pipeline.py             # Tratamento e geração dos arquivos
tests/test_pipeline.py      # Testes das regras principais
requirements.txt            # Dependências de execução
requirements-dev.txt        # Dependências de teste
output/                     # Arquivos gerados localmente
```

## Decisões e limitações

- A deduplicação usa o e-mail como chave. Em bases reais, duas pessoas podem compartilhar um endereço; a regra precisa ser avaliada conforme o contexto.
- A verificação de e-mail é **sintática e simplificada**. Ela não confirma que o endereço existe ou recebe mensagens.
- A classificação de cargos é baseada em prefixos (por exemplo, `GER` para gerente), não em um modelo de linguagem.
- Os caminhos dos arquivos são fixos para deixar o exemplo fácil de executar. Uma evolução seria aceitar caminhos como parâmetros.
- Os indicadores mostram o resultado após a limpeza; não representam uma base corporativa real.

## Tecnologias

Python, pandas e pytest.
