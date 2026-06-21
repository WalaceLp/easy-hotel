const statusStyles: Record<string, string> = {
  PENDENTE: 'bg-amber-100 text-amber-800',
  CONFIRMADA: 'bg-blue-100 text-blue-800',
  EM_ANDAMENTO: 'bg-violet-100 text-violet-800',
  CONCLUIDA: 'bg-emerald-100 text-emerald-800',
  CANCELADA: 'bg-red-100 text-red-800',
  DISPONIVEL: 'bg-emerald-100 text-emerald-800',
  OCUPADO: 'bg-violet-100 text-violet-800',
  RESERVADO: 'bg-blue-100 text-blue-800',
  MANUTENCAO: 'bg-amber-100 text-amber-800',
  INATIVO: 'bg-slate-200 text-slate-700'
}

export function Badge({ value }: { value: string }) {
  return (
    <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${statusStyles[value] ?? 'bg-slate-100 text-slate-700'}`}>
      {value.split('_').join(' ')}
    </span>
  )
}
