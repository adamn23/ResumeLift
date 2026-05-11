import { useEffect, useMemo, useState } from 'react'
import { jobApi, matchApi, resumeApi } from '../services/api'
import SectionTitle from '../components/SectionTitle'

function emptyForm() {
  return { resume_id: '', job_description_id: '' }
}

export default function MatchResultsPage() {
  const [resumes, setResumes] = useState([])
  const [jobs, setJobs] = useState([])
  const [matches, setMatches] = useState([])
  const [form, setForm] = useState(emptyForm())
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [pageLoading, setPageLoading] = useState(true)
  const [error, setError] = useState('')

  const load = async () => {
    setPageLoading(true)
    setError('')
    try {
      const [resumesRes, jobsRes, matchesRes] = await Promise.all([
        resumeApi.list(),
        jobApi.list(),
        matchApi.list(),
      ])
      setResumes(resumesRes.data)
      setJobs(jobsRes.data)
      setMatches(matchesRes.data)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not load matching data')
    } finally {
      setPageLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  const selectedResume = useMemo(() => resumes.find((item) => String(item.id) === String(form.resume_id)), [resumes, form.resume_id])
  const selectedJob = useMemo(() => jobs.find((item) => String(item.id) === String(form.job_description_id)), [jobs, form.job_description_id])

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!form.resume_id || !form.job_description_id) return

    setLoading(true)
    setError('')
    try {
      const { data } = await matchApi.analyze({
        resume_id: Number(form.resume_id),
        job_description_id: Number(form.job_description_id),
      })
      setAnalysis(data)
      await load()
    } catch (err) {
      setError(err?.response?.data?.detail || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  const handleFeedback = async () => {
    if (!form.resume_id || !form.job_description_id) return
    setLoading(true)
    setError('')
    try {
      const { data } = await matchApi.feedback({
        resume_id: Number(form.resume_id),
        job_description_id: Number(form.job_description_id),
      })
      setAnalysis((prev) => (prev ? { ...prev, feedback: data.feedback } : data))
    } catch (err) {
      setError(err?.response?.data?.detail || 'Feedback generation failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
        <h1 className="text-3xl font-semibold text-slate-900">Match results</h1>
        <p className="mt-2 text-sm text-slate-500">Choose a resume and job description to generate an embeddings-based match score.</p>

        <form onSubmit={handleSubmit} className="mt-6 grid gap-4 md:grid-cols-3">
          <select
            value={form.resume_id}
            onChange={(e) => setForm((prev) => ({ ...prev, resume_id: e.target.value }))}
            className="rounded-2xl border-slate-200 px-4 py-3"
            required
          >
            <option value="">Select resume</option>
            {resumes.map((resume) => (
              <option key={resume.id} value={resume.id}>
                {resume.filename}
              </option>
            ))}
          </select>

          <select
            value={form.job_description_id}
            onChange={(e) => setForm((prev) => ({ ...prev, job_description_id: e.target.value }))}
            className="rounded-2xl border-slate-200 px-4 py-3"
            required
          >
            <option value="">Select job description</option>
            {jobs.map((job) => (
              <option key={job.id} value={job.id}>
                {job.title}
              </option>
            ))}
          </select>

          <div className="flex gap-3">
            <button
              disabled={loading}
              className="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:opacity-60"
            >
              {loading ? 'Running...' : 'Analyze match'}
            </button>
            <button
              type="button"
              onClick={handleFeedback}
              disabled={loading}
              className="rounded-2xl border border-slate-200 px-4 py-3 text-sm font-medium text-slate-700 disabled:opacity-60"
            >
              AI feedback
            </button>
          </div>
        </form>

        {selectedResume ? <p className="mt-4 text-sm text-slate-500">Resume: {selectedResume.filename}</p> : null}
        {selectedJob ? <p className="mt-1 text-sm text-slate-500">Job: {selectedJob.title}</p> : null}
        {error ? <p className="mt-4 text-sm text-red-600">{error}</p> : null}
      </div>

      {analysis ? (
        <div className="grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
            <SectionTitle title="Current analysis" subtitle="Most recent result" />
            <div className="text-5xl font-semibold text-slate-900">{Math.round(analysis.match_score)}%</div>
            <div className="mt-5 space-y-4 text-sm">
              <div>
                <div className="font-medium text-slate-700">Matched keywords</div>
                <p className="mt-1 text-slate-500">{analysis.matched_keywords?.join(', ') || 'None'}</p>
              </div>
              <div>
                <div className="font-medium text-slate-700">Missing keywords</div>
                <p className="mt-1 text-slate-500">{analysis.missing_keywords?.join(', ') || 'None'}</p>
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
            <SectionTitle title="AI feedback" subtitle="Practical resume improvements" />
            <ul className="space-y-3">
              {(analysis.feedback || []).map((item, index) => (
                <li key={index} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">
                  {item}
                </li>
              ))}
            </ul>
          </section>
        </div>
      ) : null}

      <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
        <SectionTitle title="Recent saved results" subtitle="Stored in PostgreSQL" />
        <div className="space-y-3">
          {pageLoading ? <p className="text-sm text-slate-500">Loading results...</p> : null}
          {matches.map((match) => (
            <div key={match.id} className="rounded-2xl border border-slate-200 p-4">
              <div className="flex items-center justify-between gap-3">
                <div className="text-sm font-medium text-slate-900">Analysis #{match.id}</div>
                <div className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">
                  {Math.round(match.match_score)}%
                </div>
              </div>
              <p className="mt-2 text-sm text-slate-500">Matched: {match.matched_keywords?.join(', ') || 'None'}</p>
              <p className="mt-1 text-sm text-slate-500">Missing: {match.missing_keywords?.join(', ') || 'None'}</p>
            </div>
          ))}
          {!pageLoading && !matches.length ? <p className="text-sm text-slate-500">No match results yet.</p> : null}
        </div>
      </section>
    </div>
  )
}
