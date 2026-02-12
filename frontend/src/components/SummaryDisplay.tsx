import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import ReactMarkdown from 'react-markdown'
import { Loader2 } from 'lucide-react'

interface SummaryDisplayProps {
    summary: string
    isLoading: boolean
}

export function SummaryDisplay({ summary, isLoading }: SummaryDisplayProps) {
    if (isLoading) {
        return (
            <Card className="w-full h-full min-h-[300px] flex items-center justify-center">
                <div className="flex flex-col items-center space-y-4">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                    <p className="text-muted-foreground">Generating summary...</p>
                </div>
            </Card>
        )
    }

    if (!summary) {
        return (
            <Card className="w-full h-full min-h-[300px] flex items-center justify-center bg-muted/20">
                <p className="text-muted-foreground">Upload a PDF to see the summary here</p>
            </Card>
        )
    }

    return (
        <Card className="w-full h-full shadow-lg">
            <CardHeader>
                <CardTitle>Document Summary</CardTitle>
            </CardHeader>
            <CardContent className="prose prose-sm dark:prose-invert max-w-none">
                <ReactMarkdown>{summary}</ReactMarkdown>
            </CardContent>
        </Card>
    )
}
