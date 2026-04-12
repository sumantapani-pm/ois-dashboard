import ReactECharts from 'echarts-for-react'

export default function InventoryChart({ data }) {
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#1E293B',
      borderColor: '#334155',
      textStyle: { color: '#F1F5F9' }
    },
    grid: {
      left: '3%', right: '4%',
      bottom: '3%', containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.sku),
      axisLabel: { color: '#94A3B8', rotate: 30 },
      axisLine: { lineStyle: { color: '#334155' } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#94A3B8' },
      splitLine: { lineStyle: { color: '#334155' } }
    },
    series: [
      {
        name: 'Quantity on Hand',
        type: 'bar',
        data: data.map(d => ({
          value: d.quantity_on_hand,
          itemStyle: {
            color: d.quantity_on_hand === 0  ? '#EF4444' :
                   d.quantity_on_hand < 10   ? '#F59E0B' : '#10B981'
          }
        })),
        barMaxWidth: 40,
      },
      {
        name: 'Reorder Point',
        type: 'line',
        data: data.map(d => d.reorder_point),
        lineStyle: { color: '#3B82F6', type: 'dashed' },
        symbol: 'none'
      }
    ],
    legend: {
      textStyle: { color: '#94A3B8' },
      bottom: 0
    }
  }

  return (
    <div className="bg-slate-800 border border-slate-700
                    rounded-xl p-4">
      <h3 className="text-sm font-semibold text-slate-400
                     mb-3 uppercase">
        Inventory Health
      </h3>
      <ReactECharts option={option} style={{ height: '280px' }} />
    </div>
  )
}