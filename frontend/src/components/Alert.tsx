type AlertProps = {
  type?: 'success' | 'error' | 'info'
  children: React.ReactNode
}

const styles = {
  success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
  error: 'border-red-200 bg-red-50 text-red-800',
  info: 'border-blue-200 bg-blue-50 text-blue-800'
}

export function Alert({ type = 'info', children }: AlertProps) {
  return <div className={`rounded-md border px-4 py-3 text-sm ${styles[type]}`}>{children}</div>
}
