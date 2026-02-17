import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Home from "./pages/Home";
import StartDiagnostic from "./pages/StartDiagnostic";
import Diagnostic from "./pages/Diagnostic";
import Result from "./pages/Result";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/diagnostico/iniciar" element={<StartDiagnostic />} />
          <Route path="/diagnostico/:id" element={<Diagnostic />} />
          <Route path="/diagnostico/:id/retomar" element={<Diagnostic />} />
          <Route path="/resultado/:token" element={<Result />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
