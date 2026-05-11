import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { dashboardApi } from '../services/api'
import StatCard from '../components/StatCard'
import SectionTitle from '../components/SectionTitle'

function formatDate(value) {
  return new Date(value).toLocaleString()
}

export default function DashboardPage() {
  const [data, setData] = useState({ resumes: [], recent_matches: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError('')
      try {
        const response = await dashboardApi.get()
        setData(response.data)
      } catch (err) {
        setError(err?.response?.data?.detail || 'Could not load dashboard')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  const averageScore =
    data.recent_matches.length > 0
      ? Math.round(
          data.recent_matches.reduce((sum, item) => sum + Number(item.match_score || 0), 0) / data.recent_matches.length
        )
      : 0

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
        <h1 className="text-3xl font-semibold text-slate-900">Dashboard</h1>
        <p className="mt-2 max-w-2xl text-sm text-slate-500">
          Track uploaded resumes, saved job descriptions, and recent match analyses in one place.
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <Link to="/upload" className="rounded-2xl bg-slate-900 px-4 py-2 text-sm font-medium text-white">
            Upload resume
          </Link>
          <Link to="/matches" className="rounded-2xl border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700">
            Run matching
          </Link>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <StatCard label="Uploaded resumes" value={data.resumes.length} hint="PDF resumes stored in PostgreSQL" />
        <StatCard label="Recent analyses" value={data.recent_matches.length} hint="Latest match runs" />
        <StatCard label="Average match score" value={`${averageScore}%`} hint="Simple portfolio metric" />
      </div>

      {error ? <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div> : null}
      {loading ? <div className="text-sm text-slate-500">Loading dashboard...</div> : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
          <SectionTitle title="Uploaded resumes" subtitle="Most recent first" />
          <div className="space-y-3">
            {data.resumes.map((resume) => (
              <div key={resume.id} className="rounded-2xl border border-slate-200 p-4">
                <div className="font-medium text-slate-900">{resume.filename}</div>
                <div className="mt-1 text-sm text-slate-500">{resume.preview}</div>
                <div className="mt-2 text-xs text-slate-400">{formatDate(resume.created_at)}</div>
              </div>
            ))}
            {!data.resumes.length ? <p className="text-sm text-slate-500">No resumes uploaded yet.</p> : null}
          </div>
        </section>

        <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
          <SectionTitle title="Recent analyses" subtitle="Latest match runs" />
          <div className="space-y-3">
            {data.recent_matches.map((match) => (
              <div key={match.id} className="rounded-2xl border border-slate-200 p-4">
                <div className="flex items-center justify-between gap-3">
                  <div className="font-medium text-slate-900">Match #{match.id}</div>
                  <div className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">
                    {Math.round(match.match_score)}%
                  </div>
                </div>
                <div className="mt-2 text-sm text-slate-500">
                  Matched: {match.matched_keywords?.join(', ') || 'None'}
                </div>
                <div className="mt-1 text-sm text-slate-500">
                  Missing: {match.missing_keywords?.join(', ') || 'None'}
                </div>
              </div>
            ))}
            {!data.recent_matches.length ? <p className="text-sm text-slate-500">No analyses yet.</p> : null}
          </div>
        </section>
      </div>
    </div>
  )
}
