import type { PerfilNome } from '../types/api'

export function getHomePathForPerfil(perfil: PerfilNome) {
  if (perfil === 'RECEPCIONISTA') return '/hospedes'
  return '/dashboard'
}

export function perfilPermitido(perfil: PerfilNome | undefined, perfisPermitidos?: PerfilNome[]) {
  if (!perfisPermitidos) return true
  return Boolean(perfil && perfisPermitidos.includes(perfil))
}
