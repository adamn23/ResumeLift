import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { authApi } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem('resumelift_user')
    return raw ? JSON.parse(raw) : null
  })
  const [token, setToken] = useState(() => localStorage.getItem('resumelift_token'))

  useEffect(() => {
    if (token) localStorage.setItem('resumelift_token', token)
    else localStorage.removeItem('resumelift_token')
  }, [token])

  useEffect(() => {
    if (user) localStorage.setItem('resumelift_user', JSON.stringify(user))
    else localStorage.removeItem('resumelift_user')
  }, [user])

  const login = async (payload) => {
    const { data } = await authApi.login(payload)
    setToken(data.access_token)
    setUser(data.user)
    return data
  }

  const register = async (payload) => {
    const { data } = await authApi.register(payload)
    setToken(data.access_token)
    setUser(data.user)
    return data
  }

  const logout = () => {
    setToken(null)
    setUser(null)
  }

  const value = useMemo(() => ({ user, token, login, register, logout, isAuthenticated: Boolean(token) }), [user, token])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used inside AuthProvider')
  return context
}
