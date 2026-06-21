import { zodResolver } from '@hookform/resolvers/zod'
import { Hotel } from 'lucide-react'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Navigate, useNavigate } from 'react-router-dom'
import { z } from 'zod'
import { Alert } from '../components/Alert'
import { Button } from '../components/Button'
import { TextField } from '../components/FormField'
import { useAuth } from '../hooks/useAuth'
import { getApiError } from '../services/api'
import { loginSchema } from '../schemas/forms'

type LoginForm = z.infer<typeof loginSchema>

export function LoginPage() {
  const { login, usuario } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting }
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: { login: 'admin', senha: 'admin123' }
  })

  if (usuario) return <Navigate to="/dashboard" replace />

  async function onSubmit(data: LoginForm) {
    setError('')
    try {
      await login(data.login, data.senha)
      navigate('/dashboard')
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-slate-100 px-4">
      <section className="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-6 flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-md bg-blue-700 text-white">
            <Hotel size={22} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Easy Hotel</h1>
            <p className="text-sm text-slate-500">Acesse sua conta</p>
          </div>
        </div>
        <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
          {error && <Alert type="error">{error}</Alert>}
          <TextField label="Login" error={errors.login} {...register('login')} />
          <TextField label="Senha" type="password" error={errors.senha} {...register('senha')} />
          <Button className="w-full" disabled={isSubmitting}>
            Entrar
          </Button>
        </form>
      </section>
    </main>
  )
}
