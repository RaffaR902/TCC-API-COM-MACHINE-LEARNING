import React from 'react';
import './AbaBotoes.css';

interface AbaBotoesProps {
  aba: 'completo' | 'venda' | 'locacao';
  onChangeAba: (aba: 'completo' | 'venda' | 'locacao') => void;
}

export const AbaBotoes: React.FC<AbaBotoesProps> = ({ aba, onChangeAba }) => {
  return (
    <div className="aba-botoes">
      <button
        className={`aba-btn ${aba === 'completo' ? 'ativo' : ''}`}
        onClick={() => onChangeAba('completo')}
      >
        Previsão Completa
      </button>
      <button
        className={`aba-btn ${aba === 'venda' ? 'ativo' : ''}`}
        onClick={() => onChangeAba('venda')}
      >
        Apenas Venda
      </button>
      <button
        className={`aba-btn ${aba === 'locacao' ? 'ativo' : ''}`}
        onClick={() => onChangeAba('locacao')}
      >
        Apenas Locação
      </button>
    </div>
  );
};
