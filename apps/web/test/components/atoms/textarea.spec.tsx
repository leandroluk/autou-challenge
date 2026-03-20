import { Textarea } from "@/components/atoms/textarea"
import { fireEvent, render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

describe("components/atoms/textarea", () => {
  it("should render correctly and have the correct data-slot", () => {
    render(<Textarea placeholder="Type here" />)
    const textarea = screen.getByPlaceholderText("Type here")
    expect(textarea).toBeInTheDocument()
    expect(textarea.tagName).toBe("TEXTAREA")
    expect(textarea).toHaveAttribute("data-slot", "textarea")
  })

  it("should handle value changes correctly", () => {
    const onChange = vi.fn()
    render(<Textarea placeholder="Change test" onChange={onChange} />)
    const textarea = screen.getByPlaceholderText("Change test")

    fireEvent.change(textarea, { target: { value: "Hello world" } })
    expect(onChange).toHaveBeenCalledTimes(1)
  })

  it("should apply disabled styles and attributes", () => {
    render(<Textarea placeholder="Disabled test" disabled />)
    const textarea = screen.getByPlaceholderText("Disabled test")
    expect(textarea).toBeDisabled()
    expect(textarea).toHaveClass("disabled:cursor-not-allowed", "disabled:opacity-50")
  })

  it("should apply aria-invalid classes for error states", () => {
    render(<Textarea placeholder="Invalid test" aria-invalid="true" />)
    const textarea = screen.getByPlaceholderText("Invalid test")
    expect(textarea).toHaveAttribute("aria-invalid", "true")
    expect(textarea).toHaveClass("aria-invalid:border-destructive")
  })

  it("should merge custom classNames", () => {
    render(<Textarea placeholder="Class test" className="custom-class" />)
    const textarea = screen.getByPlaceholderText("Class test")
    expect(textarea).toHaveClass("custom-class")
    expect(textarea).toHaveClass("border-input")
  })

  it("should forward additional textarea props", () => {
    render(<Textarea placeholder="Props test" rows={10} id="main-textarea" />)
    const textarea = screen.getByPlaceholderText("Props test")
    expect(textarea).toHaveAttribute("rows", "10")
    expect(textarea).toHaveAttribute("id", "main-textarea")
  })

  it("should maintain the field-sizing-content class for auto-resize support", () => {
    render(<Textarea placeholder="Resize test" />)
    expect(screen.getByPlaceholderText("Resize test")).toHaveClass("field-sizing-content")
  })
})