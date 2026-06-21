const statusStyles: Record<string, string> = {
  PENDENTE: 'bg-amber-50 text-amber-800 ring-amber-200',
  CONFIRMADA: 'bg-blue-50 text-blue-800 ring-blue-200',
  EM_ANDAMENTO: 'bg-indigo-50 text-indigo-800 ring-indigo-200',
  CONCLUIDA: 'bg-emerald-50 text-emerald-800 ring-emerald-200',
  CANCELADA: 'bg-red-50 text-red-800 ring-red-200',
  DISPONIVEL: 'bg-emerald-50 text-emerald-800 ring-emerald-200',
  OCUPADO: 'bg-indigo-50 text-indigo-800 ring-indigo-200',
  RESERVADO: 'bg-blue-50 text-blue-800 ring-blue-200',
  MANUTENCAO: 'bg-amber-50 text-amber-800 ring-amber-200',
  INATIVO: 'bg-slate-100 text-slate-700 ring-slate-200'
}

export function Badge({ value }: { value: string }) {
  return (
    <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-bold ring-1 ${statusStyles[value] ?? 'bg-slate-100 text-slate-700 ring-slate-200'}`}>
      {value.split('_').join(' ')}
    </span>
  )
}
