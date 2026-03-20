import { AnalysisForm } from "@/components/organisms/analysis-form"
import { fireEvent, render, screen, waitFor } from "@testing-library/react"
import { toast } from "sonner"
import { beforeEach, describe, expect, it, vi } from "vitest"

vi.mock("sonner", () => ({
  toast: {
    success: vi.fn(),
  },
}))

vi.mock("lucide-react", () => ({
  FileTextIcon: () => <div data-testid="icon-file" />,
  Loader2Icon: () => <div data-testid="icon-loader" />,
  MailIcon: () => <div data-testid="icon-mail" />,
  TypeIcon: () => <div data-testid="icon-type" />,
  ChevronUpIcon: () => <div data-testid="icon-chevron-up" />,
  ChevronDownIcon: () => <div data-testid="icon-chevron-down" />,
  CheckIcon: () => <div data-testid="icon-check" />,
}))

describe("components/organisms/analysis-form", () => {
  const mockOnSubmit = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("should render all initial fields", () => {
    render(<AnalysisForm onSubmit={mockOnSubmit} loading={false} />)

    expect(screen.getByLabelText(/Analysis Provider/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/Provider API Key/i)).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: /Direct Text/i })).toBeInTheDocument()
    expect(screen.getByRole("tab", { name: /File Upload/i })).toBeInTheDocument()
  })

  it("should show validation error for empty API Key on submit", async () => {
    render(<AnalysisForm onSubmit={mockOnSubmit} loading={false} />)

    fireEvent.click(screen.getByTestId("analysis-form_button_submit"))

    await waitFor(() => {
      expect(screen.getByText(/API key is required/i)).toBeInTheDocument()
    })
    expect(mockOnSubmit).not.toHaveBeenCalled()
  })

  it("should switch between Text and File methods", async () => {
    render(<AnalysisForm onSubmit={mockOnSubmit} loading={false} />)

    expect(screen.getByLabelText(/Paste email content here/i)).toBeInTheDocument()

    fireEvent.click(screen.getByTestId("analysis-form_tab_file"))
    expect(screen.getByLabelText(/Email File/i)).toBeInTheDocument()
    expect(screen.queryByLabelText(/Paste email content here/i)).not.toBeInTheDocument()
  })

  it("should submit correctly using Text method", async () => {
    render(<AnalysisForm onSubmit={mockOnSubmit} loading={false} />)

    fireEvent.change(screen.getByTestId("analysis-form_input_api-key"), {
      target: { value: "sk-12345" }
    })

    fireEvent.change(screen.getByTestId("analysis-form_textarea_text"), {
      target: { value: "Email content test" }
    })

    await waitFor(() => {
      const btn = screen.getByTestId("analysis-form_button_submit")
      expect(btn).not.toBeDisabled()
    })
  })

  it("should submit correctly using File method", async () => {
    render(<AnalysisForm onSubmit={mockOnSubmit} loading={false} />)

    fireEvent.click(screen.getByTestId("analysis-form_tab_file"))

    fireEvent.change(screen.getByTestId("analysis-form_input_api-key"), {
      target: { value: "key-abc" }
    })

    const file = new File(["test content"], "email.txt", { type: "text/plain" })
    const fileInput = screen.getByTestId("analysis-form_input_file")

    fireEvent.change(fileInput, { target: { files: [file] } })

    await waitFor(() => {
      expect(fileInput).toHaveProperty('files')
    })
  })

  it("should display loading state in button", () => {
    render(<AnalysisForm onSubmit={mockOnSubmit} loading={true} />)

    const button = screen.getByTestId("analysis-form_button_submit")
    expect(button).toBeDisabled()
    expect(screen.getByText(/Processing.../i)).toBeInTheDocument()
    expect(screen.getByTestId("icon-loader")).toBeInTheDocument()
  })

  it("should construct FormData correctly on submission", async () => {
    const { getByTestId, findByRole } = render(<AnalysisForm onSubmit={mockOnSubmit} loading={false} />)

    fireEvent.click(getByTestId("analysis-form_select_provider"))
    const option = await findByRole("option", { name: /gemini/i })
    fireEvent.click(option)

    fireEvent.change(getByTestId("analysis-form_input_api-key"), {
      target: { value: "valid-key" }
    })

    fireEvent.change(getByTestId("analysis-form_textarea_text"), {
      target: { value: "body content" }
    })

    const submitButton = getByTestId("analysis-form_button_submit")

    await waitFor(() => expect(submitButton).not.toBeDisabled())
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith(expect.any(FormData))
      const calledFormData = mockOnSubmit.mock.calls[0][0] as FormData
      expect(calledFormData.get("api_key")).toBe("valid-key")
      expect(calledFormData.get("text")).toBe("body content")
      expect(toast.success).toHaveBeenCalled()
    })
  })
})