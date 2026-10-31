# My Profit

Calculadora de lucro para pequenos comerciantes e vendedores autônomos. Calcula lucro, margem e markup de cada produto, sugere o preço ideal de venda e mostra um ranking dos produtos mais lucrativos.

Projeto open source (licença MIT) desenvolvido na UNIFACISA, no curso de Análise e Desenvolvimento de Sistemas.

## Tecnologias

- **Front-end:** React, Vite e Recharts
- **Back-end:** Python com FastAPI e SQLAlchemy
- **Banco de dados:** SQLite no desenvolvimento local e PostgreSQL em produção
- **Autenticação:** JWT com senha em hash

## Como rodar (desenvolvimento)

> Em construção. Os comandos abaixo serão válidos conforme o código for sendo adicionado.

```text
# back-end
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload

# front-end
cd frontend
npm install
npm run dev
```

Copie `.env.example` para `.env` antes de iniciar.

## Documentação

- `docs/registro-ia.md`: registro de utilização da IA durante o desenvolvimento

## Licença

MIT. Veja o arquivo `LICENSE`.
