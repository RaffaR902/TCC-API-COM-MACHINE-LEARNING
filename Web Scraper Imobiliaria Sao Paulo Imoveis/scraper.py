import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configurações
URL_BASE = 'https://www.saopauloimoveis.com.br/imoveis/locacao/sp/sao-paulo/{}'
ARQUIVO_CSV = 'imoveis.csv'
DELAY = 1
LIMITE_NOVOS_IMOVEIS = 500

# Carrega URLs já salvas
try:
    df_existente = pd.read_csv(ARQUIVO_CSV)
    urls_existentes = set(df_existente['url'].dropna().tolist())
except FileNotFoundError:
    df_existente = pd.DataFrame()
    urls_existentes = set()

# Configura Selenium
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Burlar detecção webdriver
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

def limpar(texto):
    return re.sub(r'\s+', ' ', texto).strip()

def extrair_preco(texto: str):
    """
    Extrai preço no formato float a partir de string:
    'VENDA | R$ 21.000.000,00' -> 21000000.00 (float).
    """
    if not texto:
        return None
    m = re.search(r'R\$\s*([\d\.,]+)', texto, flags=re.IGNORECASE)
    if not m:
        return None
    bruto = m.group(1)
    # Remove separadores de milhar e troca vírgula decimal por ponto
    bruto = bruto.replace('.', '').replace(',', '.')
    try:
        return float(bruto)
    except ValueError:
        return None

def extrair_imoveis():
    todos = []
    pagina = 1

    while len(todos) < LIMITE_NOVOS_IMOVEIS:
        print(f'Coletando página {pagina}...')
        driver.get(URL_BASE.format(pagina))
        time.sleep(DELAY)

        cards = driver.find_elements(By.CSS_SELECTOR, 'div.col-md-6.col-sm-12')
        if not cards:
            print('Fim das páginas. Nenhum card encontrado.')
            break

        for card in cards:
            if len(todos) >= LIMITE_NOVOS_IMOVEIS:
                break

            try:
                dados = {
                    'url': '', 'tipo': '', 'bairro': '', 'cidade': 'São Paulo',
                    'objetivo': 'Venda', 'preco': '', 'area_util': '',
                    'quartos': '', 'suites': '', 'vagas': ''
                }

                # URL
                try:
                    link = card.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    if link in urls_existentes:
                        continue
                    dados['url'] = link
                except:
                    continue

                # Tipo e bairro
                try:
                    h2 = card.find_element(By.CSS_SELECTOR, 'h2')
                    tipo_span = h2.find_element(By.TAG_NAME, 'span')
                    dados['tipo'] = limpar(tipo_span.text).upper()
                    h2_lines = [limpar(x) for x in h2.text.split('\n') if limpar(x)]
                    if len(h2_lines) >= 2:
                        dados['bairro'] = limpar(h2_lines[1]).upper()
                except:
                    pass

                # Bloco com as infos
                try:
                    info = card.find_element(By.CSS_SELECTOR, 'div.col-md-6.col-sm-12')
                except Exception:
                    info = card

                # Preço e objetivo
                try:
                    spans = info.find_elements(By.CSS_SELECTOR, 'span')
                    preco_texto = ''
                    for sp in spans:
                        txt = sp.text
                        if 'R$' in txt:
                            preco_texto = txt
                            break
                    if preco_texto:
                        dados['preco'] = extrair_preco(preco_texto)
                        if 'LOCA' in preco_texto.upper() or 'ALUG' in preco_texto.upper():
                            dados['objetivo'] = 'Locação'
                        elif 'VENDA' in preco_texto.upper():
                            dados['objetivo'] = 'Venda'
                except Exception:
                    pass

                # Área, quartos, suítes, vagas
                try:
                    itens = card.find_elements(By.CSS_SELECTOR, 'ul li')
                    for item in itens:
                        b_tag = item.find_element(By.TAG_NAME, 'b').text
                        texto = item.text.lower()
                        valor = re.sub(r'\D', '', b_tag)  # remove qualquer caractere não numérico
                        if 'dorm' in texto or 'quarto' in texto:
                            dados['quartos'] = valor
                        elif 'suíte' in texto:
                            dados['suites'] = valor
                        elif 'vaga' in texto:
                            dados['vagas'] = valor
                        elif 'área útil' in texto:
                            dados['area_util'] = valor
                except:
                    pass

                todos.append(dados)
                urls_existentes.add(dados['url'])
                print(f"Coletado: {dados['url']} | Preço: {dados['preco']} | Bairro: {dados['bairro']}")

            except Exception as e:
                print(f'Erro ao coletar imóvel: {e}')
                continue

        pagina += 1

    return todos

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
    driver.quit()
