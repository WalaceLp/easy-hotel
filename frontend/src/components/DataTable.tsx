import { EmptyState } from './EmptyState'

export type Column<T> = {
  header: string
  render: (item: T) => React.ReactNode
}

type DataTableProps<T> = {
  columns: Column<T>[]
  data: T[]
  getKey: (item: T) => string | number
}

export function DataTable<T>({ columns, data, getKey }: DataTableProps<T>) {
  if (data.length === 0) return <EmptyState />
  return (
    <div className="overflow-hidden rounded-lg border border-slate-200 bg-white">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th key={column.header} className="px-4 py-3 text-left text-xs font-semibold uppercase text-slate-500">
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.map((item) => (
              <tr key={getKey(item)} className="hover:bg-slate-50">
                {columns.map((column) => (
                  <td key={column.header} className="px-4 py-3 text-sm text-slate-700">
                    {column.render(item)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
