import { useState } from 'react'

function JobMatching() {
  const [resumeText, setResumeText] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleMatch = async (e) => {
    e.preventDefault()

    if (!resumeText.trim() || !jobDescription.trim()) {
      setError('Please provide both resume text and job description.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/job/match',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            resume_text: resumeText,
            job_description: jobDescription,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Job matching failed')
      }

      setResult(data)
      localStorage.setItem('latestMatchScore', data.match_score)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="job-matching">
      <h1>🎯 Job Matching</h1>

      <p>
        Compare your resume with a job description.
      </p>

      <form onSubmit={handleMatch}>
        <label>Resume Text</label>

        <textarea
          rows="10"
          placeholder="Paste your resume text here..."
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
        />

        <label>Job Description</label>

        <textarea
          rows="10"
          placeholder="Paste the job description here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Matching...' : 'Match Resume'}
        </button>
      </form>

      {error && <p>{error}</p>}

      {result && (
        <div className="match-result">
          <h2>Match Result</h2>

          <h3>Match Score</h3>
          <strong>{result.match_score}%</strong>

          <h3>Matching Skills</h3>
          <ul>
            {result.matching_skills?.map((skill) => (
              <li key={skill}>✓ {skill}</li>
            ))}
          </ul>

          <h3>Missing Skills</h3>
          <ul>
            {result.missing_skills?.map((skill) => (
              <li key={skill}>✗ {skill}</li>
            ))}
          </ul>

          <h3>Resume Skills</h3>
          <ul>
            {result.resume_skills?.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>

          <h3>Job Required Skills</h3>
          <ul>
            {result.job_required_skills?.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default JobMatching