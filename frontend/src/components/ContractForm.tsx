import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Textarea } from './ui/textarea'
import { Select } from './ui/select'
import { Label } from './ui/label'
import { Card, CardContent, CardHeader, CardTitle } from './ui/card'

// Form validation schema
const contractFormSchema = z.object({
  contract_type: z.string().min(1, "Contract type is required"),
  party_a: z.object({
    name: z.string().min(1, "Party A name is required"),
    email: z.string().email("Invalid email address").optional().or(z.literal("")),
    address: z.string().optional()
  }),
  party_b: z.object({
    name: z.string().min(1, "Party B name is required"),
    email: z.string().email("Invalid email address").optional().or(z.literal("")),
    address: z.string().optional()
  }),
  terms: z.string().min(10, "Terms must be at least 10 characters long"),
  start_date: z.string().min(1, "Start date is required"),
  end_date: z.string().min(1, "End date is required"),
  additional_clauses: z.array(z.string()).optional()
})

type ContractFormData = z.infer<typeof contractFormSchema>

interface ContractFormProps {
  onSubmit: (data: ContractFormData) => void
  isLoading?: boolean
}

const contractTypes = [
  { value: "", label: "Select contract type" },
  { value: "Service Agreement", label: "Service Agreement" },
  { value: "Employment Contract", label: "Employment Contract" },
  { value: "Non-Disclosure Agreement", label: "Non-Disclosure Agreement" },
  { value: "Partnership Agreement", label: "Partnership Agreement" },
  { value: "Consulting Agreement", label: "Consulting Agreement" },
  { value: "Freelance Contract", label: "Freelance Contract" },
  { value: "Sales Agreement", label: "Sales Agreement" },
  { value: "Rental Agreement", label: "Rental Agreement" }
]

export function ContractForm({ onSubmit, isLoading = false }: ContractFormProps) {
  const [additionalClauses, setAdditionalClauses] = useState<string[]>([''])

  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue
  } = useForm<ContractFormData>({
    resolver: zodResolver(contractFormSchema),
    defaultValues: {
      contract_type: "",
      party_a: { name: "", email: "", address: "" },
      party_b: { name: "", email: "", address: "" },
      terms: "",
      start_date: "",
      end_date: "",
      additional_clauses: []
    }
  })

  const handleAddClause = () => {
    setAdditionalClauses([...additionalClauses, ''])
  }

  const handleRemoveClause = (index: number) => {
    const newClauses = additionalClauses.filter((_, i) => i !== index)
    setAdditionalClauses(newClauses)
    setValue('additional_clauses', newClauses.filter(clause => clause.trim() !== ''))
  }

  const handleClauseChange = (index: number, value: string) => {
    const newClauses = [...additionalClauses]
    newClauses[index] = value
    setAdditionalClauses(newClauses)
    setValue('additional_clauses', newClauses.filter(clause => clause.trim() !== ''))
  }

  const onFormSubmit = (data: ContractFormData) => {
    // Filter out empty additional clauses
    const filteredData = {
      ...data,
      additional_clauses: additionalClauses.filter(clause => clause.trim() !== '')
    }
    onSubmit(filteredData)
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Contract Details</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6">
          {/* Contract Type */}
          <div className="space-y-2">
            <Label htmlFor="contract_type">Contract Type *</Label>
            <Select {...register("contract_type")} id="contract_type">
              {contractTypes.map((type) => (
                <option key={type.value} value={type.value}>
                  {type.label}
                </option>
              ))}
            </Select>
            {errors.contract_type && (
              <p className="text-sm text-destructive">{errors.contract_type.message}</p>
            )}
          </div>

          {/* Party A Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Party A Information</h3>
            <div className="grid grid-cols-1 gap-4">
              <div className="space-y-2">
                <Label htmlFor="party_a_name">Name *</Label>
                <Input
                  {...register("party_a.name")}
                  id="party_a_name"
                  placeholder="Enter Party A name"
                />
                {errors.party_a?.name && (
                  <p className="text-sm text-destructive">{errors.party_a.name.message}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="party_a_email">Email</Label>
                <Input
                  {...register("party_a.email")}
                  id="party_a_email"
                  type="email"
                  placeholder="Enter Party A email"
                />
                {errors.party_a?.email && (
                  <p className="text-sm text-destructive">{errors.party_a.email.message}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="party_a_address">Address</Label>
                <Textarea
                  {...register("party_a.address")}
                  id="party_a_address"
                  placeholder="Enter Party A address"
                  rows={3}
                />
              </div>
            </div>
          </div>

          {/* Party B Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Party B Information</h3>
            <div className="grid grid-cols-1 gap-4">
              <div className="space-y-2">
                <Label htmlFor="party_b_name">Name *</Label>
                <Input
                  {...register("party_b.name")}
                  id="party_b_name"
                  placeholder="Enter Party B name"
                />
                {errors.party_b?.name && (
                  <p className="text-sm text-destructive">{errors.party_b.name.message}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="party_b_email">Email</Label>
                <Input
                  {...register("party_b.email")}
                  id="party_b_email"
                  type="email"
                  placeholder="Enter Party B email"
                />
                {errors.party_b?.email && (
                  <p className="text-sm text-destructive">{errors.party_b.email.message}</p>
                )}
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="party_b_address">Address</Label>
                <Textarea
                  {...register("party_b.address")}
                  id="party_b_address"
                  placeholder="Enter Party B address"
                  rows={3}
                />
              </div>
            </div>
          </div>

          {/* Contract Dates */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="start_date">Start Date *</Label>
              <Input
                {...register("start_date")}
                id="start_date"
                type="date"
              />
              {errors.start_date && (
                <p className="text-sm text-destructive">{errors.start_date.message}</p>
              )}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="end_date">End Date *</Label>
              <Input
                {...register("end_date")}
                id="end_date"
                type="date"
              />
              {errors.end_date && (
                <p className="text-sm text-destructive">{errors.end_date.message}</p>
              )}
            </div>
          </div>

          {/* Terms */}
          <div className="space-y-2">
            <Label htmlFor="terms">Terms and Conditions *</Label>
            <Textarea
              {...register("terms")}
              id="terms"
              placeholder="Enter the terms and conditions of the contract"
              rows={6}
            />
            {errors.terms && (
              <p className="text-sm text-destructive">{errors.terms.message}</p>
            )}
          </div>

          {/* Additional Clauses */}
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label>Additional Clauses</Label>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={handleAddClause}
              >
                Add Clause
              </Button>
            </div>
            
            {additionalClauses.map((clause, index) => (
              <div key={index} className="flex gap-2">
                <Input
                  value={clause}
                  onChange={(e) => handleClauseChange(index, e.target.value)}
                  placeholder={`Additional clause ${index + 1}`}
                />
                {additionalClauses.length > 1 && (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => handleRemoveClause(index)}
                  >
                    Remove
                  </Button>
                )}
              </div>
            ))}
          </div>

          {/* Submit Button */}
          <div className="pt-4">
            <Button 
              type="submit" 
              className="w-full" 
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? "Generating Contract..." : "Generate Contract"}
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  )
} 