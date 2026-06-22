import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Button } from '../components/Button'
import { DataTable } from '../components/DataTable'
import { SelectField, TextAreaField, TextField } from '../components/FormField'
import { PageHeader } from '../components/PageHeader'
import { pagamentoSchema } from '../schemas/forms'
import { api, getApiError } from '../services/api'
import type { MetodoPagamento, Pagamento, Reserva } from '../types/api'
import { formatCurrency, formatDateTime, formatPaymentMethod } from '../utils/formatters'

type PagamentoForm = z.infer<typeof pagamentoSchema>

export function PagamentosPage() {
  const [pagamentos, setPagamentos] = useState<Pagamento[]>([])
  const [reservas, setReservas] = useState<Reserva[]>([])
  const [metodos, setMetodos] = useState<MetodoPagamento[]>([])
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<PagamentoForm>({
    resolver: zodResolver(pagamentoSchema)
  })

  function load() {
    Promise.all([
      api.get<Pagamento[]>('/api/pagamentos').catch(() => ({ data: [] as Pagamento[] })),
      api.get<Reserva[]>('/api/reservas'),
      api.get<MetodoPagamento[]>('/api/metodos-pagamento')
    ]).then(([pagamentosResponse, reservasResponse, metodosResponse]) => {
      setPagamentos(pagamentosResponse.data)
      setReservas(reservasResponse.data.filter((reserva) => Number(reserva.saldo_pendente) > 0))
      setMetodos(metodosResponse.data.filter((item) => item.ativo))
    })
  }

  useEffect(load, [])

  async function onSubmit(data: PagamentoForm) {
    setError('')
    setSuccess('')
    try {
      await api.post('/api/pagamentos', { ...data, valor: String(data.valor) })
      reset()
      setSuccess('Pagamento registrado com sucesso.')
      load()
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <>
      <PageHeader title="Pagamentos" description="Registro financeiro de reservas." />
      <section className="mb-6 rounded-lg border border-slate-200 bg-white p-5">
        <form className="grid gap-4 lg:grid-cols-4" onSubmit={handleSubmit(onSubmit)}>
          {error && <div className="lg:col-span-4"><Alert type="error">{error}</Alert></div>}
          {success && <div className="lg:col-span-4"><Alert type="success">{success}</Alert></div>}
          <SelectField label="Reserva" error={errors.reserva_id} {...register('reserva_id')}>
            <option value="">Selecione</option>
            {reservas.map((reserva) => <option key={reserva.id} value={reserva.id}>#{reserva.id} - {reserva.hospede.nome} - saldo {formatCurrency(reserva.saldo_pendente)}</option>)}
          </SelectField>
          <SelectField label="Método" error={errors.metodo_id} {...register('metodo_id')}>
            <option value="">Selecione</option>
            {metodos.map((metodo) => <option key={metodo.id} value={metodo.id}>{formatPaymentMethod(metodo.descricao)}</option>)}
          </SelectField>
          <TextField label="Valor" type="number" step="0.01" error={errors.valor} {...register('valor')} />
          <div className="flex items-end"><Button disabled={isSubmitting}>Registrar</Button></div>
          <div className="lg:col-span-4">
            <TextAreaField label="Observações" error={errors.observacoes} {...register('observacoes')} />
          </div>
        </form>
      </section>
      <DataTable<Pagamento>
        data={pagamentos}
        getKey={(item) => item.id}
        columns={[
          { header: 'Data', render: (item) => formatDateTime(item.data_pagamento) },
          { header: 'Reserva', render: (item) => `#${item.reserva_id}` },
          { header: 'Método', render: (item) => formatPaymentMethod(item.metodo.descricao) },
          { header: 'Valor', render: (item) => formatCurrency(item.valor) }
        ]}
      />
    </>
  )
}
