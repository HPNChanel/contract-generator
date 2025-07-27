import React from 'react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'
import { Download, FileText, CheckCircle } from 'lucide-react'

interface ContractPreviewProps {
  contract?: {
    contract_id: number
    preview_html: string
    pdf_info: {
      filename: string
      download_url: string
      pdf_path: string
    }
  }
  isLoading?: boolean
  error?: string
}

export function ContractPreview({ contract, isLoading, error }: ContractPreviewProps) {
  const handleDownload = () => {
    if (contract?.pdf_info.download_url) {
      // Create a link to download the PDF
      const link = document.createElement('a')
      link.href = `http://localhost:8000${contract.pdf_info.download_url}`
      link.download = contract.pdf_info.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const handleViewHTML = () => {
    if (contract?.preview_html) {
      // Open HTML preview in a new window
      const newWindow = window.open('', '_blank')
      if (newWindow) {
        newWindow.document.write(contract.preview_html)
        newWindow.document.close()
      }
    }
  }

  if (isLoading) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Generating Contract...</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12">
            <div className="flex flex-col items-center space-y-4">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
              <p className="text-muted-foreground">Please wait while we generate your contract...</p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="text-destructive">Error</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="rounded-full bg-destructive/10 p-3">
                <FileText className="h-6 w-6 text-destructive" />
              </div>
              <div>
                <p className="font-medium text-destructive">Failed to generate contract</p>
                <p className="text-sm text-muted-foreground mt-1">{error}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (!contract) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle>Contract Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-12">
            <div className="flex flex-col items-center space-y-4 text-center">
              <div className="rounded-full bg-muted p-3">
                <FileText className="h-6 w-6 text-muted-foreground" />
              </div>
              <div>
                <p className="font-medium">No contract generated yet</p>
                <p className="text-sm text-muted-foreground">
                  Fill out the contract form and click "Generate Contract" to see the preview
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex items-center space-x-2">
          <CheckCircle className="h-5 w-5 text-green-600" />
          <CardTitle>Contract Generated Successfully!</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Success Message */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center space-x-2">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <p className="text-sm font-medium text-green-800">
              Contract #{contract.contract_id} has been generated and saved
            </p>
          </div>
        </div>

        {/* Contract Info */}
        <div className="space-y-3">
          <h3 className="font-semibold">Contract Details</h3>
          <div className="bg-muted/50 rounded-lg p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Contract ID:</span>
              <span className="font-medium">#{contract.contract_id}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">PDF Filename:</span>
              <span className="font-medium">{contract.pdf_info.filename}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Status:</span>
              <span className="font-medium text-green-600">Ready for Download</span>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-3">
          <h3 className="font-semibold">Actions</h3>
          <div className="flex flex-col space-y-2">
            <Button 
              onClick={handleDownload}
              className="w-full"
              size="lg"
            >
              <Download className="mr-2 h-4 w-4" />
              Download PDF Contract
            </Button>
            
            <Button 
              onClick={handleViewHTML}
              variant="outline"
              className="w-full"
            >
              <FileText className="mr-2 h-4 w-4" />
              Preview HTML Version
            </Button>
          </div>
        </div>

        {/* HTML Preview (truncated) */}
        <div className="space-y-3">
          <h3 className="font-semibold">HTML Preview</h3>
          <div className="border rounded-lg p-4 bg-muted/50 max-h-96 overflow-y-auto">
            <div 
              className="prose prose-sm max-w-none"
              dangerouslySetInnerHTML={{ 
                __html: contract.preview_html.substring(0, 1000) + 
                        (contract.preview_html.length > 1000 ? '...<br/><br/><em>Preview truncated. Click "Preview HTML Version" to see full content.</em>' : '')
              }}
            />
          </div>
        </div>

        {/* Additional Info */}
        <div className="text-xs text-muted-foreground border-t pt-4">
          <p>• The contract has been saved to the database and can be accessed later</p>
          <p>• PDF files are stored securely and can be downloaded multiple times</p>
          <p>• Use the API endpoints to manage contracts programmatically</p>
        </div>
      </CardContent>
    </Card>
  )
} 