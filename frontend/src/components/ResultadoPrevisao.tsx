import React from 'react';
import { CompletoResposta, VendaResposta, LocacaoResposta } from '../types';
import './ResultadoPrevisao.css';

interface ResultadoPrevisaoProps {
  resultado: CompletoResposta | VendaResposta | LocacaoResposta | null;
  tipo: 'completo' | 'venda' | 'locacao';
  erro?: string;
}

const formatarMoeda = (valor: number): string => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(valor);
};

export const ResultadoPrevisao: React.FC<ResultadoPrevisaoProps> = ({
  resultado,
  tipo,
  erro,
}) => {
  if (erro) {
    return (
      <div className="resultado erro">
        <h3>Erro ao processar previsão</h3>
        <p>{erro}</p>
      </div>
    );
  }

  if (!resultado) {
    return null;
  }

  return (
    <div className="resultado sucesso">
      <h3>Resultado da Previsão</h3>

      {tipo === 'completo' && 'valor_previsto_venda' in resultado && 'valor_previsto_locacao' in resultado && (
        <div className="resultado-completo">
          <div className="card-valor venda">
            <h4>Valor de Venda</h4>
            <p className="valor">{formatarMoeda(resultado.valor_previsto_venda)}</p>
          </div>
          <div className="card-valor locacao">
            <h4>Valor de Locação (mensal)</h4>
            <p className="valor">{formatarMoeda(resultado.valor_previsto_locacao)}</p>
          </div>
        </div>
      )}

      {tipo === 'venda' && 'valor_previsto_venda' in resultado && (
        <div className="card-valor venda unico">
          <h4>Valor de Venda Previsto</h4>
          <p className="valor">{formatarMoeda(resultado.valor_previsto_venda)}</p>
        </div>
      )}

      {tipo === 'locacao' && 'valor_previsto_locacao' in resultado && (
        <div className="card-valor locacao unico">
          <h4>Valor de Locação Previsto (mensal)</h4>
          <p className="valor">{formatarMoeda(resultado.valor_previsto_locacao)}</p>
        </div>
      )}
    </div>
  );
};
