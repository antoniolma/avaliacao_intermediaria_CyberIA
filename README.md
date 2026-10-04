# Avaliação Intermediária — Quanto custa um alerta?

Cibersegurança Aplicada com Inteligência Artificial · Insper 2026-2
**Antonio Almeida e Luka Figueiredo** · código `d23bda` · `random_state = 3527138017`

## Entregáveis

| arquivo | conteúdo |
|---|---|
| `avaliacao_d23bda.ipynb` | notebook executado de ponta a ponta, itens A a J |
| `relatorio_d23bda.pdf` | relatório de 6 páginas: respostas b.1 a i.2, parecer e gráficos |
| `saida/avaliacao_d23bda_rf.joblib` | Random Forest da Parte A (66 features, sem `alertas_ids`) |
| `saida/avaliacao_d23bda_teste.csv.gz` | teste temporal: 66 features + `ataque` + `Label` |

## Reproduzir

```bash
pip install -r requirements.txt
# coloque R2_d23bda.csv.gz e creditcard.csv.gz em dados/
jupyter lab avaliacao_d23bda.ipynb
```

Execução completa leva cerca de 90 s. Os datasets de entrada não são versionados.

Para recompilar o relatório:

```bash
python extrair_figuras.py && pdflatex relatorio_d23bda.tex
```

> **Ambiente.** O `requirements.txt` fixa o ambiente da dupla (Python 3.12, numpy 2.5.3,
> scikit-learn 1.9.1, xgboost 3.4.1). As saídas atualmente gravadas no notebook foram
> produzidas em Python 3.11.9 / numpy 1.26.4 / scikit-learn 1.9.0 / **xgboost 3.1.1** — a
> célula de ambiente registra isso. Os números da Parte A são idênticos nos dois (Random
> Forest é determinístico dado o `random_state`), mas a **Parte B não foi verificada sob
> xgboost 3.4.1**: reexecute o notebook no ambiente do `requirements.txt` antes da entrega e
> confira os itens G e H, em especial a diferença de PR-AUC entre os modelos, que é de
> apenas 0,0124.

## Decisões de método

- **Features (66)**: as 61 que sobram da limpeza do item e) do Roteiro 2, mais as 5 derivadas
  do item g). São razões linha a linha, sem estatística agregada, então criá-las antes do
  split não transfere informação do teste para o treino.
- **Split temporal da Parte A**: por `dia`, conforme o enunciado. Esse corte deixa 8 das 15
  classes fora do teste — a classe difícil entre elas, porque slowloris e Slowhttptest
  terminam cedo na quarta-feira. O item c) usa um split auxiliar por `(dia, Label)` só para
  essa medida; o modelo salvo e os arquivos de `saida/` não são alterados.
- **Convenção de decisão**: `p >= limiar` em toda a varredura. Os 102 fluxos com pontuação
  exatamente 0,5 contam como alerta, ao contrário de `predict()` — daí as 102 divergências
  reportadas no item c).
- **Parte B**: `Time` fora das features (no split temporal ele separa treino de teste por
  construção). O XGBoost aceita só sementes de 32 bits; usamos `RANDOM_STATE % (2**31 - 1)`.

## Verificações automáticas

O notebook falha em vez de reportar número errado: testes de borda de `varrer_limiares` e de
`wilson`, reconciliação independente do custo total em todos os limiares dos dois modelos,
asserções de que `alertas_ids` não entrou no modelo, de que treino e teste não se sobrepõem
nem invadem o futuro, e contagem do parecer contra o limite de 250 palavras.
