import { useState } from 'react'
import { resumeApi } from '../services/api'

export default function UploadResumePage() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (!file) return

    setLoading(true)
    setMessage('')
    setError('')
    try {
      const { data } = await resumeApi.upload(file)
      setMessage(`Uploaded ${data.filename} successfully.`)
      setFile(null)
      event.target.reset()
    } catch (err) {
      setError(err?.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-soft">
      <h1 className="text-3xl font-semibold text-slate-900">Upload resume</h1>
      <p className="mt-2 text-sm text-slate-500">Upload a PDF resume. The backend extracts text and stores it in PostgreSQL.</p>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block w-full rounded-2xl border border-slate-200 bg-white text-sm text-slate-600 file:mr-4 file:rounded-xl file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white"
          required
        />
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        {message ? <p className="text-sm text-emerald-600">{message}</p> : null}
        <button
          disabled={loading}
          className="rounded-2xl bg-slate-900 px-4 py-3 text-sm font-medium text-white transition hover:bg-slate-800 disabled:opacity-60"
        >
          {loading ? 'Uploading...' : 'Upload PDF'}
        </button>
      </form>
    </div>
  )
}
