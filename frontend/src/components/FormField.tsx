import { forwardRef, InputHTMLAttributes, SelectHTMLAttributes, TextareaHTMLAttributes } from 'react'
import { FieldError } from 'react-hook-form'

type BaseProps = {
  label: string
  error?: FieldError
}

export const TextField = forwardRef<HTMLInputElement, BaseProps & InputHTMLAttributes<HTMLInputElement>>(
  ({ label, error, ...props }, ref) => {
    return (
      <label className="block">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <input
          ref={ref}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          {...props}
        />
        {error && <span className="mt-1 block text-xs text-red-600">{error.message}</span>}
      </label>
    )
  }
)

TextField.displayName = 'TextField'

export const TextAreaField = forwardRef<HTMLTextAreaElement, BaseProps & TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ label, error, ...props }, ref) => {
    return (
      <label className="block">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <textarea
          ref={ref}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          rows={3}
          {...props}
        />
        {error && <span className="mt-1 block text-xs text-red-600">{error.message}</span>}
      </label>
    )
  }
)

TextAreaField.displayName = 'TextAreaField'

export const SelectField = forwardRef<HTMLSelectElement, BaseProps & SelectHTMLAttributes<HTMLSelectElement>>(
  ({ label, error, children, ...props }, ref) => {
    return (
      <label className="block">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <select
          ref={ref}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          {...props}
        >
          {children}
        </select>
        {error && <span className="mt-1 block text-xs text-red-600">{error.message}</span>}
      </label>
    )
  }
)

SelectField.displayName = 'SelectField'
