import { BedDouble, CalendarDays, CreditCard, FileBarChart, Hotel, LogOut, Menu, Users, X } from 'lucide-react'
import { useState } from 'react'
import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { Button } from '../components/Button'
import { useAuth } from '../hooks/useAuth'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: FileBarChart },
  { to: '/hospedes', label: 'Hóspedes', icon: Users },
  { to: '/quartos', label: 'Quartos', icon: Hotel },
  { to: '/tipos-quarto', label: 'Tipos', icon: BedDouble },
  { to: '/reservas', label: 'Reservas', icon: CalendarDays },
  { to: '/pagamentos', label: 'Pagamentos', icon: CreditCard },
  { to: '/usuarios', label: 'Usuários', icon: Users },
  { to: '/relatorios', label: 'Relatórios', icon: FileBarChart }
]

export function AppLayout() {
  const { usuario, logout } = useAuth()
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  const sidebar = (
    <aside className="flex h-full w-72 flex-col border-r border-slate-200 bg-white">
      <div className="flex h-16 items-center gap-3 border-b border-slate-200 px-5">
        <div className="grid h-9 w-9 place-items-center rounded-md bg-blue-700 text-white">
          <Hotel size={18} />
        </div>
        <div>
          <p className="font-bold text-slate-900">Easy Hotel</p>
          <p className="text-xs text-slate-500">Gestão hoteleira</p>
        </div>
      </div>
      <nav className="flex-1 space-y-1 p-3">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={() => setOpen(false)}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium ${
                isActive ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`
            }
          >
            <item.icon size={18} />
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="fixed inset-y-0 left-0 hidden lg:block">{sidebar}</div>
      {open && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div className="absolute inset-0 bg-slate-900/40" onClick={() => setOpen(false)} />
          <div className="absolute inset-y-0 left-0">{sidebar}</div>
        </div>
      )}
      <div className="lg:pl-72">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6">
          <Button type="button" variant="secondary" className="h-10 w-10 p-0 lg:hidden" onClick={() => setOpen(!open)}>
            {open ? <X size={18} /> : <Menu size={18} />}
          </Button>
          <div className="ml-auto flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-semibold text-slate-900">{usuario?.nome}</p>
              <p className="text-xs text-slate-500">{usuario?.perfil.nome}</p>
            </div>
            <Button type="button" variant="secondary" className="gap-2" onClick={handleLogout}>
              <LogOut size={16} />
              Sair
            </Button>
          </div>
        </header>
        <main className="p-4 sm:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
