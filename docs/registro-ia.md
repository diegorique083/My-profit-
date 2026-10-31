# Registro de utilização da IA

Cada entrada documenta um uso relevante de IA: ferramenta, objetivo, prompt, resposta, o que foi revisado ou corrigido por mim e a decisão tomada.

## Modelo de entrada

```text
### NNN — Título curto
- Data:
- Ferramenta:
- Objetivo:
- Prompt (resumo ou trecho):
- Resposta gerada (resumo):
- Intervenção humana (o que revisei, corrigi ou recusei):
- Decisão técnica:
```

## Entradas

### 001 — Levantamento de requisitos (Fase 1)
- Data: 31/10/2026
- Ferramenta: Claude (chat)
- Objetivo: transformar a ideia de uma calculadora de lucro em requisitos e backlog
- Prompt (resumo): descrição do problema, público (pequeno comerciante), custos a considerar e diferencial visual
- Resposta gerada (resumo): Documento de Visão, requisitos funcionais e não funcionais, histórias de usuário e backlog
- Intervenção humana: incluí o cálculo por markup e por margem, defini a tela inicial com duas opções (lucro ou preço ideal) e removi a busca de produtos na web e as fotos, para manter o sistema prático e sem API externa
- Decisão técnica: MVP com login, cálculos, gestão de produtos, gráfico e ranking

### 002 — Erro encontrado no protótipo da calculadora (Fase 2)
- Data: 31/10/2026
- Ferramenta: Claude (chat)
- Objetivo: prototipar a calculadora de lucro com cálculo ao vivo
- Resposta gerada (resumo): protótipo interativo com campo de taxa do marketplace preenchido com 10 por padrão
- Intervenção humana: ao testar com custo 250 e preço 300, percebi que o lucro esperado era 50 e margem 16,67%, mas o protótipo mostrava 40 e 13,3%. A causa era um custo oculto (taxa padrão de 10)
- Decisão técnica: todos os campos de custo começam vazios; percentuais exibidos com duas casas decimais; esse caso virou teste obrigatório das fórmulas
