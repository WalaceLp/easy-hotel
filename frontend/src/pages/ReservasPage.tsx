import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Badge } from '../components/Badge'
import { Button } from '../components/Button'
import { DataTable } from '../components/DataTable'
import { PageHeader } from '../components/PageHeader'
import { SearchInput } from '../components/SearchInput'
import { api } from '../services/api'
import type { Reserva } from '../types/api'
import { formatCurrency, formatDate } from '../utils/formatters'

export function ReservasPage() {
  const [reservas, setReservas] = useState<Reserva[]>([])
  const [search, setSearch] = useState('')

  useEffect(() => {
    api.get<Reserva[]>('/api/reservas').then((response) => setReservas(response.data))
  }, [])

  const filtered = useMemo(
    () => reservas.filter((item) => `${item.hospede.nome} ${item.quarto_numero} ${item.status}`.toLowerCase().includes(search.toLowerCase())),
    [reservas, search]
  )

  return (
    <>
      <PageHeader title="Reservas" description="Reservas, estadias e status." action={<Link to="/reservas/nova"><Button>Nova reserva</Button></Link>} />
      <div className="mb-4 max-w-md">
        <SearchInput value={search} onChange={setSearch} placeholder="Buscar por hóspede, quarto ou status" />
      </div>
      <DataTable<Reserva>
        data={filtered}
        getKey={(item) => item.id}
        columns={[
          { header: 'Hóspede', render: (item) => item.hospede.nome },
          { header: 'Quarto', render: (item) => item.quarto_numero },
          { header: 'Período', render: (item) => `${formatDate(item.data_entrada)} a ${formatDate(item.data_saida)}` },
          { header: 'Status', render: (item) => <Badge value={item.status} /> },
          { header: 'Valor', render: (item) => formatCurrency(item.valor_total) },
          { header: 'Ações', render: (item) => <Link className="font-semibold text-blue-700" to={`/reservas/${item.id}`}>Detalhes</Link> }
        ]}
      />
    </>
  )
}
