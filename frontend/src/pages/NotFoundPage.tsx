import { Link } from 'react-router-dom'
import { Button } from '../components/Button'

export function NotFoundPage() {
  return (
    <main className="grid min-h-screen place-items-center bg-slate-50 p-6">
      <section className="text-center">
        <p className="text-sm font-semibold uppercase text-blue-700">404</p>
        <h1 className="mt-2 text-3xl font-bold text-slate-900">Página não encontrada</h1>
        <p className="mt-2 text-slate-500">O endereço informado não existe no Easy Hotel.</p>
        <Link to="/dashboard" className="mt-6 inline-block">
          <Button>Voltar ao dashboard</Button>
        </Link>
      </section>
    </main>
  )
}
