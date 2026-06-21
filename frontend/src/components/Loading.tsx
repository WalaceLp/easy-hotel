export function Loading({ fullScreen = false }: { fullScreen?: boolean }) {
  return (
    <div className={`grid place-items-center ${fullScreen ? 'min-h-screen' : 'min-h-40'}`}>
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-100 border-t-blue-700" />
    </div>
  )
}
