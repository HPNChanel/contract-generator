import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface ContractData {
  contract_type: string
  party_a: {
    name: string
    email?: string
    address?: string
  }
  party_b: {
    name: string
    email?: string
    address?: string
  }
  terms: string
  start_date: string
  end_date: string
  additional_clauses?: string[]
  custom_pdf_filename?: string
}

export interface ContractResponse {
  message: string
  contract_id: number
  contract_data: {
    id: number
    contract_type: string
    party_a: {
      name: string
      email?: string
      address?: string
    }
    party_b: {
      name: string
      email?: string
      address?: string
    }
    terms: string
    start_date: string
    end_date: string
    additional_clauses?: string[]
    created_at: string
    updated_at: string
  }
  preview_html: string
  pdf_info: {
    pdf_path: string
    filename: string
    download_url: string
  }
}

export interface ApiError {
  detail: string
}

export const contractApi = {
  // Test backend connection
  testConnection: async () => {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.request) {
          throw new Error('Backend server is not responding. Please start the FastAPI server.')
        }
      }
      throw new Error('Connection test failed')
    }
  },
  // Create a new contract
  createContract: async (data: ContractData): Promise<ContractResponse> => {
    try {
      const response = await api.post<ContractResponse>('/contracts', data)
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          // Server responded with error status
          const detail = error.response.data?.detail || 'Failed to create contract'
          throw new Error(detail)
        } else if (error.request) {
          // Request was made but no response received (CORS, network issues)
          throw new Error('Unable to connect to the server. Please ensure the backend is running on http://localhost:8000')
        } else {
          // Something else happened
          throw new Error('Request configuration error')
        }
      }
      throw new Error('An unexpected error occurred')
    }
  },

  // Get all contracts
  getContracts: async (skip = 0, limit = 100) => {
    try {
      const response = await api.get(`/contracts?skip=${skip}&limit=${limit}`)
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Failed to fetch contracts')
      }
      throw new Error('Network error occurred')
    }
  },

  // Get a specific contract
  getContract: async (contractId: number) => {
    try {
      const response = await api.get(`/contracts/${contractId}`)
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Failed to fetch contract')
      }
      throw new Error('Network error occurred')
    }
  },

  // Delete a contract
  deleteContract: async (contractId: number, deletePdf = true) => {
    try {
      const response = await api.delete(`/contracts/${contractId}?delete_pdf=${deletePdf}`)
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Failed to delete contract')
      }
      throw new Error('Network error occurred')
    }
  },

  // Generate PDF for existing contract
  generatePdf: async (contractId: number, customFilename?: string) => {
    try {
      const url = customFilename 
        ? `/contracts/${contractId}/pdf?custom_filename=${encodeURIComponent(customFilename)}`
        : `/contracts/${contractId}/pdf`
      const response = await api.get(url)
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Failed to generate PDF')
      }
      throw new Error('Network error occurred')
    }
  },

  // Get sample contract data
  getSampleData: async () => {
    try {
      const response = await api.get('/contracts/sample-data')
      return response.data
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Failed to fetch sample data')
      }
      throw new Error('Network error occurred')
    }
  }
}

export default api 