import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Badge } from '../components/Badge'
import { Button } from '../components/Button'
import { DataTable } from '../components/DataTable'
import { TextField } from '../components/FormField'
import { Modal } from '../components/Modal'
import { PageHeader } from '../components/PageHeader'
import { tipoQuartoSchema } from '../schemas/forms'
import { api, getApiError } from '../services/api'
import type { TipoQuarto } from '../types/api'
import { formatCurrency } from '../utils/formatters'

type TipoForm = z.infer<typeof tipoQuartoSchema>

export function TiposQuartoPage() {
  const [tipos, setTipos] = useState<TipoQuarto[]>([])
  const [open, setOpen] = useState(false)
  const [editing, setEditing] = useState<TipoQuarto | null>(null)
  const [error, setError] = useState('')
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<TipoForm>({
    resolver: zodResolver(tipoQuartoSchema),
    defaultValues: { ativo: true }
  })

  function load() {
    api.get<TipoQuarto[]>('/api/tipos-quarto').then((response) => setTipos(response.data))
  }

  useEffect(load, [])

  function novo() {
    setEditing(null)
    reset({ descricao: '', preco_base: 0, capacidade: 1, ativo: true })
    setOpen(true)
  }

  function editar(tipo: TipoQuarto) {
    setEditing(tipo)
    reset({ descricao: tipo.descricao, preco_base: Number(tipo.preco_base), capacidade: tipo.capacidade, ativo: tipo.ativo })
    setOpen(true)
  }

  async function onSubmit(data: TipoForm) {
    setError('')
    try {
      const payload = { ...data, preco_base: String(data.preco_base) }
      if (editing) await api.put(`/api/tipos-quarto/${editing.id}`, payload)
      else await api.post('/api/tipos-quarto', payload)
      setOpen(false)
      load()
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <>
      <PageHeader title="Tipos de quarto" description="Categorias, preço-base e capacidade." action={<Button onClick={novo}>Novo tipo</Button>} />
      <DataTable<TipoQuarto>
        data={tipos}
        getKey={(item) => item.id}
        columns={[
          { header: 'Descrição', render: (item) => item.descricao },
          { header: 'Preço-base', render: (item) => formatCurrency(item.preco_base) },
          { header: 'Capacidade', render: (item) => item.capacidade },
          { header: 'Status', render: (item) => <Badge value={item.ativo ? 'ATIVO' : 'INATIVO'} /> },
          { header: 'Ações', render: (item) => <button className="font-semibold text-blue-700" onClick={() => editar(item)}>Editar</button> }
        ]}
      />
      <Modal open={open} title={editing ? 'Editar tipo' : 'Novo tipo'} onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          {error && <Alert type="error">{error}</Alert>}
          <TextField label="Descrição" error={errors.descricao} {...register('descricao')} />
          <TextField label="Preço-base" type="number" step="0.01" error={errors.preco_base} {...register('preco_base')} />
          <TextField label="Capacidade" type="number" error={errors.capacidade} {...register('capacidade')} />
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
