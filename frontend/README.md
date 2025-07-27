# Contract Generator Frontend

A modern React + TypeScript frontend application for generating professional contracts with automatic PDF creation.

## Features

- **Modern UI**: Built with React 19, TypeScript, and Tailwind CSS
- **ShadCN UI Components**: Professional, accessible UI components
- **Responsive Design**: 2-column layout that adapts to mobile devices
- **Form Validation**: Comprehensive form validation with Zod and React Hook Form
- **Real-time Preview**: Live contract preview with HTML and PDF generation
- **API Integration**: Seamless integration with FastAPI backend

## Technologies

- **React 19** - Modern React with latest features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server
- **Tailwind CSS** - Utility-first CSS framework
- **ShadCN UI** - High-quality component library
- **React Hook Form** - Performant forms with easy validation
- **Zod** - TypeScript-first schema validation
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open [http://localhost:5173](http://localhost:5173) in your browser

### Backend Integration

Make sure the FastAPI backend is running on `http://localhost:8000`. The frontend expects these endpoints:

- `POST /api/v1/contracts` - Create new contract
- `GET /api/v1/contracts/{id}` - Get contract details
- `GET /api/v1/contracts/download/{filename}` - Download PDF files
- `GET /api/v1/contracts/sample-data` - Get sample data

## Project Structure

```
src/
├── components/           # React components
│   ├── ui/              # ShadCN UI components
│   ├── ContractForm.tsx # Main contract form
│   └── ContractPreview.tsx # Contract preview panel
├── services/            # API services
│   └── api.ts          # Backend API integration
├── lib/                # Utilities
│   └── utils.ts        # Class name utilities
└── App.tsx             # Main application component
```

## Usage

1. **Fill Contract Form**: Enter contract details in the left panel
   - Contract type (dropdown selection)
   - Party A and Party B information
   - Contract dates and terms
   - Optional additional clauses

2. **Generate Contract**: Click "Generate Contract" to create the document

3. **Preview & Download**: Use the right panel to:
   - View contract details
   - Download PDF version
   - Preview HTML version
   - Get download links

## Form Fields

### Required Fields
- Contract Type
- Party A Name
- Party B Name  
- Start Date
- End Date
- Terms and Conditions (minimum 10 characters)

### Optional Fields
- Party email addresses
- Party addresses
- Additional contract clauses
- Custom PDF filename

## API Integration

The frontend communicates with the FastAPI backend using Axios. All API calls are handled in `src/services/api.ts` with proper error handling and TypeScript interfaces.

### API Response Example

```json
{
  "message": "Contract created successfully",
  "contract_id": 1,
  "contract_data": {
    "id": 1,
    "contract_type": "Service Agreement",
    "party_a": {"name": "Company A"},
    "party_b": {"name": "Company B"},
    "terms": "Contract terms...",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  },
  "preview_html": "<html>...</html>",
  "pdf_info": {
    "filename": "contract_20240127_143022.pdf",
    "download_url": "/api/v1/contracts/download/contract_20240127_143022.pdf"
  }
}
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Environment Setup

The application is configured to work with:
- **Frontend**: http://localhost:5173 (Vite dev server)
- **Backend**: http://localhost:8000 (FastAPI server)

### Adding New Components

When adding new ShadCN UI components:

1. Create the component in `src/components/ui/`
2. Use proper TypeScript interfaces
3. Follow the established patterns for styling and props

## Production Build

To build for production:

```bash
npm run build
```

The build output will be in the `dist/` directory, ready for deployment to any static hosting service.

## Contributing

1. Follow TypeScript best practices
2. Use Tailwind CSS for styling
3. Maintain component consistency with ShadCN UI patterns
4. Add proper error handling for API calls
5. Test responsive design on multiple screen sizes
