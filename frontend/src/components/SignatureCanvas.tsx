import React, { useRef, useEffect, useState, useCallback } from 'react'
import { Button } from './ui/button'

interface SignatureCanvasProps {
  onSignatureChange: (signature: string | null) => void
  disabled?: boolean
  width?: number
  height?: number
}

export function SignatureCanvas({ 
  onSignatureChange, 
  disabled = false, 
  width = 400, 
  height = 150 
}: SignatureCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [lastPosition, setLastPosition] = useState<{ x: number; y: number } | null>(null)
  const [isEmpty, setIsEmpty] = useState(true)

  // Initialize canvas
  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    canvas.width = width
    canvas.height = height

    // Set drawing styles
    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 2
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'

    // Fill with white background
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, width, height)
  }, [width, height])

  // Get coordinates relative to canvas
  const getCoordinates = useCallback((event: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas) return { x: 0, y: 0 }

    const rect = canvas.getBoundingClientRect()
    const scaleX = canvas.width / rect.width
    const scaleY = canvas.height / rect.height

    if ('touches' in event) {
      // Touch event
      const touch = event.touches[0]
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY
      }
    } else {
      // Mouse event
      return {
        x: (event.clientX - rect.left) * scaleX,
        y: (event.clientY - rect.top) * scaleY
      }
    }
  }, [])

  // Start drawing
  const startDrawing = useCallback((event: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (disabled) return
    
    event.preventDefault()
    setIsDrawing(true)
    const coords = getCoordinates(event)
    setLastPosition(coords)
  }, [disabled, getCoordinates])

  // Draw line
  const draw = useCallback((event: React.MouseEvent<HTMLCanvasElement> | React.TouchEvent<HTMLCanvasElement>) => {
    if (!isDrawing || disabled || !lastPosition) return

    event.preventDefault()
    const canvas = canvasRef.current
    const ctx = canvas?.getContext('2d')
    if (!canvas || !ctx) return

    const coords = getCoordinates(event)

    ctx.beginPath()
    ctx.moveTo(lastPosition.x, lastPosition.y)
    ctx.lineTo(coords.x, coords.y)
    ctx.stroke()

    setLastPosition(coords)
    setIsEmpty(false)
  }, [isDrawing, disabled, lastPosition, getCoordinates])

  // Stop drawing
  const stopDrawing = useCallback(() => {
    if (!isDrawing) return
    
    setIsDrawing(false)
    setLastPosition(null)

    // Convert canvas to base64 and notify parent
    const canvas = canvasRef.current
    if (canvas && !isEmpty) {
      const dataURL = canvas.toDataURL('image/png')
      onSignatureChange(dataURL)
    }
  }, [isDrawing, isEmpty, onSignatureChange])

  // Clear canvas
  const clearCanvas = useCallback(() => {
    const canvas = canvasRef.current
    const ctx = canvas?.getContext('2d')
    if (!canvas || !ctx) return

    // Clear and refill with white background
    ctx.fillStyle = '#ffffff'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    
    setIsEmpty(true)
    onSignatureChange(null)
  }, [onSignatureChange])

  // Undo last stroke (simplified - clears everything for now)
  const undoStroke = useCallback(() => {
    clearCanvas()
  }, [clearCanvas])

  return (
    <div className="space-y-3">
      <div className="border border-gray-300 rounded-lg p-4 bg-white">
        <canvas
          ref={canvasRef}
          className={`border border-dashed border-gray-300 rounded cursor-crosshair w-full ${
            disabled ? 'opacity-50 cursor-not-allowed' : ''
          }`}
          width={width}
          height={height}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
          disabled={disabled}
        />
        
        <div className="flex gap-2 mt-3 justify-end">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={undoStroke}
            disabled={disabled || isEmpty}
          >
            Undo
          </Button>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={clearCanvas}
            disabled={disabled || isEmpty}
          >
            Clear
          </Button>
        </div>
      </div>
      
      <p className="text-sm text-gray-500">
        {disabled 
          ? 'Signature drawing is disabled during form submission'
          : 'Draw your signature above using your mouse or finger'
        }
      </p>
    </div>
  )
}