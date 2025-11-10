# mock_model_generator.py (ATUALIZADO)
# RODE: python mock_model_generator.py

import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
import os

# Definição das features EXATAS do seu exemplo
numeric_features = ['area_util', 'quartos', 'suites', 'vagas']
categorical_features = ['tipo_imovel', 'bairro', 'cidade']

# Todas as colunas na ordem que o pipeline vai esperar
ALL_FEATURES = numeric_features + categorical_features

# Criar dados de treino falsos
mock_data = pd.DataFrame({
    'area_util': [75.0, 120.0, 50.0, 200.0],
    'quartos': [2, 3, 1, 4],
    'suites': [1, 2, 1, 3],
    'vagas': [1, 2, 0, 2],
    'tipo_imovel': ['apartamento', 'apartamento', 'casa', 'cobertura'],
    'bairro': ['Pinheiros', 'Moema', 'Tatuapé', 'Pinheiros'],
    'cidade': ['São Paulo', 'São Paulo', 'São Paulo', 'Campinas'],
    'preco_venda': [750000, 1500000, 500000, 2500000],
    'preco_aluguel': [2800, 5000, 1800, 7000]
})

X = mock_data[ALL_FEATURES]
y_venda = mock_data['preco_venda']
y_aluguel = mock_data['preco_aluguel']

# Criar o pipeline de pré-processamento
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numeric_features)
    ],
    remainder='drop' # Ignora colunas que não estejam em 'features'
)

# Criar e treinar os pipelines
pipeline_venda = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', DummyRegressor(strategy='mean'))
])
pipeline_aluguel = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', DummyRegressor(strategy='mean'))
])

pipeline_venda.fit(X, y_venda)
pipeline_aluguel.fit(X, y_aluguel)

# Salvar os modelos
os.makedirs('models', exist_ok=True)
joblib.dump(pipeline_venda, 'models/venda_pipeline.joblib')
joblib.dump(pipeline_aluguel, 'models/aluguel_pipeline.joblib')

print("✅ Modelos falsos (v2) criados em 'models/'")

