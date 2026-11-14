# Declaração de uso de IA

## Ferramenta e modelo

- **Ferramenta:** OpenCode (agente de código em CLI).
- **Modelo:** Big Pickle (provider `opencode`).

## O que a IA fez

- Revisou o diff e o código do CLI em busca de defeitos não cobertos pelos testes fornecidos.
- Identificou e corrigiu dois defeitos adicionais: truncamento da leitura do CSV em 200 linhas e desempate incorreto do ranking de hotéis.
- Adicionou dois testes de regressão em `tests/test_extra_regressions.py`.
- Executou os testes, o lint e o CLI na amostra e na base completa, validando os valores com um cálculo independente.
- Redigiu o `README-ENTREGA.md` e este registro de sessão.

## O que o candidato fez

- Investigou os quatro defeitos iniciais e implementou as correções de câmbio, noites, status e ordenação.
- Rodou os testes fornecidos até os 5 passarem.
- Solicitou a revisão final e a conferência do enunciado.
- Definiu o escopo da entrega e é responsável pela revisão e submissão do resultado.
