export default function StatCard({ label, value, hint }) {
  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-soft">
      <div className="text-sm font-medium text-slate-500">{label}</div>
      <div className="mt-2 text-3xl font-semibold text-slate-900">{value}</div>
      {hint ? <div className="mt-2 text-sm text-slate-500">{hint}</div> : null}
    </div>
  )
}
