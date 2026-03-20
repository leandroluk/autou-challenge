"use client"

import { Button } from "@/components/atoms/button"
import { Field, FieldContent, FieldError, FieldGroup, FieldLabel } from "@/components/atoms/field"
import { Input } from "@/components/atoms/input"
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/atoms/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/atoms/tabs"
import { Textarea } from "@/components/atoms/textarea"
import { EmailAnalyzerPortProviderEnum } from "@/domain/_shared/ports/email-analyzer"
import { useForm } from "@tanstack/react-form"
import { FileTextIcon, Loader2Icon, MailIcon, TypeIcon } from "lucide-react"
import { toast } from "sonner"
import { z } from "zod"

const analysisSchema = z.object({
  provider: z.enum(EmailAnalyzerPortProviderEnum),
  apiKey: z.string().min(1, "API key is required"),
  method: z.enum(["text", "file"]),
  text: z.string().optional(),
  file: z.instanceof(File).optional(),
})

type AnalysisFormValues = z.infer<typeof analysisSchema>

export function AnalysisForm({
  onSubmit,
  loading
}: {
  onSubmit: (data: FormData) => void
  loading: boolean
}) {
  const form = useForm({
    defaultValues: {
      provider: "" as EmailAnalyzerPortProviderEnum,
      apiKey: "",
      method: "text",
      text: "",
      file: undefined,
    } as AnalysisFormValues,
    validators: { onSubmit: analysisSchema },
    onSubmit: ({ value }) => {
      const formData = new FormData()
      formData.append("provider", value.provider)
      formData.append("api_key", value.apiKey)
      formData.append(value.method, value[value.method]!)

      onSubmit(formData)

      toast.success("Email sent for analysis", { dismissible: true })
    },
  })

  return (
    <form
      onSubmit={e => [e.preventDefault(), e.stopPropagation(), form.handleSubmit()]}
      className="space-y-6"
    >
      <FieldGroup className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <form.Field name="provider">
          {field => (
            <Field>
              <FieldLabel htmlFor={field.name}>Analysis Provider</FieldLabel>
              <FieldContent>
                <Select
                  value={field.state.value}
                  onValueChange={(val) => field.handleChange(val as EmailAnalyzerPortProviderEnum)}
                >
                  <SelectTrigger
                    data-testid="analysis-form_select_provider"
                    id={field.name}
                    className="w-full"
                  >
                    <SelectValue placeholder="Select an analysis provider" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectLabel>Select an analysis provider</SelectLabel>
                      {Object.values(EmailAnalyzerPortProviderEnum).map((provider, key) => (
                        <SelectItem key={key} value={provider}>{provider}</SelectItem>
                      ))}
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </FieldContent>
            </Field>
          )}
        </form.Field>

        <form.Field name="apiKey">
          {field => (
            <Field>
              <FieldLabel htmlFor={field.name}>Provider API Key</FieldLabel>
              <FieldContent>
                <Input
                  data-testid="analysis-form_input_api-key"
                  id={field.name}
                  type="password"
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  placeholder="Enter your API key"
                />
                <FieldError errors={field.state.meta.errors} />
              </FieldContent>
            </Field>
          )}
        </form.Field>
      </FieldGroup>

      <form.Field name="method">
        {field => (
          <Tabs
            value={field.state.value}
            onValueChange={(val) => field.handleChange(val as "text" | "file")}
            className="w-full"
          >
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="text" className="gap-2" data-testid="analysis-form_tab_text">
                <TypeIcon className="size-4" /> Direct Text
              </TabsTrigger>
              <TabsTrigger value="file" className="gap-2" data-testid="analysis-form_tab_file">
                <FileTextIcon className="size-4" /> File Upload
              </TabsTrigger>
            </TabsList>

            <TabsContent value="text" className="mt-4 space-y-4">
              <form.Field name="text">
                {textField => (
                  <Field>
                    <FieldLabel htmlFor={textField.name}>Paste email content here</FieldLabel>
                    <FieldContent>
                      <Textarea
                        data-testid="analysis-form_textarea_text"
                        id={textField.name}
                        value={textField.state.value ?? ""}
                        onBlur={textField.handleBlur}
                        onChange={(e) => textField.handleChange(e.target.value)}
                        placeholder="Paste the email body here..."
                        className="max-h-25"
                      />
                      <FieldError errors={textField.state.meta.errors} />
                    </FieldContent>
                  </Field>
                )}
              </form.Field>
            </TabsContent>

            <TabsContent value="file" className="mt-4 space-y-4">
              <form.Field name="file">
                {fileField => (
                  <Field>
                    <FieldLabel htmlFor={fileField.name}>Email File</FieldLabel>
                    <FieldContent>
                      <Input
                        data-testid="analysis-form_input_file"
                        id={fileField.name}
                        type="file"
                        accept=".pdf,.txt"
                        onChange={(e) => fileField.handleChange(e.target.files?.[0])}
                      />
                      <FieldError errors={fileField.state.meta.errors} />
                    </FieldContent>
                  </Field>
                )}
              </form.Field>
            </TabsContent>
          </Tabs>
        )}
      </form.Field>

      <form.Subscribe selector={(state) => [state.canSubmit, state.isSubmitting]}>
        {([canSubmit, isSubmitting]) => (
          <Button
            data-testid="analysis-form_button_submit"
            type="submit"
            className="w-full"
            disabled={!canSubmit || isSubmitting || loading}
          >
            {loading || isSubmitting ? (
              <>
                <Loader2Icon className="size-4 animate-spin" /> Processing...
              </>
            ) : (
              <>
                <MailIcon className="size-4" /> Analyze Email
              </>
            )}
          </Button>
        )}
      </form.Subscribe>
    </form>
  )
}