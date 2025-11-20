import axios from 'axios';
import { ImovelEntrada, VendaResposta, LocacaoResposta, CompletoResposta } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Previsão de venda
  preverVenda: (imovel: ImovelEntrada) =>
    api.post<VendaResposta>('/prever/venda', imovel),

  // Previsão de locação
  preverLocacao: (imovel: ImovelEntrada) =>
    api.post<LocacaoResposta>('/prever/locacao', imovel),

  // Previsão completa (venda + locação)
  preverCompleto: (imovel: ImovelEntrada) =>
    api.post<CompletoResposta>('/prever/completo', imovel),

  // Obter metadados (tipos e bairros)
  obterMetadados: () => api.get('/metadata/tipos-bairros'),

  // Obter informações da API
  obterInfo: () => api.get('/info'),
};

export default api;
