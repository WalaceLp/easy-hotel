import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Badge } from '../components/Badge'
import { Button } from '../components/Button'
import { DataTable } from '../components/DataTable'
import { SelectField, TextField } from '../components/FormField'
import { Modal } from '../components/Modal'
import { PageHeader } from '../components/PageHeader'
import { useAuth } from '../hooks/useAuth'
import { usuarioSchema } from '../schemas/forms'
import { api, getApiError } from '../services/api'
import type { Perfil, Usuario } from '../types/api'

type UsuarioForm = z.infer<typeof usuarioSchema>

export function UsuariosPage() {
  const { hasPerfil } = useAuth()
  const [usuarios, setUsuarios] = useState<Usuario[]>([])
  const [perfis, setPerfis] = useState<Perfil[]>([])
  const [open, setOpen] = useState(false)
  const [error, setError] = useState('')
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<UsuarioForm>({
    resolver: zodResolver(usuarioSchema),
    defaultValues: { ativo: true }
  })

  function load() {
    if (!hasPerfil('ADMINISTRADOR')) return
    Promise.all([api.get<Usuario[]>('/api/usuarios'), api.get<Perfil[]>('/api/perfis')]).then(([usuariosResponse, perfisResponse]) => {
      setUsuarios(usuariosResponse.data)
      setPerfis(perfisResponse.data)
    })
  }

  useEffect(load, [hasPerfil])

  async function onSubmit(data: UsuarioForm) {
    setError('')
    try {
      await api.post('/api/usuarios', data)
      reset({ nome: '', login: '', senha: '', perfil_id: 0, ativo: true })
      setOpen(false)
      load()
    } catch (err) {
      setError(getApiError(err))
    }
  }

  if (!hasPerfil('ADMINISTRADOR')) {
    return <Alert type="error">Apenas administradores podem gerenciar usuários.</Alert>
  }

  return (
    <>
      <PageHeader title="Usuários" description="Controle de acesso por perfil." action={<Button onClick={() => setOpen(true)}>Novo usuário</Button>} />
      <DataTable<Usuario>
        data={usuarios}
        getKey={(item) => item.id}
        columns={[
          { header: 'Nome', render: (item) => item.nome },
          { header: 'Login', render: (item) => item.login },
          { header: 'Perfil', render: (item) => item.perfil.nome },
          { header: 'Status', render: (item) => <Badge value={item.ativo ? 'ATIVO' : 'INATIVO'} /> }
        ]}
      />
      <Modal open={open} title="Novo usuário" onClose={() => setOpen(false)}>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          {error && <Alert type="error">{error}</Alert>}
          <TextField label="Nome" error={errors.nome} {...register('nome')} />
          <TextField label="Login" error={errors.login} {...register('login')} />
          <TextField label="Senha" type="password" error={errors.senha} {...register('senha')} />
          <SelectField label="Perfil" error={errors.perfil_id} {...register('perfil_id')}>
            <option value="">Selecione</option>
            {perfis.map((perfil) => <option key={perfil.id} value={perfil.id}>{perfil.nome}</option>)}
          </SelectField>
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input type="checkbox" {...register('ativo')} />
            Ativo
          </label>
          <Button disabled={isSubmitting}>Criar usuário</Button>
        </form>
      </Modal>
    </>
  )
}
