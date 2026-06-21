import { useEffect, useState } from 'react'
import { BedDouble, CalendarCheck, CalendarClock, CreditCard, DoorOpen, Hotel, UserRoundCheck, Users } from 'lucide-react'
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
      <section className="mb-6 overflow-hidden rounded-lg border border-slate-200 bg-slate-950 p-6 text-white shadow-lg shadow-slate-300/60">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm font-semibold text-blue-300">Painel operacional</p>
            <h2 className="mt-2 text-2xl font-bold">Hotel pronto para a apresentação</h2>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
              Acompanhe reservas, ocupação e faturamento com dados consolidados do sistema.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-3 sm:min-w-80">
            <div className="rounded-lg border border-white/10 bg-white/5 p-4">
              <p className="text-xs text-slate-400">Ocupação</p>
              <p className="mt-1 text-2xl font-bold">{dashboard.taxa_ocupacao}%</p>
            </div>
            <div className="rounded-lg border border-white/10 bg-white/5 p-4">
              <p className="text-xs text-slate-400">Mês</p>
              <p className="mt-1 text-2xl font-bold">{formatCurrency(dashboard.faturamento_mes)}</p>
            </div>
          </div>
        </div>
      </section>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Hóspedes" value={dashboard.total_hospedes} icon={Users} tone="blue" />
        <MetricCard label="Quartos disponíveis" value={dashboard.quartos_disponiveis} icon={DoorOpen} tone="emerald" />
        <MetricCard label="Quartos ocupados" value={dashboard.quartos_ocupados} icon={BedDouble} tone="amber" />
        <MetricCard label="Reservas pendentes" value={dashboard.reservas_pendentes} icon={CalendarClock} tone="amber" />
        <MetricCard label="Reservas confirmadas" value={dashboard.reservas_confirmadas} icon={CalendarCheck} tone="blue" />
        <MetricCard label="Check-ins hoje" value={dashboard.checkins_previstos_hoje} icon={UserRoundCheck} tone="emerald" />
        <MetricCard label="Check-outs hoje" value={dashboard.checkouts_previstos_hoje} icon={Hotel} tone="slate" />
        <MetricCard
          label="Faturamento do mês"
          value={formatCurrency(dashboard.faturamento_mes)}
          hint={`${dashboard.taxa_ocupacao}% ocupação`}
          icon={CreditCard}
          tone="emerald"
        />
      </div>
      <section className="mt-6">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-slate-950">Reservas recentes</h2>
          <span className="text-sm font-medium text-slate-500">{dashboard.reservas_recentes.length} registros</span>
        </div>
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
