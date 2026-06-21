import { useMemo, useState } from 'react'

export function usePagedData<T>(data: T[], pageSize = 8) {
  const [page, setPage] = useState(1)
  const pageData = useMemo(() => data.slice((page - 1) * pageSize, page * pageSize), [data, page, pageSize])
  return { page, setPage, pageSize, pageData }
}
