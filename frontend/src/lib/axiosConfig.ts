import axios, { AxiosError } from 'axios';

// Configurar intervalo de timeout padrão
axios.defaults.timeout = 10000;

// Interceptor para tratamento de erros global
axios.interceptors.response.use(
  response => response,
  (error: AxiosError) => {
    if (error.response?.status === 422) {
      console.error('Erro de validação:', error.response.data);
    } else if (error.response?.status === 500) {
      console.error('Erro no servidor:', error.response.data);
    } else if (!error.response) {
      console.error('Erro de conexão - API não está acessível');
    }
    return Promise.reject(error);
  }
);

export default axios;
