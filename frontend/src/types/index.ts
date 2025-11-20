// Tipos para a aplicação
export interface ImovelEntrada {
  tipo: string;
  bairro: string;
  area_util: number;
  quartos: number;
  suites: number;
  vagas: number;

  // Fields derivados exigidos pelo schema da API
  tem_suite: number;
  tem_vaga: number;
}

export interface VendaResposta {
  valor_previsto_venda: number;
}

export interface LocacaoResposta {
  valor_previsto_locacao: number;
}

export interface CompletoResposta {
  valor_previsto_venda: number;
  valor_previsto_locacao: number;
}

export interface TipoBairro {
  tipos: string[];
  bairros: string[];
}
