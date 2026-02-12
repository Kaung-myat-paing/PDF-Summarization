import React, { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { UploadCloud, FileText, X } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from './ui/button'

interface FileUploadProps {
    onFileSelect: (file: File) => void
    onClear: () => void
    selectedFile: File | null
    disabled?: boolean
}

export function FileUpload({ onFileSelect, onClear, selectedFile, disabled }: FileUploadProps) {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            onFileSelect(acceptedFiles[0])
        }
    }, [onFileSelect])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/pdf': ['.pdf']
        },
        maxFiles: 1,
        disabled
    })

    if (selectedFile) {
        return (
            <div className="flex items-center justify-between p-4 border rounded-lg bg-secondary/20">
                <div className="flex items-center space-x-3">
                    <div className="p-2 bg-primary/10 rounded-full">
                        <FileText className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <p className="text-sm font-medium">{selectedFile.name}</p>
                        <p className="text-xs text-muted-foreground">
                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                    </div>
                </div>
                <Button variant="ghost" size="icon" onClick={onClear} disabled={disabled}>
                    <X className="w-4 h-4" />
                </Button>
            </div>
        )
    }

    return (
        <div
            {...getRootProps()}
            className={cn(
                "flex flex-col items-center justify-center p-10 border-2 border-dashed rounded-lg transition-colors cursor-pointer",
                isDragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-secondary/50",
                disabled && "opacity-50 cursor-not-allowed"
            )}
        >
            <input {...getInputProps()} />
            <div className="p-4 bg-secondary rounded-full mb-4">
                <UploadCloud className="w-8 h-8 text-muted-foreground" />
            </div>
            <p className="mb-2 text-sm font-medium text-foreground">
                Click or drag PDF file to upload
            </p>
            <p className="text-xs text-muted-foreground">
                PDF (up to 10MB)
            </p>
        </div>
    )
}
