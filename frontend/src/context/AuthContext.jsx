/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState, useEffect } from "react";
import { getCurrentUser, logoutTelegram } from "../services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem("pv_token"));
  const [isLoading, setIsLoading] = useState(true);

  // On mount, validate existing token
  useEffect(() => {
    const validateToken = async () => {
      const storedToken = localStorage.getItem("pv_token");
      if (!storedToken) {
        setIsLoading(false);
        return;
      }

      try {
        const data = await getCurrentUser(storedToken);
        setUser(data.user);
        setToken(storedToken);
      } catch {
        // Token invalid or expired
        localStorage.removeItem("pv_token");
        localStorage.removeItem("pv_user");
        setToken(null);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    validateToken();
  }, []);

  const completeLogin = (data) => {
    const { user: userData, token: authToken } = data;

    localStorage.setItem("pv_token", authToken);
    localStorage.setItem("pv_user", JSON.stringify(userData));

    setToken(authToken);
    setUser(userData);

    return userData;
  };

  const logout = async () => {
    localStorage.setItem("pv_force_telegram_otp", "1");
    try {
      await logoutTelegram();
    } catch (error) {
      console.error("Telegram logout failed:", error);
    }
    localStorage.removeItem("pv_token");
    localStorage.removeItem("pv_user");
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    isLoading,
    completeLogin,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
