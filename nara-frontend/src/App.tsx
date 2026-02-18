import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CookieConsentBanner } from "./components/CookieConsentBanner";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { ProtectedAdminRoute } from "./components/ProtectedAdminRoute";
import AdminLogin from "./pages/AdminLogin";
import Dashboard from "./pages/Dashboard";
import Home from "./pages/Home";
import StartDiagnostic from "./pages/StartDiagnostic";
import Diagnostic from "./pages/Diagnostic";
import Result from "./pages/Result";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import TermsOfUse from "./pages/TermsOfUse";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/diagnostico/iniciar" element={<StartDiagnostic />} />
            <Route path="/diagnostico/:id" element={<Diagnostic />} />
            <Route path="/diagnostico/:id/retomar" element={<Diagnostic />} />
            <Route path="/resultado/:token" element={<Result />} />
            <Route path="/politica-de-privacidade" element={<PrivacyPolicy />} />
            <Route path="/termos-de-uso" element={<TermsOfUse />} />
            <Route path="/admin/login" element={<AdminLogin />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedAdminRoute>
                  <Dashboard />
                </ProtectedAdminRoute>
              }
            />
          </Routes>
          <CookieConsentBanner />
        </BrowserRouter>
      </ErrorBoundary>
    </QueryClientProvider>
  );
}

export default App;
