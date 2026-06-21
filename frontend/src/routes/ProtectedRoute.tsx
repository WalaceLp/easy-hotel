import { Navigate, Outlet } from 'react-router-dom'
import { Loading } from '../components/Loading'
import { useAuth } from '../hooks/useAuth'

export function ProtectedRoute() {
  const { usuario, loading } = useAuth()
  if (loading) return <Loading fullScreen />
  if (!usuario) return <Navigate to="/login" replace />
  return <Outlet />
}
