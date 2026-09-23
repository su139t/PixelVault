import api from "./api";

export const sendTelegramCode = async (phoneNumber) => {
  const forceCode = localStorage.getItem("pv_force_telegram_otp") === "1";
  const response = await api.post("/telegram/send-code", {
    phone_number: phoneNumber,
    force_code: forceCode,
  });
  if (response.data.code_sent) {
    localStorage.removeItem("pv_force_telegram_otp");
  }
  return response.data;
};

export const verifyTelegramCode = async (phoneNumber, code) => {
  const response = await api.post("/telegram/verify", {
    phone_number: phoneNumber,
    code,
  });
  return response.data;
};

export const verifyTelegram2FA = async (phoneNumber, password) => {
  const response = await api.post("/telegram/2fa", {
    phone_number: phoneNumber,
    password,
  });
  return response.data;
};

export const logoutTelegram = async () => {
  const response = await api.post("/telegram/logout");
  return response.data;
};

export const getCurrentUser = async (token) => {
  const response = await api.get("/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};
