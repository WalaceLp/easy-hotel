export type PerfilNome = 'ADMINISTRADOR' | 'GERENTE' | 'RECEPCIONISTA'

export type Perfil = {
  id: number
  nome: PerfilNome
}

export type Usuario = {
  id: number
  nome: string
  login: string
  perfil_id: number
  ativo: boolean
  criado_em: string
  atualizado_em: string
  perfil: Perfil
}

export type AuthResponse = {
  access_token: string
  token_type: 'bearer'
  usuario: Usuario
}

export type Hospede = {
  id: number
  nome: string
  cpf: string
  telefone: string | null
  email: string | null
  criado_em: string
  atualizado_em: string
}

export type TipoQuarto = {
  id: number
  descricao: string
  preco_base: string
  capacidade: number
  ativo: boolean
}

export type StatusQuarto = {
  id: number
  descricao: string
}

export type Quarto = {
  numero: string
  tipo_id: number
  status_id: number
  observacoes: string | null
  ativo: boolean
  tipo: TipoQuarto
  status: StatusQuarto
  criado_em: string
  atualizado_em: string
}

export type Reserva = {
  id: number
  data_reserva: string
  data_entrada: string
  data_saida: string
  status: string
  quantidade_hospedes: number
  valor_total: string
  total_pago: string
  saldo_pendente: string
  hospede_id: number
  quarto_numero: string
  usuario_id: number
  observacoes: string | null
  criado_em: string
  atualizado_em: string
  hospede: Hospede
  quarto: Quarto
  usuario: Usuario
}

export type MetodoPagamento = {
  id: number
  descricao: string
  ativo: boolean
}

export type Pagamento = {
  id: number
  valor: string
  data_pagamento: string
  metodo_id: number
  reserva_id: number
  usuario_id: number
  observacoes: string | null
  metodo: MetodoPagamento
}

export type Dashboard = {
  total_hospedes: number
  quartos_disponiveis: number
  quartos_ocupados: number
  reservas_pendentes: number
  reservas_confirmadas: number
  checkins_previstos_hoje: number
  checkouts_previstos_hoje: number
  faturamento_mes: string
  taxa_ocupacao: number
  reservas_recentes: Reserva[]
}

export type Faturamento = {
  data_inicio: string | null
  data_fim: string | null
  valor_total: string
  quantidade_pagamentos: number
}

export type Ocupacao = {
  data_inicio: string | null
  data_fim: string | null
  total_quartos_ativos: number
  quartos_ocupados: number
  taxa_ocupacao: number
}

export type ReservasRelatorio = {
  data_inicio: string | null
  data_fim: string | null
  total: number
  pendentes: number
  confirmadas: number
  em_andamento: number
  concluidas: number
  canceladas: number
}
