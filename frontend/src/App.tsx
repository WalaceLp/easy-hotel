import { Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { AppLayout } from './layouts/AppLayout'
import { ProtectedRoute } from './routes/ProtectedRoute'
import { DashboardPage } from './pages/DashboardPage'
import { HospedeFormPage } from './pages/HospedeFormPage'
import { HospedesPage } from './pages/HospedesPage'
import { LoginPage } from './pages/LoginPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { PagamentosPage } from './pages/PagamentosPage'
import { QuartosPage } from './pages/QuartosPage'
import { RelatoriosPage } from './pages/RelatoriosPage'
import { ReservaDetalhePage } from './pages/ReservaDetalhePage'
import { ReservaFormPage } from './pages/ReservaFormPage'
import { ReservasPage } from './pages/ReservasPage'
import { TiposQuartoPage } from './pages/TiposQuartoPage'
import { UsuariosPage } from './pages/UsuariosPage'
import { useAuth } from './hooks/useAuth'
import { getHomePathForPerfil } from './utils/permissions'

function HomeRedirect() {
  const { usuario } = useAuth()
  return <Navigate to={usuario ? getHomePathForPerfil(usuario.perfil.nome) : '/login'} replace />
}

export function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route index element={<HomeRedirect />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/hospedes" element={<HospedesPage />} />
            <Route path="/hospedes/novo" element={<HospedeFormPage />} />
            <Route path="/hospedes/:id/editar" element={<HospedeFormPage />} />
            <Route path="/quartos" element={<QuartosPage />} />
            <Route path="/tipos-quarto" element={<TiposQuartoPage />} />
            <Route path="/reservas" element={<ReservasPage />} />
            <Route path="/reservas/nova" element={<ReservaFormPage />} />
            <Route path="/reservas/:id" element={<ReservaDetalhePage />} />
            <Route path="/pagamentos" element={<PagamentosPage />} />
            <Route path="/usuarios" element={<UsuariosPage />} />
            <Route path="/relatorios" element={<RelatoriosPage />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AuthProvider>
  )
}
