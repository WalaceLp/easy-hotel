import { createContext } from 'react'
import type { PerfilNome, Usuario } from '../types/api'

export type AuthContextValue = {
  usuario: Usuario | null
  loading: boolean
  login: (login: string, senha: string) => Promise<Usuario>
  logout: () => void
  hasPerfil: (...perfis: PerfilNome[]) => boolean
}

export const AuthContext = createContext<AuthContextValue | null>(null)
