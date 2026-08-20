import { useState } from 'react'

function ResumeAnalyzer() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleUpload = async (e) => {
    e.preventDefault()

    if (!file) {
      setError('Please select a PDF resume.')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/resume/upload',
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Resume upload failed')
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="resume-analyzer">
      <h1>Resume Analyzer</h1>

      <p>Upload your PDF resume to analyze it.</p>

      <form onSubmit={handleUpload}>
        <input
          type="file"
          accept=".pdf,application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Resume'}
        </button>
      </form>

      {error && <p>{error}</p>}

      {result && (
        <div>
          <h2>Analysis Result</h2>

          <h3>Resume Score</h3>
          <strong>{result.resume_score}/100</strong>

          <h3>Detected Domains</h3>
          <ul>
            {result.detected_domains?.map((domain) => (
              <li key={domain}>{domain}</li>
            ))}
          </ul>

          <h3>Skills</h3>
          <ul>
            {result.skills?.map((skill) => (
              <li key={skill}>{skill}</li>
            ))}
          </ul>

          <h3>Education</h3>
          <ul>
            {result.education?.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>

          <h3>Experience</h3>
          <ul>
            {result.experience?.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>

          <h3>Recommendations</h3>
          <ul>
            {result.recommendations?.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default ResumeAnalyzer