import { forwardRef, InputHTMLAttributes, SelectHTMLAttributes, TextareaHTMLAttributes } from 'react'
import { FieldError } from 'react-hook-form'

type BaseProps = {
  label: string
  error?: FieldError
  hint?: string
}

export const TextField = forwardRef<HTMLInputElement, BaseProps & InputHTMLAttributes<HTMLInputElement>>(
  ({ label, error, hint, ...props }, ref) => {
    return (
      <label className="block">
        <span className="text-sm font-semibold text-slate-700">{label}</span>
        <input
          ref={ref}
          className="mt-1.5 w-full rounded-md border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-500"
          {...props}
        />
        {hint && !error && <span className="mt-1 block text-xs text-slate-500">{hint}</span>}
        {error && <span className="mt-1 block text-xs text-red-600">{error.message}</span>}
      </label>
    )
  }
)

TextField.displayName = 'TextField'

export const TextAreaField = forwardRef<HTMLTextAreaElement, BaseProps & TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ label, error, hint, ...props }, ref) => {
    return (
      <label className="block">
        <span className="text-sm font-semibold text-slate-700">{label}</span>
        <textarea
          ref={ref}
          className="mt-1.5 w-full rounded-md border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition placeholder:text-slate-400 focus:border-blue-600 focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-500"
          rows={3}
          {...props}
        />
        {hint && !error && <span className="mt-1 block text-xs text-slate-500">{hint}</span>}
        {error && <span className="mt-1 block text-xs text-red-600">{error.message}</span>}
      </label>
    )
  }
)

TextAreaField.displayName = 'TextAreaField'

export const SelectField = forwardRef<HTMLSelectElement, BaseProps & SelectHTMLAttributes<HTMLSelectElement>>(
  ({ label, error, hint, children, ...props }, ref) => {
    return (
      <label className="block">
        <span className="text-sm font-semibold text-slate-700">{label}</span>
        <select
          ref={ref}
          className="mt-1.5 w-full rounded-md border border-slate-300 bg-white px-3 py-2.5 text-sm text-slate-900 shadow-sm outline-none transition focus:border-blue-600 focus:ring-4 focus:ring-blue-100 disabled:cursor-not-allowed disabled:bg-slate-100 disabled:text-slate-500"
          {...props}
        >
          {children}
        </select>
        {hint && !error && <span className="mt-1 block text-xs text-slate-500">{hint}</span>}
        {error && <span className="mt-1 block text-xs text-red-600">{error.message}</span>}
      </label>
    )
  }
)

SelectField.displayName = 'SelectField'
