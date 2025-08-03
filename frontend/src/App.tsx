import React, { useState, useEffect } from 'react'
import { Toaster, toast } from 'react-hot-toast'
import { ContractForm } from './components/ContractForm'
import { ContractPreview } from './components/ContractPreview'
import { contractApi } from './services/api'
import type { ContractData, ContractResponse } from './services/api'

function App() {
  const [isLoading, setIsLoading] = useState(false)
  const [contract, setContract] = useState<ContractResponse | undefined>(undefined)
  const [error, setError] = useState<string>('')
  const [recentContracts, setRecentContracts] = useState<number[]>([])
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking')

  // Load recent contracts from localStorage and test backend connection
  useEffect(() => {
    const stored = localStorage.getItem('recentContractIds')
    if (stored) {
      try {
        setRecentContracts(JSON.parse(stored))
      } catch (err) {
        console.error('Failed to parse recent contracts from localStorage:', err)
      }
    }

    // Test backend connection
    const testConnection = async () => {
              try {
          await contractApi.testConnection()
          setBackendStatus('connected')
        } catch {
          setBackendStatus('disconnected')
          toast.error('Backend server is not responding. Please ensure the FastAPI server is running on http://localhost:8000', {
            duration: 8000
          })
        }
    }

    testConnection()
  }, [])

  const saveContractToLocalStorage = (contractId: number) => {
    const updated = [contractId, ...recentContracts.filter(id => id !== contractId)].slice(0, 10)
    setRecentContracts(updated)
    localStorage.setItem('recentContractIds', JSON.stringify(updated))
  }

  const handleFormSubmit = async (data: ContractData, signature?: File | string) => {
    setIsLoading(true)
    setError('')
    setContract(undefined)

    try {
      toast.loading('Generating contract...', { id: 'contract-generation' })
      
      const response = await contractApi.createContract(data, signature)
      setContract(response)
      saveContractToLocalStorage(response.contract_id)
      
      toast.success('Contract generated successfully!', { 
        id: 'contract-generation',
        duration: 4000 
      })

      // Show email status if recipient email was provided
      if (data.recipient_email && data.recipient_email.trim() !== '') {
        if (response.email_sent) {
          toast.success(`Contract PDF sent to ${data.recipient_email}`, { 
            duration: 5000 
          })
        } else {
          toast.error(`Failed to send email to ${data.recipient_email}`, { 
            duration: 5000 
          })
        }
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred'
      setError(errorMessage)
      
      toast.error(`Failed to generate contract: ${errorMessage}`, { 
        id: 'contract-generation',
        duration: 6000 
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewContract = () => {
    setContract(undefined)
    setError('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            style: {
              background: '#10b981',
            },
          },
          error: {
            duration: 5000,
            style: {
              background: '#ef4444',
            },
          },
        }}
      />
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Contract Generator</h1>
              <span className="ml-2 px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                Beta
              </span>
              
              {/* Backend Status Indicator */}
              <div className="ml-4 flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${
                  backendStatus === 'connected' ? 'bg-green-500' :
                  backendStatus === 'disconnected' ? 'bg-red-500' :
                  'bg-yellow-500 animate-pulse'
                }`} />
                <span className="text-xs text-gray-600">
                  {backendStatus === 'connected' ? 'API Connected' :
                   backendStatus === 'disconnected' ? 'API Disconnected' :
                   'Checking API...'}
                </span>
              </div>
            </div>
            
            {contract && (
              <button
                onClick={handleNewContract}
                className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors"
              >
                Create New Contract
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Contract Form */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="mb-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  Create New Contract
                </h2>
                <p className="text-gray-600 text-sm">
                  Fill out the form below to generate a professional contract with automatic PDF generation.
                </p>
              </div>
              
              <ContractForm 
                onSubmit={handleFormSubmit}
                isLoading={isLoading}
              />
            </div>

            {/* Instructions Card */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">How it works</h3>
              <div className="space-y-3">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                    1
                  </div>
                  <p className="text-sm text-gray-600">
                    Fill out the contract details including parties, terms, and dates
                  </p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                    2
                  </div>
                  <p className="text-sm text-gray-600">
                    Click "Generate Contract" to create the document with HTML preview
                  </p>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                    3
                  </div>
                  <p className="text-sm text-gray-600">
                    Download the PDF or preview the HTML version in the right panel
                  </p>
                </div>
              </div>
            </div>

            {/* Recent Contracts */}
            {recentContracts.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Contracts</h3>
                <div className="space-y-2">
                  {recentContracts.slice(0, 5).map((contractId) => (
                    <div 
                      key={contractId}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-md"
                    >
                      <span className="text-sm font-medium text-gray-700">
                        Contract #{contractId}
                      </span>
                      <button
                        onClick={() => {
                          // You could implement a load contract function here
                          toast(`Contract #${contractId} - View feature coming soon!`)
                        }}
                        className="text-xs text-blue-600 hover:text-blue-800"
                      >
                        View
                      </button>
                    </div>
                  ))}
                </div>
                {recentContracts.length > 5 && (
                  <p className="text-xs text-gray-500 mt-2">
                    Showing 5 of {recentContracts.length} recent contracts
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Right Column - Contract Preview */}
          <div className="lg:sticky lg:top-8 lg:self-start">
            <ContractPreview 
              contract={contract}
              isLoading={isLoading}
              error={error}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <p className="text-gray-600 text-sm">
              Built with React, TypeScript, Tailwind CSS, and FastAPI
            </p>
            <p className="text-gray-500 text-xs mt-2">
              Professional contract generation with automatic PDF creation
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
