import { useState } from 'react'
import axios from 'axios'
import { FileUpload } from '@/components/FileUpload'
import { SummaryDisplay } from '@/components/SummaryDisplay'
import { EvaluationTable } from '@/components/EvaluationTable'
import { EvaluationCharts } from '@/components/EvaluationCharts'
import { LiveStats } from '@/components/LiveStats'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Loader2, ArrowRight } from 'lucide-react'

// API Base URL (adjust if backend port changes)
const API_URL = 'http://127.0.0.1:8000/api'

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [extractedText, setExtractedText] = useState<string>('')
  const [summary, setSummary] = useState<string>('')
  const [keywords, setKeywords] = useState<string[]>([])
  const [stats, setStats] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [status, setStatus] = useState<string>('')
  const [showBenchmarks, setShowBenchmarks] = useState(false)

  const [isEvaluating, setIsEvaluating] = useState(false)
  const [evalTimestamp, setEvalTimestamp] = useState(Date.now())

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    setExtractedText('')
    setSummary('')
    setKeywords([])
    setStats(null)
    setStatus('')
    setShowBenchmarks(false)
  }

  const handleClear = () => {
    setFile(null)
    setExtractedText('')
    setSummary('')
    setKeywords([])
    setStats(null)
    setStatus('')
    setShowBenchmarks(false)
  }

  const processFile = async () => {
    if (!file) return

    setIsLoading(true)
    setSummary('')
    setKeywords([])
    setStats(null)

    try {
      // Step 1: Extract Text
      setStatus('Extracting text from PDF...')
      const formData = new FormData()
      formData.append('file', file)

      const extractResponse = await axios.post(`${API_URL}/extract-text`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      const text = extractResponse.data.text
      setExtractedText(text)

      // Step 2: Summarize
      setStatus('Generating summary with Ollama...')
      const summarizeResponse = await axios.post(`${API_URL}/summarize`, {
        text: text,
        model: 'llama3.2:1b'
      })

      const data = summarizeResponse.data
      setSummary(data.summary)
      setKeywords(data.keywords || [])
      setStats({
        runtime_sec: data.runtime_sec,
        tokens_generated: data.tokens_generated,
        speed_tokens_per_sec: data.speed_tokens_per_sec
      })
      setStatus('Done!')
    } catch (error: any) {
      console.error('Error processing file:', error)
      setStatus(`Error: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRunEvaluation = async () => {
    if (showBenchmarks) {
      setShowBenchmarks(false)
      return
    }

    setIsEvaluating(true)
    try {
      await axios.post(`${API_URL}/evaluate`, {
        text: extractedText
      })
      setEvalTimestamp(Date.now()) // Force image reload
      setShowBenchmarks(true)
    } catch (error) {
      console.error("Evaluation failed:", error)
      alert("Failed to run benchmarks. Check console for details.")
    } finally {
      setIsEvaluating(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-8 font-sans flex flex-col items-center w-full">
      <div className="w-full max-w-5xl mx-auto space-y-8">

        {/* Header */}
        <div className="w-full max-w-5xl text-center space-y-4">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600">
            PDF Summarizer
          </h1>
          <p className="text-lg text-muted-foreground">
            Private, local document summarization powered by Ollama.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">

          {/* Left Column: Input */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Upload Document</CardTitle>
                <CardDescription>
                  Select a PDF file to analyze. Max 10MB.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <FileUpload
                  selectedFile={file}
                  onFileSelect={handleFileSelect}
                  onClear={handleClear}
                  disabled={isLoading}
                />

                <Button
                  className=""
                  size="lg"
                  onClick={processFile}
                  disabled={!file || isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {status}
                    </>
                  ) : (
                    <>
                      Summarize PDF <ArrowRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </Button>

                {status && !isLoading && (
                  <p className="text-sm text-center text-muted-foreground">{status}</p>
                )}
              </CardContent>
            </Card>

            {/* Optional: Extracted Text Debug View */}
            {extractedText && (
              <Card className="max-h-[300px] overflow-hidden">
                <CardHeader>
                  <CardTitle className="text-base">Extracted Text Preview</CardTitle>
                </CardHeader>
                <CardContent className="overflow-y-auto max-h-[200px] text-xs font-mono text-muted-foreground bg-muted p-4 rounded-md mx-6 mb-6">
                  {extractedText.slice(0, 500)}...
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column: Output */}
          <div className="h-full flex flex-col space-y-6">
            <LiveStats stats={stats} />

            <div className="flex-grow">
              <SummaryDisplay summary={summary} isLoading={isLoading && !summary} />
            </div>

            {/* Keywords / Topics */}
            {keywords.length > 0 && (
              <div className="flex flex-wrap gap-2 animate-in fade-in zoom-in duration-500 pt-4 pb-2">
                {keywords.map((keyword, i) => (
                  <span key={i} className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm font-medium">
                    #{keyword}
                  </span>
                ))}
              </div>
            )}
          </div>

        </div>


        {/* Evaluation Results Section - Only show when summary is present */}
        {summary && (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700 pt-8 border-t">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">Model Performance</h3>
                <p className="text-sm text-muted-foreground">Real-time stats from this run.</p>
              </div>
              <Button variant="outline" onClick={handleRunEvaluation} disabled={isEvaluating}>
                {isEvaluating ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Running Benchmarks...
                  </>
                ) : (
                  showBenchmarks ? "Hide Historical Benchmarks" : "View Historical Benchmarks"
                )}
              </Button>
            </div>

            {showBenchmarks && (
              <div className="animate-in fade-in slide-in-from-top-2 duration-500 space-y-8">
                <div className="flex items-center space-x-2">
                  <span className="h-px flex-1 bg-border"></span>
                  <span className="text-muted-foreground text-sm font-medium uppercase tracking-wider">Evaluation & Metrics (Reference Set)</span>
                  <span className="h-px flex-1 bg-border"></span>
                </div>

                <EvaluationTable />
                <EvaluationCharts timestamp={evalTimestamp} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}


export default App
