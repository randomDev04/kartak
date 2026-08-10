import { createContext, useContext, useState, useEffect } from "react";
import { api } from "./api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));

  async function login(email, password) {
    const data = await api.login(email, password);
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
  }

  useEffect(() => {
    const handleUnauthorized = () => {
      console.log("Unauthorized event detected, logging out...");
      logout();
    };
    window.addEventListener("unauthorized", handleUnauthorized);
    return () => window.removeEventListener("unauthorized", handleUnauthorized);
  }, []);

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: Boolean(token), login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
