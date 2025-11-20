import React from 'react';
import './App.css';
import { PrevisaoForm } from './components/PrevisaoForm';
import { ResultadoPrevisao } from './components/ResultadoPrevisao';
import { AbaBotoes } from './components/AbaBotoes';
import { apiService } from './services/api';
import { ImovelEntrada, CompletoResposta, VendaResposta, LocacaoResposta } from './types';

const tiposBairros = {
  tipos: ['apartamento', 'casa'],
  bairros: [
    'aclimacao', 'agua_branca', 'agua_funda', 'alto_da_boa_vista', 'alto_da_mooca',
    'alto_de_pinheiros', 'alto_do_ipiranga', 'americanopolis', 'barra_funda',
    'bela_alianca', 'bela_vista', 'boacava', 'bosque_da_saude', 'bras', 'brooklin',
    'brooklin_novo', 'brooklin_paulista', 'butanta', 'cambuci', 'campininha',
    'campo_belo', 'campo_grande', 'campos_eliseos', 'capela_do_socorro',
    'casa_verde_baixa', 'centro', 'cerqueira_cesar', 'chacara_gaivotas',
    'chacara_inglesa', 'chacara_klabin', 'chacara_meyer', 'chacara_monte_alegre',
    'chacara_santo_antonio_zona_sul', 'cidade_ademar', 'cidade_domitila',
    'cidade_mae_do_ceu', 'cidade_moncoes', 'cidade_vargas',
    'conjunto_residencial_jardim_canaa', 'consolacao', 'cupece', 'cursino',
    'eldorado', 'fazenda_morumbi', 'granja_julieta', 'higienopolis', 'indianopolis',
    'instituto_de_previdencia', 'interlagos', 'ipiranga', 'itaim', 'itaim_bibi',
    'jabaquara', 'jardim_aeroporto', 'jardim_alzira', 'jardim_america',
    'jardim_ampliacao', 'jardim_analia_franco', 'jardim_aurelia', 'jardim_botucatu',
    'jardim_cabore', 'jardim_caravelas', 'jardim_celeste', 'jardim_celia_zona_sul',
    'jardim_cidalia', 'jardim_climax', 'jardim_colombo', 'jardim_consorcio',
    'jardim_cordeiro', 'jardim_da_gloria', 'jardim_da_saude', 'jardim_das_acacias',
    'jardim_das_bandeiras', 'jardim_das_laranjeiras', 'jardim_dom_bosco',
    'jardim_dos_estados', 'jardim_dos_lagos', 'jardim_ernestina', 'jardim_europa',
    'jardim_fonte_do_morumbi', 'jardim_franca', 'jardim_germania', 'jardim_gloria',
    'jardim_ipanema_zona_sul', 'jardim_itacolomi', 'jardim_itapeva',
    'jardim_itapura', 'jardim_leonor', 'jardim_lourdes_zona_sul', 'jardim_luanda',
    'jardim_luso', 'jardim_luzitania', 'jardim_marajoara', 'jardim_maria_estela',
    'jardim_marquesa', 'jardim_miriam_zona_sul', 'jardim_morumbi',
    'jardim_nosso_lar', 'jardim_nova_germania', 'jardim_novo_mundo',
    'jardim_oriental', 'jardim_patente', 'jardim_patente_novo', 'jardim_paulista',
    'jardim_paulistano', 'jardim_petropolis', 'jardim_pinheiros',
    'jardim_portal_i_e_ii', 'jardim_previdencia', 'jardim_prudencia',
    'jardim_santa_cruz_sacoma', 'jardim_santa_emilia', 'jardim_santo_amaro',
    'jardim_santo_antoninho', 'jardim_sao_paulozona_norte', 'jardim_sao_saverio',
    'jardim_saude', 'jardim_selma', 'jardim_sertaozinho', 'jardim_taquaral',
    'jardim_ubirajara_zona_sul', 'jardim_umuarama', 'jardim_vergueiro_sacoma',
    'jardim_vila_mariana', 'jardins', 'jurubatuba', 'klabin', 'lapa', 'liberdade',
    'mirandopolis', 'moema', 'mooca', 'morro_dos_ingleses', 'morumbi',
    'nova_piraju', 'pacaembu', 'paineiras_do_morumbi', 'panamby', 'paraiso',
    'paraiso_do_morumbi', 'parque_alves_de_lima', 'parque_bairro_morumbi',
    'parque_bristol', 'parque_colonial', 'parque_da_mooca',
    'parque_da_vila_prudente', 'parque_do_castelo', 'parque_do_morumbi',
    'parque_dos_principes', 'parque_independencia', 'parque_jabaquara',
    'parque_reboucas', 'parque_santo_antonio', 'perdizes', 'pinheiros',
    'planalto_paulista', 'quinta_da_paineira', 'real_parque', 'recanto_paraiso',
    'republica', 'sacoma', 'santa_cecilia', 'santa_efigenia', 'santa_teresinha',
    'santana', 'santo_amaro', 'sao_joao_climaco', 'sao_judas', 'saude', 'se',
    'socorro', 'sumare', 'sumarezinho', 'super_quadra_morumbi', 'tatuape',
    'usina_piratininga', 'veleiros', 'vila_agua_funda', 'vila_andrade',
    'vila_arapua', 'vila_arriete', 'vila_babilonia', 'vila_bela', 'vila_brasilina',
    'vila_brasilio_machado', 'vila_buarque', 'vila_californiazona_sul',
    'vila_campestre', 'vila_campo_grande', 'vila_caraguata', 'vila_carioca',
    'vila_carrao', 'vila_castelo', 'vila_clara', 'vila_clementino',
    'vila_constanca', 'vila_cordeiro', 'vila_cruzeiro', 'vila_das_merces',
    'vila_deodoro', 'vila_do_bosque', 'vila_do_encontro', 'vila_dom_pedro_ii',
    'vila_emir', 'vila_fachini', 'vila_gea', 'vila_gertrudes', 'vila_graciosa',
    'vila_guarani', 'vila_guarani_zona_sul', 'vila_gumercindo', 'vila_heliopolis',
    'vila_ida', 'vila_imperio', 'vila_independencia', 'vila_ipojuca',
    'vila_irmaos_arnoni', 'vila_isa', 'vila_leopoldina', 'vila_libanesa',
    'vila_liviero', 'vila_madalena', 'vila_marari', 'vila_mariana', 'vila_marte',
    'vila_mascote', 'vila_mira', 'vila_moinho_velho', 'vila_monumento',
    'vila_moraes', 'vila_moreira', 'vila_natalia', 'vila_noca',
    'vila_nova_caledonia', 'vila_nova_conceicao', 'vila_olimpia',
    'vila_parque_jabaquara', 'vila_patrimonial', 'vila_paulista', 'vila_prudente',
    'vila_rica', 'vila_romana', 'vila_santa_catarina', 'vila_santa_teresa_zona_sul',
    'vila_santo_estefano', 'vila_sao_francisco_zona_sul', 'vila_sao_jose_ipiranga',
    'vila_sao_paulo', 'vila_sao_pedro', 'vila_sofia', 'vila_sonia', 'vila_suzana',
    'vila_talarico', 'vila_tramontano', 'vila_uberabinha',
  ],
};

function App() {
  const [aba, setAba] = React.useState<'completo' | 'venda' | 'locacao'>('completo');
  const [resultado, setResultado] = React.useState<
    CompletoResposta | VendaResposta | LocacaoResposta | null
  >(null);
  const [loading, setLoading] = React.useState(false);
  const [erro, setErro] = React.useState<string | undefined>();

  const handleSubmit = async (imovel: ImovelEntrada) => {
    setLoading(true);
    setErro(undefined);
    setResultado(null);

    try {
      let response;
      switch (aba) {
        case 'venda':
          response = await apiService.preverVenda(imovel);
          break;
        case 'locacao':
          response = await apiService.preverLocacao(imovel);
          break;
        case 'completo':
          response = await apiService.preverCompleto(imovel);
          break;
      }
      setResultado(response.data);
    } catch (error: any) {
      
      let mensagem = 'Erro ao conectar com a API. Verifique se ela está rodando.';
      const detail = error?.response?.data?.detail ?? error?.response?.data ?? null;

      if (Array.isArray(detail)) {
        
        mensagem = detail
          .map((d: any) => {
            if (typeof d === 'string') return d;
            if (d?.msg) return d.msg;
            if (d?.message) return d.message;
            return JSON.stringify(d);
          })
          .join('; ');
      } else if (detail && typeof detail === 'object') {
        mensagem = detail?.detail || detail?.message || JSON.stringify(detail);
      } else if (error?.message) {
        mensagem = error.message;
      }

      setErro(mensagem);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="title">
          <h1>Previsão de Preços de Imóveis - Usando Machine Learning</h1>
          
        </div>
        
      </header>

      <main className="container">
        <div className="left">
          <AbaBotoes aba={aba} onChangeAba={setAba} />
          <PrevisaoForm
            tipos={tiposBairros.tipos}
            bairros={tiposBairros.bairros}
            onSubmit={handleSubmit}
            loading={loading}
          />
        </div>

        <aside className="right">
          <ResultadoPrevisao resultado={resultado} tipo={aba} erro={erro} />
        </aside>
      </main>

      <footer className="footer">
        <p>© 2025 - TCC API com Machine Learning</p>
        <p>Guilherme Bertogna & Rafael Ribeiro</p>
      </footer>
    </div>
  );
}

export default App;
