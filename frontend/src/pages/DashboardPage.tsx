import { useEffect, useState } from 'react'
import { Alert } from '../components/Alert'
import { Badge } from '../components/Badge'
import { DataTable } from '../components/DataTable'
import { Loading } from '../components/Loading'
import { MetricCard } from '../components/MetricCard'
import { PageHeader } from '../components/PageHeader'
import { api, getApiError } from '../services/api'
import type { Dashboard, Reserva } from '../types/api'
import { formatCurrency, formatDate } from '../utils/formatters'

export function DashboardPage() {
  const [dashboard, setDashboard] = useState<Dashboard | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get<Dashboard>('/api/relatorios/dashboard')
      .then((response) => setDashboard(response.data))
      .catch((err) => setError(getApiError(err)))
  }, [])

  if (error) return <Alert type="error">{error}</Alert>
  if (!dashboard) return <Loading />

  return (
    <>
      <PageHeader title="Dashboard" description="Visão geral da operação do hotel." />
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Hóspedes" value={dashboard.total_hospedes} />
        <MetricCard label="Quartos disponíveis" value={dashboard.quartos_disponiveis} />
        <MetricCard label="Quartos ocupados" value={dashboard.quartos_ocupados} />
        <MetricCard label="Reservas pendentes" value={dashboard.reservas_pendentes} />
        <MetricCard label="Reservas confirmadas" value={dashboard.reservas_confirmadas} />
        <MetricCard label="Check-ins hoje" value={dashboard.checkins_previstos_hoje} />
        <MetricCard label="Check-outs hoje" value={dashboard.checkouts_previstos_hoje} />
        <MetricCard label="Faturamento do mês" value={formatCurrency(dashboard.faturamento_mes)} hint={`${dashboard.taxa_ocupacao}% ocupação`} />
      </div>
      <section className="mt-6">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Reservas recentes</h2>
        <DataTable<Reserva>
          data={dashboard.reservas_recentes}
          getKey={(item) => item.id}
          columns={[
            { header: 'Hóspede', render: (item) => item.hospede.nome },
            { header: 'Quarto', render: (item) => item.quarto_numero },
            { header: 'Entrada', render: (item) => formatDate(item.data_entrada) },
            { header: 'Status', render: (item) => <Badge value={item.status} /> },
            { header: 'Valor', render: (item) => formatCurrency(item.valor_total) }
          ]}
        />
      </section>
    </>
  )
}
