import { ReactNode, useEffect, useMemo, useState } from 'react'
import { api } from '../services/api'
import type { AuthResponse, PerfilNome, Usuario } from '../types/api'
import { AuthContext } from './auth-context'

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('easyhotel.token')
    if (!token) {
      setLoading(false)
      return
    }
    api
      .get<Usuario>('/api/auth/me')
      .then((response) => setUsuario(response.data))
      .catch(() => localStorage.removeItem('easyhotel.token'))
      .finally(() => setLoading(false))
  }, [])

  async function login(loginValue: string, senha: string) {
    const response = await api.post<AuthResponse>('/api/auth/login', { login: loginValue, senha })
    localStorage.setItem('easyhotel.token', response.data.access_token)
    setUsuario(response.data.usuario)
    return response.data.usuario
  }

  function logout() {
    localStorage.removeItem('easyhotel.token')
    setUsuario(null)
  }

  const value = useMemo(
    () => ({
      usuario,
      loading,
      login,
      logout,
      hasPerfil: (...perfis: PerfilNome[]) => Boolean(usuario && perfis.includes(usuario.perfil.nome))
    }),
    [usuario, loading]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
