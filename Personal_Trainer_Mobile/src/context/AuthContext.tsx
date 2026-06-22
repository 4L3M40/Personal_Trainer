import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { hasSession, saveTokens, clearTokens } from "../storage/token";
import { setUnauthorizedHandler } from "../api/client";

interface AuthContextValue {
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (access: string, refresh: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Ao abrir o app, verifica se já existe um token salvo (auto-login).
  useEffect(() => {
    (async () => {
      const logged = await hasSession();
      setIsLoggedIn(logged);
      setIsLoading(false);
    })();
  }, []);

  // Se o client.ts não conseguir renovar o token (refresh expirado/inválido),
  // ele chama esse handler para tirar o usuário das telas protegidas.
  useEffect(() => {
    setUnauthorizedHandler(() => setIsLoggedIn(false));
    return () => setUnauthorizedHandler(null);
  }, []);

  const login = useCallback(async (access: string, refresh: string) => {
    await saveTokens(access, refresh);
    setIsLoggedIn(true);
  }, []);

  const logout = useCallback(async () => {
    await clearTokens();
    setIsLoggedIn(false);
  }, []);

  return (
    <AuthContext.Provider value={{ isLoggedIn, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth precisa ser usado dentro de um <AuthProvider>.");
  }
  return ctx;
}
