import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (event) => setForm((prev) => ({ ...prev, [event.target.name]: event.target.value }))

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      await register(form)
      navigate('/dashboard')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-soft">
        <h1 className="text-3xl font-semibold text-slate-900">Create account</h1>
        <p className="mt-2 text-sm text-slate-500">Build your resume analyzer portfolio app.</p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <input
            name="email"
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange}
            className="w-full rounded-2xl border-slate-200 px-4 py-3"
            required
          />
          <input
            name="password"
            type="password"
            placeholder="Password (8+ characters)"
            value={form.password}
            onChange={handleChange}
            className="w-full rounded-2xl border-slate-200 px-4 py-3"
            required
          />
          {error ? <p className="text-sm text-red-600">{error}</p> : null}
          <button
            disabled={loading}
            className="w-full rounded-2xl bg-slate-900 px-4 py-3 font-medium text-white transition hover:bg-slate-800 disabled:opacity-60"
          >
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>

        <p className="mt-6 text-sm text-slate-500">
          Already have an account?{' '}
          <Link to="/login" className="font-medium text-slate-900 underline">
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
