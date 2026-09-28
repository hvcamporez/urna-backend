# Backend — Simulação de Urna Eletrônica

API em Python (FastAPI) que centraliza as regras de negócio da votação
e é a única peça autorizada a escrever no banco (via `service_role key`
do Supabase, que ignora o RLS).

## Como rodar localmente

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edite o .env com a URL do seu projeto e a service_role key
# (Supabase > Project Settings > API)

uvicorn main:app --reload
```

A API sobe em `http://localhost:8000`. Documentação automática (Swagger)
em `http://localhost:8000/docs` — ótimo para testar os endpoints antes
de ligar o frontend.

## Onde pegar as chaves no Supabase

Painel do projeto → **Project Settings** → **API**:
- `Project URL` → `SUPABASE_URL`
- `service_role` (em "Project API keys") → `SUPABASE_SERVICE_KEY`

**Nunca** coloque a `service_role key` no Lovable/frontend. Ela dá acesso
total ao banco, ignorando toda a segurança (RLS). Só o backend pode tê-la.

## Schema dedicado ("urna")

As tabelas deste projeto ficam no schema `urna`, não no `public`. Isso
exige um passo manual único, feito uma vez no painel do Supabase (não
dá pra fazer isso pelo SQL Editor):

1. `Project Settings` → `API` → `Data API` → **Exposed schemas**
2. Adicione `urna` à lista (o `public` já vem por padrão)
3. Salve

Sem esse passo, a API do Supabase não enxerga as tabelas do schema
`urna`, mesmo que elas já existam no banco — e o backend vai receber
erro dizendo que a tabela não foi encontrada.

O backend já está configurado para usar esse schema automaticamente
(variável `SUPABASE_SCHEMA=urna` no `.env`).

## Endpoints principais

| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/login` | Identifica o eleitor pela matrícula |
| GET | `/votacao/candidatos/{cargo_id}` | Lista candidatos de um cargo |
| GET | `/votacao/sessao/{turma_id}` | Status da sessão de votação da turma |
| POST | `/votacao/votar` | Registra o voto (atômico e sigiloso) |
| POST | `/mesario/sessao/abrir` | Abre a sessão de votação da turma |
| POST | `/mesario/sessao/fechar` | Fecha a sessão de votação da turma |
| GET | `/apuracao/resultado/{cargo_id}` | Totaliza os votos de um cargo |

## Deploy (para o Lovable conseguir chamar a API)

Durante o desenvolvimento, pode usar `ngrok http 8000` para expor o
localhost temporariamente. Para uma versão "de verdade" rodando o tempo
todo, opções gratuitas/simples: **Render**, **Railway** ou **Fly.io** —
todas sobem um projeto FastAPI a partir deste mesmo repositório, só
configurando as variáveis de ambiente do `.env` no painel do serviço.
