import axios from "axios";
import { getToken, clearTokens, saveTokens } from "../storage/token";

// ⚠️  Troque pelo IP local da sua máquina (ex: 192.168.1.10)
// No terminal: ipconfig (Windows) ou ifconfig (Mac/Linux)
export const BASE_URL = "http://192.168.1.5:8000";

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

// Injeta o token em toda requisição
api.interceptors.request.use(async (config) => {
  const token = await getToken("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Se der 401, tenta renovar com o refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refresh = await getToken("refresh");
        const res = await axios.post(`${BASE_URL}/api/v1/auth/refresh/`, {
          refresh,
        });
        await saveTokens(res.data.access, refresh!);
        original.headers.Authorization = `Bearer ${res.data.access}`;
        return api(original);
      } catch {
        await clearTokens();
      }
    }
    return Promise.reject(error);
  }
);

export default api;
