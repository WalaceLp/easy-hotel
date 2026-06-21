export function Loading({ fullScreen = false }: { fullScreen?: boolean }) {
  return (
    <div className={`grid place-items-center ${fullScreen ? 'min-h-screen' : 'min-h-40'}`}>
      <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-600 shadow-sm">
        <span className="h-5 w-5 animate-spin rounded-full border-2 border-blue-100 border-t-blue-700" />
        Carregando
      </div>
    </div>
  )
}
