import { useState } from 'react'
import { updateAnomalyStatus, executeAction } from '../../lib/api'

const SEVERITY_STYLES = {
  critical: 'border-red-500 bg-red-500/10',
  high:     'border-orange-500 bg-orange-500/10',
  medium:   'border-yellow-500 bg-yellow-500/10',
  low:      'border-blue-500 bg-blue-500/10',
}

const STATUS_LABELS = {
  open:        { label: 'Open',        color: 'bg-red-500' },
  assigned:    { label: 'Assigned',    color: 'bg-orange-500' },
  in_progress: { label: 'In Progress', color: 'bg-yellow-500' },
  resolved:    { label: 'Resolved',    color: 'bg-blue-500' },
  verified:    { label: 'Verified',    color: 'bg-green-500' },
}

const NEXT_ACTIONS = {
  open:        { label: 'Assign',  next_status: 'assigned' },
  assigned:    { label: 'Start',   next_status: 'in_progress' },
  in_progress: { label: 'Resolve', next_status: 'resolved' },
  resolved:    { label: 'Verify',  next_status: 'verified' },
  verified:    null,
}

export default function AnomalyCard({ anomaly, clientId, onUpdate }) {
  const [loading, setLoading] = useState(false)
  const [note, setNote] = useState('')
  const [postValue, setPostValue] = useState('')

  const statusStyle = STATUS_LABELS[anomaly.status]
  const severityStyle = SEVERITY_STYLES[anomaly.severity] || ''
  const nextAction = NEXT_ACTIONS[anomaly.status]

  async function handleAction() {
    if (!nextAction) return
    setLoading(true)
    try {
      await updateAnomalyStatus(anomaly.id, {
        status: nextAction.next_status,
        resolution_note: note || undefined,
        metric_post_action: postValue
          ? parseFloat(postValue) : undefined,
      })
      await executeAction({
        anomaly_id: anomaly.id,
        client_id: clientId,
        action_type: 'status_changed',
        action_detail: { new_status: nextAction.next_status }
      })
      onUpdate()
    } catch (err) {
      alert(`Error: ${err.response?.data?.detail || err.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={`rounded-xl border-l-4 p-4 mb-3 ${severityStyle}`}>
      <div className="flex items-center justify-between mb-2">
        <div>
          <span className="text-xs font-mono text-ois-muted uppercase">
            {anomaly.domain} · {anomaly.metric}
          </span>
          <h3 className="text-lg font-semibold text-ois-text">
            {anomaly.entity_label || anomaly.entity_id}
          </h3>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs px-2 py-1 rounded-full text-white
                           font-medium ${statusStyle.color}`}>
            {statusStyle.label}
          </span>
          <span className="text-xs text-ois-muted capitalize">
            {anomaly.severity}
          </span>
        </div>
      </div>

      <div className="flex gap-6 my-3">
        <div>
          <p className="text-xs text-ois-muted">Threshold</p>
          <p className="text-xl font-bold text-yellow-400">
            {anomaly.threshold_value}
          </p>
        </div>
        <div>
          <p className="text-xs text-ois-muted">Actual</p>
          <p className="text-xl font-bold text-red-400">
            {anomaly.actual_value}
          </p>
        </div>
        {anomaly.metric_post_action !== null && (
          <div>
            <p className="text-xs text-ois-muted">Post-Action</p>
            <p className="text-xl font-bold text-green-400">
              {anomaly.metric_post_action}
            </p>
          </div>
        )}
      </div>

      <p className="text-xs text-ois-muted mb-3">
        Detected: {new Date(anomaly.created_at).toLocaleString()}
      </p>

      {nextAction && (
        <div className="space-y-2">
          {anomaly.status === 'in_progress' && (
            <>
              <input
                type="text"
                placeholder="Resolution note (optional)"
                value={note}
                onChange={e => setNote(e.target.value)}
                className="w-full bg-slate-800 border border-slate-600
                           rounded px-3 py-1.5 text-sm text-slate-100"
              />
              <input
                type="number"
                placeholder="Post-action metric value"
                value={postValue}
                onChange={e => setPostValue(e.target.value)}
                className="w-full bg-slate-800 border border-slate-600
                           rounded px-3 py-1.5 text-sm text-slate-100"
              />
            </>
          )}
          <button
            onClick={handleAction}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white
                       font-medium py-2 rounded-lg text-sm transition-colors
                       disabled:opacity-50"
          >
            {loading ? 'Processing...' : `${nextAction.label} →`}
          </button>
        </div>
      )}

      {anomaly.status === 'verified' && (
        <div className="mt-2 text-sm text-green-400 font-medium">
          ✓ Metric recovery verified
        </div>
      )}
    </div>
  )
}