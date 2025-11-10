# 🚀 Guia Rápido - API de Precificação de Imóveis

## ⚡ Início Rápido (3 Passos)

### **1. Instalar Dependências**
```powershell
pip install -r requirements.txt
```

### **2. Gerar Modelos**
```powershell
python mock_model_generator.py
```

### **3. Iniciar API**
```powershell
python main.py
```

✅ **Acesse:** http://127.0.0.1:8000/docs

---

## 📝 10 Endpoints Disponíveis

### **Previsão**
1. `POST /predict/venda` - Prever valor de venda
2. `POST /predict/aluguel` - Prever valor de aluguel
3. `POST /predict/imovel` - Prever venda + aluguel

### **Consulta**
4. `GET /tipos-imoveis` - Listar tipos
5. `GET /estados` - Listar estados
6. `GET /estados/{uf}/cidades` - Listar cidades
7. `GET /estados/{uf}/cidades/{cidade}/bairros` - Listar bairros

### **Monitoramento**
8. `GET /status` - Status da API
9. `GET /modelo/versao` - Versão dos modelos

### **Avançado**
10. `GET /estatisticas/{estado}/{cidade}/{bairro}` - Estatísticas do bairro

---

## 🧪 Teste Rápido

**1. Listar estados:**
```
http://127.0.0.1:8000/estados
```

**2. Prever valor (via Swagger):**
- Acesse: http://127.0.0.1:8000/docs
- Clique em `POST /predict/imovel`
- "Try it out"
- Cole:
```json
{
  "tipo_imovel": "apartamento",
  "bairro": "Pinheiros",
  "cidade": "São Paulo",
  "quartos": 2,
  "suites": 1,
  "vagas": 1,
  "area_util": 75.0
}
```
- "Execute"

---

## 📂 Arquivos do Projeto

```
├── models/                  # Modelos de ML (gerados)
├── main.py                  # API principal (10 endpoints)
├── schemas.py               # Modelos Pydantic
├── ml_service.py            # Serviço de ML
├── mock_db.py               # Banco de dados falso
├── mock_model_generator.py  # Gera modelos
├── requirements.txt         # Dependências
├── README_COMPLETO.md       # Documentação completa
└── GUIA_RAPIDO.md          # Este arquivo
```

---

## 🎯 Comandos Úteis

```powershell
# Instalar dependências
pip install -r requirements.txt

# Gerar modelos
python mock_model_generator.py

# Iniciar servidor
python main.py

# Iniciar com reload automático
uvicorn main:app --reload

# Iniciar em outra porta
uvicorn main:app --port 8001

# Ver documentação
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc
```

---

## ✅ Checklist

- [ ] Instalei as dependências
- [ ] Gerei os modelos (`mock_model_generator.py`)
- [ ] Iniciei o servidor (`python main.py`)
- [ ] Acessei o Swagger (http://127.0.0.1:8000/docs)
- [ ] Testei um endpoint de predição
- [ ] Testei um endpoint de consulta
- [ ] Verifiquei o status da API

---

**💡 Dica:** Use o Swagger UI para testar todos os endpoints de forma visual e interativa!

