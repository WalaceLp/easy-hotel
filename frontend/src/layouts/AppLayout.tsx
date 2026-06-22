import { BedDouble, CalendarDays, CreditCard, FileBarChart, Hotel, LogOut, Menu, Users, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { Button } from '../components/Button'
import { useAuth } from '../hooks/useAuth'
import type { PerfilNome } from '../types/api'
import { perfilPermitido } from '../utils/permissions'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: FileBarChart, perfis: ['ADMINISTRADOR', 'GERENTE'] },
  { to: '/hospedes', label: 'Hóspedes', icon: Users },
  { to: '/quartos', label: 'Quartos', icon: Hotel },
  { to: '/tipos-quarto', label: 'Tipos', icon: BedDouble, perfis: ['ADMINISTRADOR', 'GERENTE'] },
  { to: '/reservas', label: 'Reservas', icon: CalendarDays },
  { to: '/pagamentos', label: 'Pagamentos', icon: CreditCard, perfis: ['ADMINISTRADOR', 'GERENTE'] },
  { to: '/usuarios', label: 'Usuários', icon: Users, perfis: ['ADMINISTRADOR'] },
  { to: '/relatorios', label: 'Relatórios', icon: FileBarChart, perfis: ['ADMINISTRADOR', 'GERENTE'] }
] satisfies Array<{
  to: string
  label: string
  icon: typeof FileBarChart
  perfis?: PerfilNome[]
}>

export function AppLayout() {
  const { usuario, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()
  const visibleNavItems = navItems.filter((item) => perfilPermitido(usuario?.perfil.nome, item.perfis))

  function handleLogout() {
    logout()
    navigate('/login')
  }

  const sidebar = (
    <aside className="flex h-full w-72 flex-col border-r border-slate-800 bg-slate-950 text-white">
      <div className="flex h-20 items-center gap-3 border-b border-white/10 px-5">
        <div className="grid h-11 w-11 place-items-center rounded-md bg-blue-600 text-white shadow-lg shadow-blue-950/40">
          <Hotel size={18} />
        </div>
        <div>
          <p className="font-bold text-white">Easy Hotel</p>
          <p className="text-xs text-slate-400">Gestão hoteleira</p>
        </div>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {visibleNavItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={() => setOpen(false)}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-semibold transition ${
                isActive ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-300 hover:bg-white/10 hover:text-white'
              }`
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
      </nav>
      <div className="border-t border-white/10 p-4 text-xs leading-relaxed text-slate-400">
        Operação, reservas e financeiro em uma única visão.
      </div>
    </aside>
  )

  return (
    <div className="min-h-screen bg-slate-100">
      <div className="fixed inset-y-0 left-0 hidden lg:block">{sidebar}</div>
      {open && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="absolute inset-0 bg-slate-950/50 backdrop-blur-sm" onClick={() => setOpen(false)} />
          <div className="absolute inset-y-0 left-0">{sidebar}</div>
        </div>
      )}
      <div className="lg:pl-72">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/90 px-4 shadow-sm backdrop-blur sm:px-6">
          <Button type="button" variant="secondary" className="h-10 w-10 p-0 lg:hidden" onClick={() => setOpen(!open)}>
            {open ? <X size={18} /> : <Menu size={18} />}
          </Button>
          <div className="ml-auto flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-semibold text-slate-900">{usuario?.nome}</p>
              <p className="text-xs text-slate-500">{usuario?.perfil.nome}</p>
            </div>
            <div className="grid h-10 w-10 place-items-center rounded-md bg-blue-50 text-sm font-bold text-blue-700 ring-1 ring-blue-100">
              {usuario?.nome?.slice(0, 1)}
            </div>
            <Button type="button" variant="secondary" onClick={handleLogout}>
              <LogOut size={16} />
              Sair
            </Button>
          </div>
        </header>
        <main className="mx-auto w-full max-w-7xl p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
