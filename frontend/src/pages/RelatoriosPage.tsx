import { useEffect, useState } from 'react'
import { Alert } from '../components/Alert'
import { MetricCard } from '../components/MetricCard'
import { PageHeader } from '../components/PageHeader'
import { useAuth } from '../hooks/useAuth'
import { api } from '../services/api'
import type { Faturamento, Ocupacao, ReservasRelatorio } from '../types/api'
import { formatCurrency } from '../utils/formatters'

export function RelatoriosPage() {
  const { hasPerfil } = useAuth()
  const [faturamento, setFaturamento] = useState<Faturamento | null>(null)
  const [ocupacao, setOcupacao] = useState<Ocupacao | null>(null)
  const [reservas, setReservas] = useState<ReservasRelatorio | null>(null)

  useEffect(() => {
    if (!hasPerfil('ADMINISTRADOR', 'GERENTE')) return
    Promise.all([
      api.get<Faturamento>('/api/relatorios/faturamento'),
      api.get<Ocupacao>('/api/relatorios/ocupacao'),
      api.get<ReservasRelatorio>('/api/relatorios/reservas')
    ]).then(([faturamentoResponse, ocupacaoResponse, reservasResponse]) => {
      setFaturamento(faturamentoResponse.data)
      setOcupacao(ocupacaoResponse.data)
      setReservas(reservasResponse.data)
    })
  }, [hasPerfil])

  if (!hasPerfil('ADMINISTRADOR', 'GERENTE')) {
    return <Alert type="error">Apenas gerente e administrador podem acessar relatórios.</Alert>
  }

  return (
    <>
      <PageHeader title="Relatórios" description="Indicadores administrativos e financeiros." />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Faturamento" value={faturamento ? formatCurrency(faturamento.valor_total) : '-'} hint={`${faturamento?.quantidade_pagamentos ?? 0} pagamentos`} />
        <MetricCard label="Taxa de ocupação" value={ocupacao ? `${ocupacao.taxa_ocupacao}%` : '-'} hint={`${ocupacao?.quartos_ocupados ?? 0} quartos ocupados`} />
        <MetricCard label="Reservas totais" value={reservas?.total ?? '-'} />
        <MetricCard label="Reservas concluídas" value={reservas?.concluidas ?? '-'} />
      </div>
      <section className="mt-6 rounded-lg border border-slate-200 bg-white p-5">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Reservas por status</h2>
        <div className="grid gap-3 sm:grid-cols-3 xl:grid-cols-6">
          <MetricCard label="Pendentes" value={reservas?.pendentes ?? 0} />
          <MetricCard label="Confirmadas" value={reservas?.confirmadas ?? 0} />
          <MetricCard label="Em andamento" value={reservas?.em_andamento ?? 0} />
          <MetricCard label="Concluídas" value={reservas?.concluidas ?? 0} />
          <MetricCard label="Canceladas" value={reservas?.canceladas ?? 0} />
        </div>
      </section>
    </>
  )
}
