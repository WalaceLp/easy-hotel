import { Inbox } from 'lucide-react'

export function EmptyState({ message = 'Nenhum registro encontrado.' }: { message?: string }) {
  return (
    <div className="rounded-lg border border-dashed border-slate-300 bg-white p-10 text-center text-sm text-slate-500 shadow-sm">
      <div className="mx-auto mb-3 grid h-11 w-11 place-items-center rounded-md bg-slate-100 text-slate-500">
        <Inbox size={20} />
      </div>
      <p className="font-medium">{message}</p>
    </div>
  )
}
