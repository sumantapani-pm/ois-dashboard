import { useState, useEffect, useCallback } from 'react'
import AnomalyCard from '../components/anomaly-cards/AnomalyCard'
import InventoryChart from '../components/charts/InventoryChart'
import { getAnomalies } from '../lib/api'

const CLIENT_ID = 'fead7b5d-60d4-4083-ab74-86161391733e'

const STATUS_FILTERS = [
  'all', 'open', 'assigned',
  'in_progress', 'resolved', 'verified'
]

const chartData = [
  { sku: 'SKU-001', quantity_on_hand: 45, reorder_point: 50 },
  { sku: 'SKU-002', quantity_on_hand: 8,  reorder_point: 30 },
  { sku: 'SKU-003', quantity_on_hand: 0,  reorder_point: 20 },
  { sku: 'SKU-004', quantity_on_hand: 200,reorder_point: 25 },
]

export default function Dashboard() {
  const [anomalies, setAnomalies]     = useState([])
  const [filter, setFilter]           = useState('open')
  const [loading, setLoading]         = useState(true)
  const [lastRefresh, setLastRefresh] = useState(null)

  const fetchAnomalies = useCallback(async () => {
    setLoading(true)
    try {
      const res = await getAnomalies(
        CLIENT_ID,
        filter === 'all' ? undefined : filter
      )
      setAnomalies(res.data)
      setLastRefresh(new Date())
    } catch (err) {
      console.error('Fetch failed:', err)
    } finally {
      setLoading(false)
    }
  }, [filter])

  useEffect(() => {
    fetchAnomalies()
    const interval = setInterval(fetchAnomalies, 60000)
    return () => clearInterval(interval)
  }, [fetchAnomalies])

  const openCount     = anomalies.filter(
    a => a.status === 'open').length
  const criticalCount = anomalies.filter(
    a => a.severity === 'critical').length

  return (
    <div className="min-h-screen bg-slate-900 p-6">

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">
            OIS — Operational Intelligence
          </h1>
          <p className="text-sm text-slate-400">
            {lastRefresh
              ? `Last refresh: ${lastRefresh.toLocaleTimeString()}`
              : 'Loading...'}
          </p>
        </div>
        <button
          onClick={fetchAnomalies}
          className="bg-slate-800 border border-slate-600
                     text-slate-100 px-4 py-2 rounded-lg
                     text-sm hover:bg-slate-700 transition"
        >
          Refresh
        </button>
      </div>

      {/* KPI Bar */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: 'Open Anomalies',
            value: openCount,     color: 'text-red-400' },
          { label: 'Critical',
            value: criticalCount, color: 'text-red-300' },
          { label: 'Total Tracked',
            value: anomalies.length, color: 'text-slate-100' },
        ].map(kpi => (
          <div key={kpi.label}
               className="bg-slate-800 border border-slate-700
                          rounded-xl p-4 text-center">
            <p className={`text-3xl font-bold ${kpi.color}`}>
              {kpi.value}
            </p>
            <p className="text-xs text-slate-400 mt-1">
              {kpi.label}
            </p>
          </div>
        ))}
      </div>

      {/* Chart */}
      <div className="mb-6">
        <InventoryChart data={chartData} />
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 mb-4 flex-wrap">
        {STATUS_FILTERS.map(s => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1.5 rounded-lg text-xs
                        font-medium capitalize transition-colors
                        ${filter === s
                          ? 'bg-blue-600 text-white'
                          : 'bg-slate-800 text-slate-400'
                        }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Anomaly Cards */}
      {loading ? (
        <p className="text-slate-400 text-center py-12">
          Loading anomalies...
        </p>
      ) : anomalies.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-green-400 text-lg font-semibold">
            ✓ No anomalies in this state
          </p>
          <p className="text-slate-400 text-sm mt-1">
            Operational baseline holding
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2
                        lg:grid-cols-3 gap-4">
          {anomalies.map(a => (
            <AnomalyCard
              key={a.id}
              anomaly={a}
              clientId={CLIENT_ID}
              onUpdate={fetchAnomalies}
            />
          ))}
        </div>
      )}
    </div>
  )
}