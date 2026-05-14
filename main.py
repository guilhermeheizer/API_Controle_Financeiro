from fastapi import FastAPI
from Controllers.TipoCategoriaController import router as tipo_categoria_controller
from Controllers.CategoriaController import router as categoria_controller
from Controllers.DespesaController import router as despesa_controller
from Controllers.TransacaoControle import router as transacao_controller


app = FastAPI(title="API Controle Financeiro", version="1.0", description="API para controle financeiro pessoal")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Controle Financeiro!"}

app.include_router(tipo_categoria_controller)
app.include_router(categoria_controller)
app.include_router(despesa_controller)
app.include_router(transacao_controller)