import React from 'react';
import { ImovelEntrada } from '../types';
import './PrevisaoForm.css';

interface PrevisaoFormProps {
  tipos: string[];
  bairros: string[];
  onSubmit: (imovel: ImovelEntrada) => void;
  loading: boolean;
}

export const PrevisaoForm: React.FC<PrevisaoFormProps> = ({
  tipos,
  bairros,
  onSubmit,
  loading,
}) => {
  const [formData, setFormData] = React.useState<ImovelEntrada>({
    tipo: tipos[0] || '',
    bairro: bairros[0] || '',
    area_util: 100,
    quartos: 1,
    suites: 0,
    vagas: 0,
    tem_suite: 0,
    tem_vaga: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const parsedValue = type === 'number' ? parseFloat(value) || 0 : value;

    setFormData(prev => {
      const next = {
        ...prev,
        [name]: parsedValue,
      } as ImovelEntrada;

      // Atualiza os campos derivados quando suites/vagas mudam
      if (name === 'suites') {
        next.tem_suite = Number(parsedValue) > 0 ? 1 : 0;
      }
      if (name === 'vagas') {
        next.tem_vaga = Number(parsedValue) > 0 ? 1 : 0;
      }

      return next;
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Garante que os campos derivados estejam corretos ao submeter
    const payload: ImovelEntrada = {
      ...formData,
      tem_suite: formData.suites > 0 ? 1 : 0,
      tem_vaga: formData.vagas > 0 ? 1 : 0,
    };

    onSubmit(payload);
  };

  return (
    <form className="previsao-form" onSubmit={handleSubmit}>
      <h2>Preencha os dados do imóvel</h2>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="tipo">Tipo de Imóvel</label>
          <select
            id="tipo"
            name="tipo"
            value={formData.tipo}
            onChange={handleChange}
            required
          >
            {tipos.map(tipo => (
              <option key={tipo} value={tipo}>
                {tipo.charAt(0).toUpperCase() + tipo.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="bairro">Bairro</label>
          <select
            id="bairro"
            name="bairro"
            value={formData.bairro}
            onChange={handleChange}
            required
          >
            {bairros.map(bairro => (
              <option key={bairro} value={bairro}>
                {bairro
                  .split('_')
                  .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                  .join(' ')}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="area_util">Área Útil (m²)</label>
          <input
            id="area_util"
            type="number"
            name="area_util"
            value={formData.area_util}
            onChange={handleChange}
            min="1"
            step="0.1"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="quartos">Quartos</label>
          <input
            id="quartos"
            type="number"
            name="quartos"
            value={formData.quartos}
            onChange={handleChange}
            min="0"
            max="20"
            required
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="suites">Suítes</label>
          <input
            id="suites"
            type="number"
            name="suites"
            value={formData.suites}
            onChange={handleChange}
            min="0"
            max="20"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="vagas">Vagas de Garagem</label>
          <input
            id="vagas"
            type="number"
            name="vagas"
            value={formData.vagas}
            onChange={handleChange}
            min="0"
            max="20"
            required
          />
        </div>
      </div>

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? 'Gerando Previsão...' : 'Gerar Previsão'}
      </button>
    </form>
  );
};
