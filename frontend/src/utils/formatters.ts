export function formatCurrency(value: string | number) {
  return Number(value).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

export function formatDate(value: string) {
  return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR')
}

export function formatDateTime(value: string) {
  return new Date(value).toLocaleString('pt-BR')
}

export function formatPaymentMethod(value: string) {
  const labels: Record<string, string> = {
    CARTAO_CREDITO: 'CARTÃO DE CRÉDITO',
    CARTAO_DEBITO: 'CARTÃO DE DÉBITO'
  }

  return labels[value] ?? value.split('_').join(' ')
}

export function onlyDigits(value: string) {
  return value.replace(/\D/g, '')
}
