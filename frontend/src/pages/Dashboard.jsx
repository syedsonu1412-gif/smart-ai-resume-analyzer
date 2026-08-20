import { useEffect, useState } from 'react'

function Dashboard({ onNavigate, onLogout }) {
  const [resume, setResume] = useState(null)
  const [matchScore] = useState(
  localStorage.getItem('latestMatchScore')
)
const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
  const loadDashboardData = async () => {
    try {
      const resumeResponse = await fetch(
        'http://127.0.0.1:8000/api/resume/latest'
      )

      if (resumeResponse.ok) {
        const resumeData = await resumeResponse.json()
        setResume(resumeData)
      }

      const applicationResponse = await fetch(
        'http://127.0.0.1:8000/api/applications/'
      )

      if (applicationResponse.ok) {
        const applicationData = await applicationResponse.json()

        setApplications(
          Array.isArray(applicationData)
            ? applicationData
            : []
        )
      }
    } catch (error) {
      console.error(
        'Dashboard loading error:',
        error
      )
    } finally {
      setLoading(false)
    }
  }

  loadDashboardData()
}, [])

  return (
    <div className="dashboard-page">

      <header className="dashboard-header">
        <div>
          <h1>Smart AI Resume Analyzer</h1>
          <p>AI-powered Resume Analysis & Job Tracker</p>
        </div>

        <button onClick={onLogout}>
          Logout
        </button>
      </header>

      <main className="dashboard-content">

        <div className="welcome-card">
          <h2>Welcome 👋</h2>
          <p>
            Analyze your resume, match it with jobs,
            and track your applications in one place.
          </p>
        </div>

        <div className="stats">

          <div className="stat-card">
            <h3>📄 Resume</h3>
            <p>
              {resume?.filename || 'No resume uploaded'}
            </p>

            <strong>
              {loading
                ? 'Loading...'
                : resume
                  ? `${resume.resume_score}/100`
                  : 'N/A'}
            </strong>
          </div>

          <div className="stat-card">
            <h3>🎯 Job Match</h3>
            <p>Latest Match</p>
            <strong>
            {matchScore ? `${matchScore}%` : 'N/A'}
            </strong>
          </div>

          <div className="stat-card">
            <h3>📋 Applications</h3>
            <p>Total Applications</p>
            <strong>{applications.length}</strong>
          </div>

          <div className="stat-card">
            <h3>💼 Status</h3>
            <p>Current Status</p>
            <strong>
  {applications.length > 0
    ? applications[applications.length - 1].status
    : 'No Applications'}
</strong>
          </div>

        </div>

        {resume && (
          <div className="resume-summary">
            <h2>Latest Resume Analysis</h2>

            <p>
              <strong>Resume:</strong> {resume.filename}
            </p>

            <p>
              <strong>Score:</strong> {resume.resume_score}/100
            </p>

            <h3>Detected Domains</h3>

            <ul>
              {resume.detected_domains?.map((domain) => (
                <li key={domain}>{domain}</li>
              ))}
            </ul>

            <h3>Skills</h3>

            <ul>
              {resume.skills?.map((skill) => (
                <li key={skill}>{skill}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="dashboard-cards">

          <div className="dashboard-card">
            <h2>📄 Resume Analyzer</h2>

            <p>
              Upload your resume and get your AI-powered
              resume score, skills, domains and recommendations.
            </p>

            <button onClick={() => onNavigate('resume')}>
              Analyze Resume
            </button>
          </div>

          <div className="dashboard-card">
            <h2>🎯 Job Matching</h2>

            <p>
              Compare your resume against a job description
              and identify matching and missing skills.
            </p>

            <button onClick={() => onNavigate('job')}>
              Match Job
            </button>
          </div>

          <div className="dashboard-card">
            <h2>📋 Job Tracker</h2>

            <p>
              Track companies, job titles, locations,
              application dates and statuses.
            </p>

            <button onClick={() => onNavigate('tracker')}>
              View Applications
            </button>
          </div>

        </div>

      </main>
    </div>
  )
}

export default Dashboard