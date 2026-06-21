import axios from 'axios'

function getApiBaseUrl() {
  const configuredUrl = import.meta.env.VITE_API_URL

  if (!configuredUrl && typeof window !== 'undefined') {
    return `${window.location.protocol}//${window.location.hostname}:8000`
  }

  if (configuredUrl && typeof window !== 'undefined') {
    const currentHost = window.location.hostname
    const localHosts = ['localhost', '127.0.0.1', '0.0.0.0']

    try {
      const url = new URL(configuredUrl)
      if (!localHosts.includes(currentHost) && localHosts.includes(url.hostname)) {
        url.hostname = currentHost
        return url.toString().replace(/\/$/, '')
      }
    } catch {
      return configuredUrl
    }
  }

  return configuredUrl ?? 'http://localhost:8000'
}

export const api = axios.create({
  baseURL: getApiBaseUrl()
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('easyhotel.token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export function getApiError(error: unknown) {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((item) => item.msg).join(', ')
    return error.message
  }
  return 'Não foi possível concluir a operação.'
}
