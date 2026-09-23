import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { sendTelegramCode, verifyTelegram2FA, verifyTelegramCode } from "../services/authService";
import { Image as ImageIcon, Shield, Zap, Cloud, ArrowRight, Phone } from "lucide-react";

export default function LoginPage() {
  const { isAuthenticated, isLoading, completeLogin } = useAuth();
  const [phoneNumber, setPhoneNumber] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [step, setStep] = useState("phone");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);
    try {
      if (step === "phone") {
        const response = await sendTelegramCode(phoneNumber);
        if (response.token) completeLogin(response);
        else setStep("code");
      } else if (step === "code") {
        const response = await verifyTelegramCode(phoneNumber, code);
        if (response.password_required) setStep("2fa");
        else completeLogin(response);
      } else {
        completeLogin(await verifyTelegram2FA(phoneNumber, password));
      }
    } catch (loginError) {
      setError(loginError.response?.data?.message || "Unable to sign in. Check your phone number and try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-[#0a0a0f] flex items-center justify-center">
        <div className="w-12 h-12 rounded-full border-[3px] border-white/10 border-t-violet-500 animate-spin" />
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="login-page">
      {/* Animated gradient background */}
      <div className="login-bg" />

      {/* Floating orbs */}
      <div className="login-orb login-orb-1" />
      <div className="login-orb login-orb-2" />
      <div className="login-orb login-orb-3" />

      {/* Content */}
      <div className="login-content">
        {/* Glass card */}
        <div className="login-card">
          {/* Logo */}
          <div className="login-logo">
            <div className="login-logo-icon">
              <ImageIcon className="w-8 h-8 text-white" />
            </div>
            <h1 className="login-title">PixelVault</h1>
          </div>

          <p className="login-subtitle">
            Sign in with your Telegram account to unlock your private photo vault.
          </p>

          {/* Features */}
          <div className="login-features">
            <div className="login-feature">
              <Shield className="w-4 h-4" />
              <span>End-to-end encrypted</span>
            </div>
            <div className="login-feature">
              <Zap className="w-4 h-4" />
              <span>AI-powered search</span>
            </div>
            <div className="login-feature">
              <Cloud className="w-4 h-4" />
              <span>Unlimited cloud storage</span>
            </div>
          </div>

          <form className="phone-login-form" onSubmit={handleSubmit}>
            {step === "phone" && <>
              <label htmlFor="phone-number">Telegram phone number</label>
              <div className="phone-input-wrap">
                <Phone className="h-4 w-4" />
                <input id="phone-number" type="tel" value={phoneNumber} onChange={(event) => setPhoneNumber(event.target.value)} placeholder="+1 555 123 4567" autoComplete="tel" required />
              </div>
            </>}
            {step === "code" && <>
              <label htmlFor="telegram-code">Verification code</label>
              <input id="telegram-code" inputMode="numeric" value={code} onChange={(event) => setCode(event.target.value)} placeholder="12345" autoComplete="one-time-code" required />
              <p className="login-hint">Telegram sent a code to your account.</p>
            </>}
            {step === "2fa" && <>
              <label htmlFor="telegram-password">Telegram 2FA password</label>
              <input id="telegram-password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Your Telegram password" autoComplete="current-password" required />
              <p className="login-hint">Your account has two-step verification enabled.</p>
            </>}
            {error && <p className="login-error" role="alert">{error}</p>}
            <button className="phone-login-submit" type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Working..." : step === "phone" ? "Send Telegram code" : step === "code" ? "Verify code" : "Complete sign in"}
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          {/* Divider */}
          <div className="login-divider">
            <div className="login-divider-line" />
            <span className="login-divider-text">Sign in to continue</span>
            <div className="login-divider-line" />
          </div>

          <p className="login-footer">
            Your number and password are handled by Telegram MTProto.
            <br />
            PixelVault never stores your OTP or 2FA password.
          </p>
        </div>
      </div>
    </div>
  );
}
