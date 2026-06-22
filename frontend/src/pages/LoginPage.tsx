import { zodResolver } from '@hookform/resolvers/zod'
import { BedDouble, CalendarCheck, Hotel, ShieldCheck } from 'lucide-react'
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
import { getHomePathForPerfil } from '../utils/permissions'

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

  if (usuario) return <Navigate to={getHomePathForPerfil(usuario.perfil.nome)} replace />

  async function onSubmit(data: LoginForm) {
    setError('')
    try {
      const usuarioAutenticado = await login(data.login, data.senha)
      navigate(getHomePathForPerfil(usuarioAutenticado.perfil.nome))
    } catch (err) {
      setError(getApiError(err))
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-8 text-white">
      <div className="mx-auto grid min-h-[calc(100vh-4rem)] w-full max-w-6xl items-center gap-8 lg:grid-cols-[1.15fr_0.85fr]">
        <section className="hidden lg:block">
          <div className="mb-8 flex items-center gap-3">
            <div className="grid h-12 w-12 place-items-center rounded-md bg-blue-600 shadow-lg shadow-blue-950/40">
              <Hotel size={23} />
            </div>
            <div>
              <p className="text-xl font-bold">Easy Hotel</p>
              <p className="text-sm text-slate-400">Sistema acadêmico de gestão hoteleira</p>
            </div>
          </div>
          <h1 className="max-w-2xl text-4xl font-bold leading-tight text-white">
            Controle reservas, quartos e pagamentos com uma operação mais clara.
          </h1>
          <p className="mt-4 max-w-xl text-base leading-7 text-slate-300">
            Acesse o painel para acompanhar ocupação, check-ins, hóspedes e indicadores administrativos em tempo real.
          </p>
          <div className="mt-8 grid max-w-2xl gap-4 sm:grid-cols-3">
            {[
              { icon: CalendarCheck, label: 'Reservas' },
              { icon: BedDouble, label: 'Quartos' },
              { icon: ShieldCheck, label: 'Perfis' }
            ].map((item) => (
              <div key={item.label} className="rounded-lg border border-white/10 bg-white/5 p-4">
                <item.icon className="mb-3 text-blue-300" size={22} />
                <p className="text-sm font-semibold text-white">{item.label}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="w-full rounded-lg border border-white/10 bg-white p-6 text-slate-900 shadow-2xl shadow-slate-950/40 sm:p-8">
          <div className="mb-7 flex items-center gap-3 lg:hidden">
            <div className="grid h-11 w-11 place-items-center rounded-md bg-blue-700 text-white">
              <Hotel size={22} />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-950">Easy Hotel</h1>
              <p className="text-sm text-slate-500">Acesse sua conta</p>
            </div>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-950">Entrar no sistema</h2>
            <p className="mt-1 text-sm text-slate-500">Use uma das contas de demonstração para apresentar o fluxo.</p>
          </div>
          <form className="mt-6 space-y-4" onSubmit={handleSubmit(onSubmit)}>
          {error && <Alert type="error">{error}</Alert>}
          <TextField label="Login" error={errors.login} {...register('login')} />
          <TextField label="Senha" type="password" error={errors.senha} {...register('senha')} />
          <Button className="w-full" disabled={isSubmitting}>
            Entrar
          </Button>
          </form>
        </section>
      </div>
    </main>
  )
}
