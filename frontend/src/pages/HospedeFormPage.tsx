import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Button } from '../components/Button'
import { TextField } from '../components/FormField'
import { PageHeader } from '../components/PageHeader'
import { hospedeSchema } from '../schemas/forms'
import { api, getApiError } from '../services/api'
import type { Hospede } from '../types/api'

type HospedeForm = z.infer<typeof hospedeSchema>

export function HospedeFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const isEdit = Boolean(id)
  const {
    register,
    reset,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<HospedeForm>({ resolver: zodResolver(hospedeSchema) })

  useEffect(() => {
    if (id) {
      api.get<Hospede>(`/api/hospedes/${id}`).then((response) => reset({
        nome: response.data.nome,
        cpf: response.data.cpf,
        telefone: response.data.telefone ?? '',
        email: response.data.email ?? ''
      }))
    }
  }, [id, reset])

  async function onSubmit(data: HospedeForm) {
    setError('')
    try {
      if (isEdit) await api.put(`/api/hospedes/${id}`, data)
      else await api.post('/api/hospedes', data)
      navigate('/hospedes')
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <>
      <PageHeader title={isEdit ? 'Editar hóspede' : 'Novo hóspede'} action={<Link to="/hospedes"><Button variant="secondary">Voltar</Button></Link>} />
      <form className="max-w-2xl space-y-4 rounded-lg border border-slate-200 bg-white p-5" onSubmit={handleSubmit(onSubmit)}>
        {error && <Alert type="error">{error}</Alert>}
        <TextField label="Nome" error={errors.nome} {...register('nome')} />
        <TextField label="CPF" error={errors.cpf} {...register('cpf')} />
        <TextField label="Telefone" error={errors.telefone} {...register('telefone')} />
        <TextField label="E-mail" error={errors.email} {...register('email')} />
        <Button disabled={isSubmitting}>Salvar</Button>
      </form>
    </>
  )
}
