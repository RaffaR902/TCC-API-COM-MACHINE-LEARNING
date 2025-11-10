# 🏠 API de Precificação de Imóveis - Documentação Completa

## 📁 Estrutura do Projeto

```
api_precificacao_completa/
│
├── models/                     # Pasta para modelos de ML
│   ├── venda_pipeline.joblib   # (será gerado)
│   └── aluguel_pipeline.joblib # (será gerado)
│
├── schemas.py                  # Define todos os inputs/outputs da API
├── ml_service.py               # Carrega modelos e faz predições
├── mock_db.py                  # Simula um DB (estados, cidades, bairros)
├── main.py                     # API FastAPI com todos os endpoints
├── mock_model_generator.py     # Gera os modelos falsos de ML
├── requirements.txt            # Dependências do projeto
└── README_COMPLETO.md          # Este arquivo
```

---

## 🚀 Passo a Passo - Instalação e Execução

### **Passo 1: Instalar Dependências**

Abra o PowerShell na pasta do projeto e execute:

```powershell
pip install -r requirements.txt
```

**OU** se `pip` não funcionar, tente:

```powershell
python -m pip install -r requirements.txt
```

**OU** se ainda não funcionar:

```powershell
py -m pip install -r requirements.txt
```

As dependências instaladas serão:
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `pydantic` - Validação de dados
- `scikit-learn` - Machine Learning
- `pandas` - Manipulação de dados
- `joblib` - Serialização de modelos
- `requests` - Para testes HTTP

---

### **Passo 2: Gerar os Modelos Falsos**

**IMPORTANTE:** Execute este comando antes de iniciar a API:

```powershell
python mock_model_generator.py
```

**OU**:

```powershell
py mock_model_generator.py
```

Você verá a mensagem:
```
✅ Modelos falsos (v2) criados em 'models/'
```

Isso criará dois arquivos na pasta `models/`:
- `venda_pipeline.joblib`
- `aluguel_pipeline.joblib`

---

### **Passo 3: Iniciar o Servidor da API**

Execute o comando:

```powershell
python main.py
```

**OU**:

```powershell
py main.py
```

**OU** usando uvicorn diretamente:

```powershell
uvicorn main:app --reload
```

Você verá algo como:
```
LOG: Modelos (v1.0.3) carregados com sucesso.
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

✅ **Sua API está rodando!**

---

## 📚 Endpoints Disponíveis

A API possui **10 endpoints** organizados em 4 categorias:

### 🔹 **1. Endpoints de Previsão**

#### **POST /predict/venda**
Retorna o valor previsto de **venda** de um imóvel.

**Body (JSON):**
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

**Resposta (200):**
```json
{
  "valor_previsto_venda": 750000.00
}
```

---

#### **POST /predict/aluguel**
Retorna o valor previsto de **aluguel** de um imóvel.

**Body (JSON):** (mesmo do endpoint de venda)

**Resposta (200):**
```json
{
  "valor_previsto_aluguel": 2800.00
}
```

---

#### **POST /predict/imovel**
Retorna valores previstos de **venda e aluguel** para o imóvel.

**Body (JSON):** (mesmo dos anteriores)

**Resposta (200):**
```json
{
  "valor_previsto_venda": 750000.00,
  "valor_previsto_aluguel": 2800.00
}
```

---

### 🔹 **2. Endpoints de Consulta**

#### **GET /tipos-imoveis**
Lista os tipos de imóveis suportados.

**Resposta (200):**
```json
{
  "tipos_disponiveis": ["apartamento", "casa", "cobertura", "loft"]
}
```

---

#### **GET /estados**
Lista os estados (UFs) disponíveis.

**Resposta (200):**
```json
{
  "estados": ["SP", "RJ", "MG"]
}
```

---

#### **GET /estados/{uf}/cidades**
Lista as cidades de um estado específico.

**Exemplo:** `GET /estados/SP/cidades`

**Resposta (200):**
```json
{
  "estado": "SP",
  "cidades": ["São Paulo", "Campinas", "Santos"]
}
```

**Resposta (404):** Se o estado não existir
```json
{
  "detail": "Estado (UF) 'XX' não encontrado."
}
```

---

#### **GET /estados/{uf}/cidades/{cidade}/bairros**
Lista os bairros de uma cidade específica.

**Exemplo:** `GET /estados/SP/cidades/São Paulo/bairros`

**Resposta (200):**
```json
{
  "estado": "SP",
  "cidade": "São Paulo",
  "bairros": ["Pinheiros", "Moema", "Tatuapé", "Vila Madalena"]
}
```

**Nota:** O nome da cidade deve estar codificado na URL (use `%20` para espaços).

---

### 🔹 **3. Endpoints de Monitoramento**

#### **GET /status**
Verifica o status da API e dos modelos.

**Resposta (200):**
```json
{
  "status": "ok",
  "versao": "1.0.0",
  "modelo_atualizado": true
}
```

---

#### **GET /modelo/versao**
Retorna informações sobre a versão dos modelos de ML.

**Resposta (200):**
```json
{
  "versao_modelo": "1.0.3",
  "ultima_atualizacao": "2025-08-15"
}
```

---

### 🔹 **4. Endpoints Avançados**

#### **GET /estatisticas/{estado}/{cidade}/{bairro}**
Retorna estatísticas agregadas para um bairro específico.

**Exemplo:** `GET /estatisticas/SP/São Paulo/Pinheiros`

**Resposta (200):**
```json
{
  "estado": "SP",
  "cidade": "São Paulo",
  "bairro": "Pinheiros",
  "media_venda": 950000.0,
  "valor_minimo_venda": 650000.0,
  "valor_maximo_venda": 1500000.0,
  "media_aluguel": 3800.0,
  "valor_minimo_aluguel": 2500.0,
  "valor_maximo_aluguel": 5500.0
}
```

**Resposta (404):** Se o bairro não tiver dados
```json
{
  "detail": "Dados não disponíveis para o bairro 'XYZ'."
}
```

---

## 🧪 Como Testar a API

### **Opção 1: Swagger UI (Recomendado) 🌐**

1. Com o servidor rodando, abra seu navegador
2. Acesse: **http://127.0.0.1:8000/docs**
3. Você verá uma interface interativa com todos os endpoints
4. Clique em qualquer endpoint → "Try it out" → Preencha os dados → "Execute"

---

### **Opção 2: ReDoc (Documentação Alternativa) 📖**

Acesse: **http://127.0.0.1:8000/redoc**

---

### **Opção 3: PowerShell/Curl 💻**

**Exemplo 1:** Prever valor de venda
```powershell
curl http://127.0.0.1:8000/predict/venda -Method Post -ContentType "application/json" -Body '{"tipo_imovel":"apartamento","bairro":"Pinheiros","cidade":"São Paulo","quartos":2,"suites":1,"vagas":1,"area_util":75.0}'
```

**Exemplo 2:** Listar estados
```powershell
curl http://127.0.0.1:8000/estados
```

**Exemplo 3:** Listar cidades de SP
```powershell
curl http://127.0.0.1:8000/estados/SP/cidades
```

**Exemplo 4:** Status da API
```powershell
curl http://127.0.0.1:8000/status
```

---

### **Opção 4: Script Python 🐍**

Crie um arquivo `testar.py`:

```python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Teste 1: Listar tipos de imóveis
print("1️⃣ Tipos de Imóveis:")
response = requests.get(f"{BASE_URL}/tipos-imoveis")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Teste 2: Listar estados
print("\n2️⃣ Estados:")
response = requests.get(f"{BASE_URL}/estados")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Teste 3: Prever venda e aluguel
print("\n3️⃣ Previsão de Imóvel:")
dados = {
    "tipo_imovel": "apartamento",
    "bairro": "Pinheiros",
    "cidade": "São Paulo",
    "quartos": 2,
    "suites": 1,
    "vagas": 1,
    "area_util": 75.0
}
response = requests.post(f"{BASE_URL}/predict/imovel", json=dados)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Teste 4: Estatísticas do bairro
print("\n4️⃣ Estatísticas de Pinheiros:")
response = requests.get(f"{BASE_URL}/estatisticas/SP/São Paulo/Pinheiros")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# Teste 5: Status da API
print("\n5️⃣ Status da API:")
response = requests.get(f"{BASE_URL}/status")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
```

Execute:
```powershell
python testar.py
```

---

## 📊 Dados Disponíveis na API

### **Tipos de Imóveis:**
- apartamento
- casa
- cobertura
- loft

### **Estados e Cidades:**

**SP (São Paulo):**
- São Paulo (Bairros: Pinheiros, Moema, Tatuapé, Vila Madalena)
- Campinas (Bairros: Centro, Cambuí, Barão Geraldo)
- Santos (Bairros: Gonzaga, Boqueirão, Ponta da Praia)

**RJ (Rio de Janeiro):**
- Rio de Janeiro (Bairros: Copacabana, Ipanema, Barra da Tijuca, Leblon)
- Niterói (Bairros: Icaraí, Santa Rosa)
- Petrópolis (Bairros: Centro, Quitandinha)

**MG (Minas Gerais):**
- Belo Horizonte (Bairros: Savassi, Lourdes, Pampulha)
- Uberlândia (Bairros: Centro, Tibery)
- Juiz de Fora (Bairros: Centro, São Mateus)

### **Estatísticas Disponíveis:**
Apenas para:
- SP / São Paulo / Pinheiros
- SP / São Paulo / Moema

---

## 🔧 Arquitetura do Sistema

### **schemas.py**
Define os contratos de entrada e saída (Pydantic models):
- `ImovelFeatures`: Entrada para predições
- `PredicaoVendaOutput`, `PredicaoAluguelOutput`, `PredicaoImovelOutput`: Saídas de predição
- `TiposImoveisOutput`, `EstadosOutput`, `CidadesOutput`, `BairrosOutput`: Saídas de consulta
- `StatusOutput`, `ModeloVersaoOutput`: Saídas de monitoramento
- `EstatisticasBairroOutput`: Saída de estatísticas

### **ml_service.py**
Gerencia os modelos de Machine Learning:
- Carrega os pipelines (`venda_pipeline.joblib`, `aluguel_pipeline.joblib`)
- Prepara os dados de entrada (converte para DataFrame do pandas)
- Executa as predições
- Fornece informações sobre versão dos modelos

### **mock_db.py**
Simula um banco de dados com:
- Listas de tipos de imóveis
- Hierarquia de estados → cidades → bairros
- Estatísticas agregadas por bairro
- Tratamento de erros (404 quando não encontrado)

### **main.py**
API FastAPI principal:
- Define todos os 10 endpoints
- Organiza endpoints por tags (Previsão, Consulta, Monitoramento, Avançado)
- Trata erros e exceções
- Documenta cada endpoint com docstrings

### **mock_model_generator.py**
Script auxiliar para criar modelos falsos:
- Cria dados de treino sintéticos
- Treina pipelines com scikit-learn (`DummyRegressor`)
- Salva os modelos serializados com joblib

---

## ⚠️ Observações Importantes

### **1. Modelos Falsos**
Os modelos gerados são **simplificados** e usam `DummyRegressor` (sempre prevê a média).
Para uso em produção, substitua por modelos reais treinados com dados reais.

### **2. Ordem das Features**
O pipeline espera as features nesta ordem exata:
```python
['area_util', 'quartos', 'suites', 'vagas', 'tipo_imovel', 'bairro', 'cidade']
```

### **3. Banco de Dados Mock**
O `mock_db.py` simula um banco. Em produção, substitua por:
- PostgreSQL/MySQL para dados estruturados
- MongoDB para dados não estruturados
- Redis para cache

### **4. Tratamento de Erros**
A API retorna códigos HTTP apropriados:
- `200`: Sucesso
- `400`: Erro nos dados de entrada
- `404`: Recurso não encontrado
- `500`: Erro interno do servidor
- `503`: Serviço indisponível (modelos não carregados)

---

## 🎯 Próximos Passos

### **Para Desenvolvimento:**
1. Treinar modelos reais com dados históricos
2. Adicionar autenticação (JWT, OAuth2)
3. Implementar rate limiting
4. Adicionar logging estruturado
5. Criar testes unitários e de integração
6. Adicionar CI/CD

### **Para Produção:**
1. Usar banco de dados real
2. Implementar cache com Redis
3. Adicionar monitoramento (Prometheus, Grafana)
4. Configurar CORS adequadamente
5. Usar HTTPS
6. Containerizar com Docker
7. Deploy em cloud (AWS, Azure, GCP)

---

## 🐛 Solução de Problemas

### **Erro: "Arquivos de modelo não encontrados"**
**Solução:** Execute `python mock_model_generator.py` primeiro.

### **Erro: "No module named 'sklearn'"**
**Solução:** Instale as dependências: `pip install -r requirements.txt`

### **Erro: "Port 8000 already in use"**
**Solução:** Mate o processo na porta 8000 ou use outra porta:
```powershell
uvicorn main:app --port 8001
```

### **Erro 404 ao acessar cidades/bairros**
**Solução:** Verifique se o estado/cidade existe em `mock_db.py` e use a grafia correta.

---

## 📞 Suporte

Para dúvidas, consulte:
- Documentação interativa: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- FastAPI Docs: https://fastapi.tiangolo.com/

---

**🎉 Bom desenvolvimento!**

