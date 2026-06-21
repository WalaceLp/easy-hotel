import { Modal } from './Modal'
import { Button } from './Button'

type ConfirmDialogProps = {
  open: boolean
  title: string
  message: string
  onCancel: () => void
  onConfirm: () => void
  loading?: boolean
}

export function ConfirmDialog({ open, title, message, onCancel, onConfirm, loading }: ConfirmDialogProps) {
  return (
    <Modal open={open} title={title} onClose={onCancel}>
      <p className="text-sm text-slate-600">{message}</p>
      <div className="mt-5 flex justify-end gap-2">
        <Button type="button" variant="secondary" onClick={onCancel} disabled={loading}>
          Cancelar
        </Button>
        <Button type="button" variant="danger" onClick={onConfirm} disabled={loading}>
          Confirmar
        </Button>
      </div>
    </Modal>
  )
}
