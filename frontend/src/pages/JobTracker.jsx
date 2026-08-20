import { useEffect, useState } from 'react'

function JobTracker() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let ignore = false

    const fetchApplications = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/api/applications/'
        )

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || 'Failed to load applications')
        }

        if (!ignore) {
          setApplications(
            Array.isArray(data) ? data : data.applications || []
          )
        }
      } catch (err) {
        if (!ignore) {
          setError(err.message)
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    fetchApplications()

    return () => {
      ignore = true
    }
  }, [])

  if (loading) {
    return <h2>Loading applications...</h2>
  }

  return (
    <div className="job-tracker">
      <h1>📋 Job Tracker</h1>

      {error && <p>{error}</p>}

      {!error && applications.length === 0 && (
        <p>No applications found.</p>
      )}

      {applications.length > 0 && (
        <div>
          {applications.map((application) => (
            <div className="application-card" key={application.id}>
              <h2>{application.company}</h2>

              <p>
                <strong>Job:</strong> {application.job_title}
              </p>

              <p>
                <strong>Location:</strong> {application.location}
              </p>

              <p>
                <strong>Status:</strong> {application.status}
              </p>

              <p>
                <strong>Applied Date:</strong>{' '}
                {application.applied_date}
              </p>

              {application.job_url && (
                <a
                  href={application.job_url}
                  target="_blank"
                  rel="noreferrer"
                >
                  View Job
                </a>
              )}

              {application.notes && (
                <p>
                  <strong>Notes:</strong> {application.notes}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default JobTracker
