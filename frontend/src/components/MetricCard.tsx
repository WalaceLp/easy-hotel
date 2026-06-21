import type { LucideIcon } from 'lucide-react'

type MetricCardProps = {
  label: string
  value: React.ReactNode
  hint?: string
  icon?: LucideIcon
  tone?: 'blue' | 'emerald' | 'amber' | 'red' | 'slate'
}

const tones = {
  blue: 'bg-blue-50 text-blue-700 ring-blue-100',
  emerald: 'bg-emerald-50 text-emerald-700 ring-emerald-100',
  amber: 'bg-amber-50 text-amber-700 ring-amber-100',
  red: 'bg-red-50 text-red-700 ring-red-100',
  slate: 'bg-slate-100 text-slate-700 ring-slate-200'
}

export function MetricCard({ label, value, hint, icon: Icon, tone = 'blue' }: MetricCardProps) {
  return (
    <div className="surface p-5 transition hover:-translate-y-0.5 hover:shadow-md hover:shadow-slate-200/80">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-semibold text-slate-500">{label}</p>
          <p className="mt-2 text-2xl font-bold text-slate-950">{value}</p>
        </div>
        {Icon && (
          <span className={`grid h-11 w-11 shrink-0 place-items-center rounded-md ring-1 ${tones[tone]}`}>
            <Icon size={20} />
          </span>
        )}
      </div>
      {hint && <p className="mt-3 text-xs font-medium text-slate-500">{hint}</p>}
    </div>
  )
}
