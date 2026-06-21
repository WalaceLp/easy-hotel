import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { Button } from '../components/Button'
import { ConfirmDialog } from '../components/ConfirmDialog'
import { DataTable } from '../components/DataTable'
import { PageHeader } from '../components/PageHeader'
import { Pagination } from '../components/Pagination'
import { SearchInput } from '../components/SearchInput'
import { usePagedData } from '../hooks/usePagedData'
import { api, getApiError } from '../services/api'
import type { Hospede } from '../types/api'

export function HospedesPage() {
  const [hospedes, setHospedes] = useState<Hospede[]>([])
  const [search, setSearch] = useState('')
  const [deleteId, setDeleteId] = useState<number | null>(null)
  const [error, setError] = useState('')

  function load() {
    api.get<Hospede[]>('/api/hospedes').then((response) => setHospedes(response.data))
  }

  useEffect(load, [])

  const filtered = useMemo(
    () => hospedes.filter((item) => `${item.nome} ${item.cpf} ${item.email ?? ''}`.toLowerCase().includes(search.toLowerCase())),
    [hospedes, search]
  )
  const { page, setPage, pageSize, pageData } = usePagedData(filtered)

  async function excluir() {
    if (!deleteId) return
    setError('')
    try {
      await api.delete(`/api/hospedes/${deleteId}`)
      setDeleteId(null)
      load()
    } catch (err) {
      setError(getApiError(err))
      setDeleteId(null)
    }
  }

  return (
    <>
      <PageHeader
        title="Hóspedes"
        description="Cadastro e manutenção de hóspedes."
        action={<Link to="/hospedes/novo"><Button>Novo hóspede</Button></Link>}
      />
      {error && <div className="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">{error}</div>}
      <div className="mb-4 max-w-md">
        <SearchInput value={search} onChange={setSearch} placeholder="Buscar por nome, CPF ou e-mail" />
      </div>
      <DataTable<Hospede>
        data={pageData}
        getKey={(item) => item.id}
        columns={[
          { header: 'Nome', render: (item) => item.nome },
          { header: 'CPF', render: (item) => item.cpf },
          { header: 'Telefone', render: (item) => item.telefone ?? '-' },
          { header: 'E-mail', render: (item) => item.email ?? '-' },
          {
            header: 'Ações',
            render: (item) => (
              <div className="flex gap-2">
                <Link to={`/hospedes/${item.id}/editar`} className="text-sm font-semibold text-blue-700">Editar</Link>
                <button className="text-sm font-semibold text-red-600" onClick={() => setDeleteId(item.id)}>Excluir</button>
              </div>
            )
          }
        ]}
      />
      <Pagination page={page} total={filtered.length} pageSize={pageSize} onPageChange={setPage} />
      <ConfirmDialog
        open={deleteId !== null}
        title="Excluir hóspede"
        message="Confirme a exclusão deste hóspede."
        onCancel={() => setDeleteId(null)}
        onConfirm={excluir}
      />
    </>
  )
}
