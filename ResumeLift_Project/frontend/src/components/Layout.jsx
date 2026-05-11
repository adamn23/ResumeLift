import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { Brain, LogOut, Upload, LayoutDashboard, Sparkles } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const linkClass = ({ isActive }) =>
  `flex items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition ${
    isActive ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'
  }`

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-slate-100">
      <header className="border-b border-slate-200/80 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <Link to="/dashboard" className="flex items-center gap-2 font-semibold text-slate-900">
            <div className="rounded-2xl bg-slate-900 p-2 text-white">
              <Brain className="h-5 w-5" />
            </div>
            <span>ResumeLift</span>
          </Link>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-500 sm:block">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="inline-flex items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[220px_1fr] lg:px-8">
        <aside className="rounded-3xl border border-slate-200 bg-white p-4 shadow-soft">
          <nav className="space-y-2">
            <NavLink to="/dashboard" className={linkClass}>
              <LayoutDashboard className="h-4 w-4" />
              Dashboard
            </NavLink>
            <NavLink to="/upload" className={linkClass}>
              <Upload className="h-4 w-4" />
              Upload Resume
            </NavLink>
            <NavLink to="/matches" className={linkClass}>
              <Sparkles className="h-4 w-4" />
              Match Results
            </NavLink>
          </nav>
        </aside>

        <main className="min-w-0">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
