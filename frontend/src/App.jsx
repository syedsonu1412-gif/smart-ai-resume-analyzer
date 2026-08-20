import { useState } from 'react'

import Login from './pages/Login'
import ResumeAnalyzer from './pages/ResumeAnalyzer'
import JobMatching from './pages/JobMatching'
import JobTracker from './pages/JobTracker'
import Dashboard from './pages/Dashboard'
import './App.css'

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [page, setPage] = useState('dashboard')

  // Login
  const handleLogin = () => {
    setLoggedIn(true)
    setPage('dashboard')
  }

  // Logout
  const handleLogout = async () => {
    try {
      // Delete latest resume
      const resumeResponse = await fetch(
        'http://127.0.0.1:8000/api/resume/latest',
        {
          method: 'DELETE',
        }
      )

      const resumeData = await resumeResponse.json()

      console.log(
        'Resume cleanup:',
        resumeData
      )

      // Delete all job applications
      const applicationResponse = await fetch(
        'http://127.0.0.1:8000/api/applications/',
        {
          method: 'DELETE',
        }
      )

      const applicationData =
        await applicationResponse.json()

      console.log(
        'Application cleanup:',
        applicationData
      )

      // Clear saved Job Match score
      localStorage.removeItem(
        'latestMatchScore'
      )

    } catch (error) {
      console.error(
        'Logout cleanup error:',
        error
      )
    }

    // Logout
    setLoggedIn(false)

    // Reset page
    setPage('dashboard')
  }

  // Show Login when logged out
  if (!loggedIn) {
    return (
      <Login onLogin={handleLogin} />
    )
  }

  // Common layout
  const commonLayout = (children) => (
    <div className="app">

      <button
        onClick={() =>
          setPage('dashboard')
        }
      >
        ← Back to Dashboard
      </button>

      {children}

    </div>
  )

  // Job Tracker
  if (page === 'tracker') {
    return commonLayout(
      <JobTracker />
    )
  }

  // Job Matching
  if (page === 'job') {
    return commonLayout(
      <JobMatching />
    )
  }

  // Resume Analyzer
  if (page === 'resume') {
    return commonLayout(
      <ResumeAnalyzer />
    )
  }

  // Dashboard
  return (
    <Dashboard
      onNavigate={(destination) =>
        setPage(destination)
      }
      onLogout={handleLogout}
    />
  )
}

export default App