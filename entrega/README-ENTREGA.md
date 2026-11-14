# Entrega — Consolidador de reservas de hotel (Onfly)

## Defeitos corrigidos

1. **Conversão de câmbio invertida e com `float`** (`services/currency_converter.py`).
2. **Cálculo de noites usando apenas o dia do mês** (`services/stay_calculator.py`).
3. **Status `NO_SHOW` tratado como faturável** (`services/status_policy.py`).
4. **Ranking de hotéis em ordem crescente de valor** (`services/report_builder.py`).
5. **Desempate do ranking por `hotel_id` decrescente** (`services/report_builder.py`).
6. **Leitura do CSV interrompida na 200ª linha** (`repositories/csv_reservation_repository.py`).

## Causa raiz (uma frase por defeito)

1. O código dividia `amount` pela taxa e ainda passava por `float` antes de voltar para `Decimal`, em vez de multiplicar o valor exato pela taxa (`amount * rate_to_brl`).
2. A conta subtraía `checkout.day - checkin.day`, o que ignora a virada de mês/ano; o correto é subtrair as datas (`(checkout - checkin).days`).
3. A regra era `status != "CANCELLED"`, deixando `NO_SHOW` entrar nos totais, quando somente `CONFIRMED` é faturável.
4. O `sorted` sem `reverse` e sem chave negativa ordenava o valor de forma ascendente.
5. Ao usar `reverse=True` sobre a tupla `(amount, hotel_id)`, o desempate também era invertido, contrariando a regra de `hotel_id` ascendente.
6. Havia um `break` ao atingir 200 linhas, então as 100 reservas restantes do arquivo (300 no total) eram descartadas silenciosamente.

## Como investiguei e abordei o problema

1. Rodei `pytest -q` e usei a saída dos testes para localizar os módulos envolvidos (câmbio, noites, status e ranking).
2. Li cada serviço comparando a implementação com as regras de negócio do `README.md`, corrigindo os quatro defeitos iniciais.
3. Rodei o CLI na amostra `data/exemplo-validacao.csv` e conferi todos os números com a tabela de validação do enunciado.
4. Rodei o CLI no arquivo completo e percebi que `total_reservations` era 200, embora o CSV tivesse 300 linhas — daí o defeito de truncamento.
5. Auditei a ordenação de `top_hotels` contra a regra de desempate e corrigi a chave para `(-amount, hotel_id)`.
6. Adicionei quatro testes de regressão em `tests/test_extra_regressions.py` (arquivo novo; os cinco testes fornecidos não foram alterados): truncamento acima de 200 linhas, desempate do ranking, moeda em minúsculas e moeda sem taxa.
7. Validei o relatório completo com um cálculo independente em `Decimal`, comparando resumo, `by_month` e `top_hotels`.
8. Reforcei o contrato de erros: moeda sem taxa agora levanta `InputFileError` e o CLI retorna código `2` (entrada inválida), não `1`.

## Como validar

```bash
source .venv/bin/activate
pytest -q

# Amostra de validação do enunciado
PYTHONPATH=src python -m onfly_report \
  --input data/exemplo-validacao.csv \
  --rates data/taxas_cambio.csv \
  --output output/exemplo.json

# Base completa
PYTHONPATH=src python -m onfly_report \
  --input data/reservas_hoteis.csv \
  --rates data/taxas_cambio.csv \
  --output output/report.json --top 5
```

Na amostra, o relatório deve bater com o enunciado: 12 reservas, 9 confirmadas, 2 canceladas,
1 no-show, 28 noites, `7566.00` de total e `270.21` de média por noite.

Na base completa (300 linhas), o resultado observado é: 300 reservas, 235 confirmadas,
31 canceladas, 34 no-shows, 1.347 noites, `396170.00` de total e `294.11` de média por noite,
com `by_month` de 2024-12 a 2025-06.

## Resultado do `pytest`

```
.........                                                                [100%]
9 passed in 0.73s
```

São os 5 testes fornecidos (sem alteração) mais 4 testes de regressão adicionados.
`ruff check src tests` também passa sem avisos.
