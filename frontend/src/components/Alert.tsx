type AlertProps = {
  type?: 'success' | 'error' | 'info'
  children: React.ReactNode
}

const styles = {
  success: 'border-emerald-200 bg-emerald-50 text-emerald-800 shadow-emerald-100/70',
  error: 'border-red-200 bg-red-50 text-red-800 shadow-red-100/70',
  info: 'border-blue-200 bg-blue-50 text-blue-800 shadow-blue-100/70'
}

export function Alert({ type = 'info', children }: AlertProps) {
  return <div className={`rounded-md border px-4 py-3 text-sm font-medium shadow-sm ${styles[type]}`}>{children}</div>
}
