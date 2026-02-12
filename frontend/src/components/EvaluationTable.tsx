import { useEffect, useState } from 'react'
import axios from 'axios'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { Loader2 } from 'lucide-react'

// Define the interface for our evaluation data rows
interface EvaluationRow {
    model: string
    runtime_s: number
    tokens: number
    memory_MB: number
    ROUGE1: number
    ROUGE2: number
    ROUGEL: number
    BERTScore_F1: number
    summary: string
}

export function EvaluationTable() {
    const [data, setData] = useState<EvaluationRow[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/evaluation-results')
                setData(response.data)
            } catch (err) {
                setError('Failed to load evaluation results.')
                console.error(err)
            } finally {
                setIsLoading(false)
            }
        }

        fetchData()
    }, [])

    if (isLoading) {
        return <div className="flex justify-center p-4"><Loader2 className="animate-spin" /></div>
    }

    if (error) {
        return <div className="text-red-500 p-4">{error}</div>
    }

    if (data.length === 0) {
        return <div className="text-muted-foreground p-4">No evaluation results found. Run the evaluation pipeline backend script to generate data.</div>
    }

    return (
        <Card className="w-full mt-8">
            <CardHeader>
                <CardTitle>Evaluation Benchmarks</CardTitle>
            </CardHeader>
            <CardContent>
                {/* Guide to Metrics */}
                <div className="bg-muted/30 border rounded-lg p-4 mb-6 text-sm">
                    <h4 className="font-semibold mb-2">Guide to Metrics:</h4>
                    <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-muted-foreground">
                        <li>⏱️ <span className="font-medium text-foreground">Runtime:</span> Time taken to summarize (Lower is faster ↓)</li>
                        <li>💾 <span className="font-medium text-foreground">Memory:</span> RAM usage during generation (Lower is lighter ↓)</li>
                        <li>📝 <span className="font-medium text-foreground">ROUGE:</span> Word overlap accuracy (Higher is better ↑)</li>
                        <li>🧠 <span className="font-medium text-foreground">BERTScore:</span> Semantic meaning accuracy (Higher is better ↑)</li>
                    </ul>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-sm text-left">
                        <thead className="text-xs uppercase bg-muted/50 text-muted-foreground">
                            <tr>
                                <th className="px-4 py-3 rounded-tl-lg">Model</th>
                                <th className="px-4 py-3">Runtime (s) <span className="text-xs">↓</span></th>
                                <th className="px-4 py-3">Tokens</th>
                                <th className="px-4 py-3">Memory (MB) <span className="text-xs">↓</span></th>
                                <th className="px-4 py-3">ROUGE-1 <span className="text-xs">↑</span></th>
                                <th className="px-4 py-3">ROUGE-L <span className="text-xs">↑</span></th>
                                <th className="px-4 py-3 rounded-tr-lg">BERTScore <span className="text-xs">↑</span></th>
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((row, index) => (
                                <tr key={index} className="border-b last:border-0 hover:bg-muted/50 transition-colors">
                                    <td className="px-4 py-3 font-medium">{row.model}</td>
                                    <td className="px-4 py-3">{row.runtime_s.toFixed(2)}</td>
                                    <td className="px-4 py-3">{row.tokens}</td>
                                    <td className="px-4 py-3">{row.memory_MB.toFixed(1)}</td>
                                    <td className="px-4 py-3 text-green-600 font-semibold">{(row.ROUGE1 * 100).toFixed(1)}%</td>
                                    <td className="px-4 py-3">{(row.ROUGEL * 100).toFixed(1)}%</td>
                                    <td className="px-4 py-3">{(row.BERTScore_F1 * 100).toFixed(1)}%</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </CardContent>
        </Card>
    )
}
