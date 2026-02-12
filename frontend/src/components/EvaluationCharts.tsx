import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function EvaluationCharts({ timestamp }: { timestamp: number }) {
    const charts = [
        { title: "Runtime vs Quality", src: `http://127.0.0.1:8000/static/runtime_vs_quality.png?t=${timestamp}` },
        { title: "Runtime vs ROUGE", src: `http://127.0.0.1:8000/static/runtime_vs_rouge.png?t=${timestamp}` },
        { title: "Memory Usage", src: `http://127.0.0.1:8000/static/memory_usage.png?t=${timestamp}` },
    ]

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            {charts.map((chart, index) => (
                <Card key={index} className="overflow-hidden">
                    <CardHeader className="p-4">
                        <CardTitle className="text-sm font-medium">{chart.title}</CardTitle>
                    </CardHeader>
                    <CardContent className="p-0">
                        <img
                            src={chart.src}
                            alt={chart.title}
                            className="w-full h-48 object-cover hover:scale-105 transition-transform duration-300"
                            onError={(e) => {
                                e.currentTarget.src = "https://placehold.co/400x300?text=Chart+Not+Found" // Fallback
                            }}
                        />
                    </CardContent>
                </Card>
            ))}
        </div>
    )
}
