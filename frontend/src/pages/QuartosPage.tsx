import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Badge } from '../components/Badge'
import { Button } from '../components/Button'
import { DataTable } from '../components/DataTable'
import { SelectField, TextAreaField, TextField } from '../components/FormField'
import { Modal } from '../components/Modal'
import { PageHeader } from '../components/PageHeader'
import { quartoSchema } from '../schemas/forms'
import { api, getApiError } from '../services/api'
import type { Quarto, StatusQuarto, TipoQuarto } from '../types/api'

type QuartoForm = z.infer<typeof quartoSchema>

export function QuartosPage() {
  const [quartos, setQuartos] = useState<Quarto[]>([])
  const [tipos, setTipos] = useState<TipoQuarto[]>([])
  const [status, setStatus] = useState<StatusQuarto[]>([])
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState<Quarto | null>(null)
  const [error, setError] = useState('')
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<QuartoForm>({
    resolver: zodResolver(quartoSchema),
    defaultValues: { ativo: true }
  })

  function load() {
    Promise.all([
      api.get<Quarto[]>('/api/quartos'),
      api.get<TipoQuarto[]>('/api/tipos-quarto'),
      api.get<StatusQuarto[]>('/api/status-quarto')
    ]).then(([quartosResponse, tiposResponse, statusResponse]) => {
      setQuartos(quartosResponse.data)
      setTipos(tiposResponse.data)
      setStatus(statusResponse.data)
    })
  }

  useEffect(load, [])

  function novo() {
    setEditing(null)
    reset({ numero: '', tipo_id: tipos[0]?.id ?? 0, status_id: status[0]?.id ?? 0, observacoes: '', ativo: true })
    setOpen(true)
  }

  function editar(quarto: Quarto) {
    setEditing(quarto)
    reset({ numero: quarto.numero, tipo_id: quarto.tipo_id, status_id: quarto.status_id, observacoes: quarto.observacoes ?? '', ativo: quarto.ativo })
    setOpen(true)
  }

  async function onSubmit(data: QuartoForm) {
    setError('')
    try {
      if (editing) await api.put(`/api/quartos/${editing.numero}`, data)
      else await api.post('/api/quartos', data)
      setOpen(false)
      load()
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <>
      <PageHeader title="Quartos" description="Unidades, status e disponibilidade." action={<Button onClick={novo}>Novo quarto</Button>} />
      <DataTable<Quarto>
        data={quartos}
        getKey={(item) => item.numero}
        columns={[
          { header: 'Número', render: (item) => item.numero },
          { header: 'Tipo', render: (item) => item.tipo.descricao },
          { header: 'Status', render: (item) => <Badge value={item.status.descricao} /> },
          { header: 'Ativo', render: (item) => item.ativo ? 'Sim' : 'Não' },
          { header: 'Ações', render: (item) => <button className="font-semibold text-blue-700" onClick={() => editar(item)}>Editar</button> }
        ]}
      />
      <Modal open={open} title={editing ? 'Editar quarto' : 'Novo quarto'} onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          {error && <Alert type="error">{error}</Alert>}
          <TextField label="Número" disabled={Boolean(editing)} error={errors.numero} {...register('numero')} />
          <SelectField label="Tipo" error={errors.tipo_id} {...register('tipo_id')}>
            <option value="">Selecione</option>
            {tipos.map((tipo) => <option key={tipo.id} value={tipo.id}>{tipo.descricao}</option>)}
          </SelectField>
          <SelectField label="Status" error={errors.status_id} {...register('status_id')}>
            <option value="">Selecione</option>
            {status.map((item) => <option key={item.id} value={item.id}>{item.descricao}</option>)}
          </SelectField>
          <TextAreaField label="Observações" error={errors.observacoes} {...register('observacoes')} />
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" {...register('ativo')} />
            Ativo
          </label>
          <Button disabled={isSubmitting}>Salvar</Button>
        </form>
      </Modal>
    </>
  )
}
