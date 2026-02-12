import { Zap, Clock, FileText } from 'lucide-react'
import { Card, CardContent } from "@/components/ui/card"

interface LiveStatsProps {
    stats: {
        runtime_sec: number
        tokens_generated: number
        speed_tokens_per_sec: number
    } | null
}

export function LiveStats({ stats }: LiveStatsProps) {
    if (!stats) return null

    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6 animate-in fade-in slide-in-from-top-4 duration-500">
            <Card className="bg-primary/5 border-primary/20">
                <CardContent className="p-4 flex items-center space-x-4">
                    <div className="p-2 bg-primary/10 rounded-full">
                        <Zap className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">Speed</p>
                        <p className="text-xl font-bold">{stats.speed_tokens_per_sec} <span className="text-xs font-normal text-muted-foreground">tokens/s</span></p>
                    </div>
                </CardContent>
            </Card>

            <Card className="bg-blue-500/5 border-blue-500/20">
                <CardContent className="p-4 flex items-center space-x-4">
                    <div className="p-2 bg-blue-500/10 rounded-full">
                        <Clock className="w-5 h-5 text-blue-500" />
                    </div>
                    <div>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">Time</p>
                        <p className="text-xl font-bold">{stats.runtime_sec}s</p>
                    </div>
                </CardContent>
            </Card>

            <Card className="bg-green-500/5 border-green-500/20">
                <CardContent className="p-4 flex items-center space-x-4">
                    <div className="p-2 bg-green-500/10 rounded-full">
                        <FileText className="w-5 h-5 text-green-500" />
                    </div>
                    <div>
                        <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">Generated</p>
                        <p className="text-xl font-bold">{stats.tokens_generated} <span className="text-xs font-normal text-muted-foreground">words</span></p>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
