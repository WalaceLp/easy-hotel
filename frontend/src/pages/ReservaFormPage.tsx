import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Button } from '../components/Button'
import { SelectField, TextAreaField, TextField } from '../components/FormField'
import { PageHeader } from '../components/PageHeader'
import { reservaSchema } from '../schemas/forms'
import { api, getApiError } from '../services/api'
import type { Hospede, Quarto } from '../types/api'

type ReservaForm = z.infer<typeof reservaSchema>

export function ReservaFormPage() {
  const navigate = useNavigate()
  const [hospedes, setHospedes] = useState<Hospede[]>([])
  const [quartos, setQuartos] = useState<Quarto[]>([])
  const [error, setError] = useState('')
  const { register, watch, handleSubmit, formState: { errors, isSubmitting } } = useForm<ReservaForm>({
    resolver: zodResolver(reservaSchema)
  })
  const entrada = watch('data_entrada')
  const saida = watch('data_saida')

  useEffect(() => {
    api.get<Hospede[]>('/api/hospedes').then((response) => setHospedes(response.data))
  }, [])

  useEffect(() => {
    if (entrada && saida && saida > entrada) {
      api.get<Quarto[]>('/api/quartos/disponiveis', { params: { data_entrada: entrada, data_saida: saida } }).then((response) => setQuartos(response.data))
    }
  }, [entrada, saida])

  async function onSubmit(data: ReservaForm) {
    setError('')
    try {
      const response = await api.post('/api/reservas', data)
      navigate(`/reservas/${response.data.id}`)
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <>
      <PageHeader title="Nova reserva" action={<Link to="/reservas"><Button variant="secondary">Voltar</Button></Link>} />
      <form className="max-w-3xl space-y-4 rounded-lg border border-slate-200 bg-white p-5" onSubmit={handleSubmit(onSubmit)}>
        {error && <Alert type="error">{error}</Alert>}
        <div className="grid gap-4 sm:grid-cols-2">
          <TextField label="Entrada" type="date" error={errors.data_entrada} {...register('data_entrada')} />
          <TextField label="Saída" type="date" error={errors.data_saida} {...register('data_saida')} />
        </div>
        <SelectField label="Hóspede" error={errors.hospede_id} {...register('hospede_id')}>
          <option value="">Selecione</option>
          {hospedes.map((hospede) => <option key={hospede.id} value={hospede.id}>{hospede.nome}</option>)}
        </SelectField>
        <SelectField label="Quarto disponível" error={errors.quarto_numero} {...register('quarto_numero')}>
          <option value="">Selecione o período</option>
          {quartos.map((quarto) => <option key={quarto.numero} value={quarto.numero}>{quarto.numero} - {quarto.tipo.descricao}</option>)}
        </SelectField>
        <TextField label="Quantidade de hóspedes" type="number" error={errors.quantidade_hospedes} {...register('quantidade_hospedes')} />
        <TextAreaField label="Observações" error={errors.observacoes} {...register('observacoes')} />
        <Button disabled={isSubmitting}>Criar reserva</Button>
      </form>
    </>
  )
}
