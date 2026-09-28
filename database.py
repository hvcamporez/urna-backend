import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_SCHEMA = os.getenv("SUPABASE_SCHEMA", "urna")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError(
        "Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no arquivo .env "
        "(veja .env.example)."
    )

# ATENÇÃO: a service_role key ignora o RLS do Supabase.
# Ela só pode existir aqui, no backend. NUNCA no frontend/Lovable.
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def db():
    """
    Retorna o client apontando para o schema 'urna' (não o 'public').
    Use db().table(...) / db().rpc(...) em vez de supabase.table(...)
    em todos os routers.
    """
    return supabase.schema(SUPABASE_SCHEMA)
