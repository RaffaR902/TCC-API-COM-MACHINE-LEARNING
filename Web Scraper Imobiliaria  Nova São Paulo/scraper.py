import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurações
URL_BASE = '' 
ARQUIVO_CSV = 'imoveis.csv'
DELAY = 10  # Tempo de espera entre requisições (respeitando o robots.txt do site)
LIMITE_NOVOS_IMOVEIS = 10000 

# Lista de tipos de imóveis que o código reconhece
tipos_possiveis = [
    "casa assobradada", "casa de vila", "casa térrea", "conj. comercial", "ponto comercial",
    "apartamento", "cobertura", "comercial", "condomínio", "duplex", "flat", "galpão", "garden",
    "kit", "loja", "penthouse", "prédio", "sobrado", "studio", "terreno", "triplex", "sítio", "área"
]

# Mapeia as versões minúsculas para o formato padronizado
mapa_tipos = {
    "casa assobradada": "Casa Assobradada",
    "casa de vila": "Casa de Vila",
    "casa térrea": "Casa Térrea",
    "conj. comercial": "Conjunto Comercial",
    "ponto comercial": "Ponto Comercial",
    "apartamento": "Apartamento",
    "cobertura": "Cobertura",
    "comercial": "Comercial",
    "condomínio": "Condomínio",
    "duplex": "Duplex",
    "flat": "Flat",
    "galpão": "Galpão",
    "garden": "Garden",
    "kit": "Kitnet",
    "loja": "Loja",
    "penthouse": "Penthouse",
    "prédio": "Prédio",
    "sobrado": "Sobrado",
    "studio": "Studio",
    "terreno": "Terreno",
    "triplex": "Triplex",
    "sítio": "Sítio",
    "área": "Área"
}

# Carrega URLs de imóveis já salvos para evitar duplicação
try:
    df_existente = pd.read_csv(ARQUIVO_CSV)
    urls_existentes = set(df_existente['url'].dropna().tolist())
except FileNotFoundError:
    # Se o arquivo ainda não existir, cria DataFrame vazio
    df_existente = pd.DataFrame()
    urls_existentes = set()

# Configurações do navegador (Selenium)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

# Inicializa o driver do Chrome com o gerenciador automático
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Desativa a propriedade "webdriver" para tentar burlar a detecção de automação
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# Função que remove quebras de linha e espaços duplicados
def limpar(texto):
    return re.sub(r'\s+', ' ', texto).strip()

# Função que coleta os imóveis
def extrair_imoveis():
    todos = []
    pagina = 1

    while len(todos) < LIMITE_NOVOS_IMOVEIS:
        print(f'Coletando página {pagina}...')
        driver.get(URL_BASE.format(pagina))
        time.sleep(DELAY)

        cards = driver.find_elements(By.CSS_SELECTOR, 'div.bxOferta') # Coleta todos os cards de imóveis
        if not cards:
            print('Fim das páginas. Nenhum card encontrado.')
            break

        for card in cards:
            if len(todos) >= LIMITE_NOVOS_IMOVEIS:
                break

            try:
                # Inicializa os dados do imóvel
                dados = {
                    'url': '', 'tipo': '', 'bairro': '', 'cidade': '',
                    'objetivo': '', 'preco': '', 'area_util': '',
                    'quartos': '', 'suites': '', 'vagas': ''
                }

                # Coleta a URL do imóvel
                try:
                    link = card.find_element(By.CSS_SELECTOR, '.fotoImovel a')
                    href = link.get_attribute('href')
                    if href and '/imovel/' in href:
                        if href in urls_existentes:
                            continue
                        dados['url'] = href
                except:
                    continue

                # Coleta tipo, bairro e cidade
                try:
                    titulo = limpar(card.find_element(By.CSS_SELECTOR, '.titleOferta a').text)
                    tipo_lower = titulo.lower()

                    tipo_detectado = None
                    for tipo in tipos_possiveis:
                        if tipo in tipo_lower:
                            tipo_detectado = tipo
                            break

                    if not tipo_detectado: # Se o tipo não for reconhecido, pula
                        continue 

                    dados['tipo'] = mapa_tipos[tipo_detectado]

                    partes = titulo.split(' - ')
                    if len(partes) >= 2:
                        dados['cidade'] = limpar(partes[-1])
                        bairro_com_tipo = limpar(partes[-2])
                        if bairro_com_tipo.lower().startswith(tipo_detectado):
                            bairro = bairro_com_tipo[len(tipo_detectado):].strip(' -')
                        else:
                            bairro = bairro_com_tipo
                        dados['bairro'] = bairro
                except:
                    continue

                # Coleta preço e objetivo (venda/locação)
                try:
                    preco_tag = card.find_element(By.CSS_SELECTOR, 'p.valorOferta.secondValue')
                    preco_texto = limpar(preco_tag.text)

                    # Detecta objetivo
                    if 'locação' in preco_texto.lower() or 'aluguel' in preco_texto.lower():
                        dados['objetivo'] = 'Locação'
                    elif 'venda' in preco_texto.lower():
                        dados['objetivo'] = 'Venda'
                    else:
                        dados['objetivo'] = 'Desconhecido'

                    # Extrai o valor numérico
                    preco_match = re.search(r'R\$ ([\d\.\,]+)', preco_texto)
                    if preco_match:
                        preco_valor = preco_match.group(1).replace('.', '').replace(',', '.')
                        dados['preco'] = float(preco_valor)
                except:
                    pass

                # Coleta área útil (em m²)
                try:
                    area = card.find_element(By.CSS_SELECTOR, 'span.area').text
                    dados['area_util'] = re.sub(r'\D', '', area)
                except:
                    pass

                # Coleta número de quartos
                try:
                    quartos = card.find_element(By.CSS_SELECTOR, 'span.dorms').text
                    dados['quartos'] = re.sub(r'\D', '', quartos)
                except:
                    pass

                # Coleta número de suítes
                try:
                    suites = card.find_element(By.CSS_SELECTOR, 'span.suites').text
                    dados['suites'] = re.sub(r'\D', '', suites)
                except:
                    pass

                # Coleta número de vagas
                try:
                    vagas = card.find_element(By.CSS_SELECTOR, 'span.vagas').text
                    dados['vagas'] = re.sub(r'\D', '', vagas)
                except:
                    pass

                todos.append(dados)
                urls_existentes.add(dados['url'])
                print(f"Coletado: {dados['url']}")

            except Exception as e:
                print(f'Erro ao coletar imóvel: {e}')
                continue

        pagina += 1

    return todos # Retorna todos os imóveis coletados

# Execução principal
try:
    imoveis = extrair_imoveis()
    if imoveis:
        df_novos = pd.DataFrame(imoveis)
        df_final = pd.concat([df_existente, df_novos], ignore_index=True)
        df_final.drop_duplicates(subset=['url'], inplace=True)
        df_final.to_csv(ARQUIVO_CSV, index=False)
        print(f'\n{len(imoveis)} novos imóveis salvos em "{ARQUIVO_CSV}"')
    else:
        print('Nenhum imóvel novo coletado.')
finally:
    driver.quit() # Encerra o navegador
