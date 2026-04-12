import axios from 'axios'

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' }
})

export const getAnomalies = (clientId, status) =>
  API.get('/anomalies/', { params: { client_id: clientId, status } })

export const updateAnomalyStatus = (anomalyId, payload) =>
  API.patch(`/anomalies/${anomalyId}/status`, payload)

export const executeAction = (payload) =>
  API.post('/actions/execute', payload)

export const getActionHistory = (anomalyId) =>
  API.get(`/actions/${anomalyId}/history`)