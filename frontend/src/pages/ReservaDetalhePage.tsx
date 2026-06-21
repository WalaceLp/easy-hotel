import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Alert } from '../components/Alert'
import { Badge } from '../components/Badge'
import { Button } from '../components/Button'
import { DataTable } from '../components/DataTable'
import { PageHeader } from '../components/PageHeader'
import { api, getApiError } from '../services/api'
import type { Pagamento, Reserva } from '../types/api'
import { formatCurrency, formatDate, formatDateTime } from '../utils/formatters'

export function ReservaDetalhePage() {
  const { id } = useParams()
  const [reserva, setReserva] = useState<Reserva | null>(null)
  const [pagamentos, setPagamentos] = useState<Pagamento[]>([])
  const [error, setError] = useState('')

  function load() {
    Promise.all([
      api.get<Reserva>(`/api/reservas/${id}`),
      api.get<Pagamento[]>(`/api/reservas/${id}/pagamentos`)
    ]).then(([reservaResponse, pagamentosResponse]) => {
      setReserva(reservaResponse.data)
      setPagamentos(pagamentosResponse.data)
    })
  }

  useEffect(load, [id])

  async function action(path: string, body = {}) {
    setError('')
    try {
      await api.request({ url: path, method: path.includes('check') ? 'POST' : 'PATCH', data: body })
      load()
    } catch (err) {
      setError(getApiError(err))
    }
  }

  if (!reserva) return null

  return (
    <>
      <PageHeader title={`Reserva #${reserva.id}`} action={<Link to="/reservas"><Button variant="secondary">Voltar</Button></Link>} />
      {error && <div className="mb-4"><Alert type="error">{error}</Alert></div>}
      <section className="grid gap-4 lg:grid-cols-3">
        <div className="rounded-lg border border-slate-200 bg-white p-5 lg:col-span-2">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">{reserva.hospede.nome}</h2>
              <p className="text-sm text-slate-500">Quarto {reserva.quarto_numero} · {formatDate(reserva.data_entrada)} a {formatDate(reserva.data_saida)}</p>
            </div>
            <Badge value={reserva.status} />
          </div>
          <dl className="mt-5 grid gap-4 sm:grid-cols-3">
            <div><dt className="text-xs text-slate-500">Valor total</dt><dd className="font-semibold">{formatCurrency(reserva.valor_total)}</dd></div>
            <div><dt className="text-xs text-slate-500">Total pago</dt><dd className="font-semibold">{formatCurrency(reserva.total_pago)}</dd></div>
            <div><dt className="text-xs text-slate-500">Saldo</dt><dd className="font-semibold">{formatCurrency(reserva.saldo_pendente)}</dd></div>
          </dl>
          <div className="mt-5 flex flex-wrap gap-2">
            <Button variant="secondary" onClick={() => action(`/api/reservas/${reserva.id}/confirmar`)} disabled={reserva.status !== 'PENDENTE'}>Confirmar</Button>
            <Button variant="secondary" onClick={() => action(`/api/reservas/${reserva.id}/check-in`, { observacoes: '' })} disabled={reserva.status !== 'CONFIRMADA'}>Check-in</Button>
            <Button variant="secondary" onClick={() => action(`/api/reservas/${reserva.id}/check-out`, { observacoes: '' })} disabled={reserva.status !== 'EM_ANDAMENTO'}>Check-out</Button>
            <Button variant="danger" onClick={() => action(`/api/reservas/${reserva.id}/cancelar`)} disabled={['CONCLUIDA', 'CANCELADA'].includes(reserva.status)}>Cancelar</Button>
          </div>
        </div>
        <div className="rounded-lg border border-slate-200 bg-white p-5">
          <h3 className="font-semibold text-slate-900">Quarto</h3>
          <p className="mt-2 text-sm text-slate-600">{reserva.quarto.tipo.descricao}</p>
          <div className="mt-3"><Badge value={reserva.quarto.status.descricao} /></div>
        </div>
      </section>
      <section className="mt-6">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Pagamentos</h2>
        <DataTable<Pagamento>
          data={pagamentos}
          getKey={(item) => item.id}
          columns={[
            { header: 'Data', render: (item) => formatDateTime(item.data_pagamento) },
            { header: 'Método', render: (item) => item.metodo.descricao },
            { header: 'Valor', render: (item) => formatCurrency(item.valor) },
            { header: 'Observações', render: (item) => item.observacoes ?? '-' }
          ]}
        />
      </section>
    </>
  )
}
