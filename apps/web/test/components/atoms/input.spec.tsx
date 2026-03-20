import { Input } from "@/components/atoms/input"
import { fireEvent, render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

describe("components/atoms/input", () => {
  it("should render correctly with default props", () => {
    render(<Input placeholder="Enter text" />)
    const input = screen.getByPlaceholderText("Enter text")
    expect(input).toBeInTheDocument()
    expect(input).toHaveAttribute("data-slot", "input")
    expect(input).toHaveClass("border-input")
  })

  it("should forward the type prop", () => {
    render(<Input type="password" placeholder="Password" />)
    expect(screen.getByPlaceholderText("Password")).toHaveAttribute("type", "password")
  })

  it("should handle value changes", () => {
    const onChange = vi.fn()
    render(<Input onChange={onChange} placeholder="Input" />)
    const input = screen.getByPlaceholderText("Input")

    fireEvent.change(input, { target: { value: "test value" } })
    expect(onChange).toHaveBeenCalledTimes(1)
  })

  it("should apply disabled styles and attributes", () => {
    render(<Input disabled placeholder="Disabled" />)
    const input = screen.getByPlaceholderText("Disabled")
    expect(input).toBeDisabled()
    expect(input).toHaveClass("disabled:opacity-50", "disabled:cursor-not-allowed")
  })

  it("should apply aria-invalid styles", () => {
    render(<Input aria-invalid="true" placeholder="Invalid" />)
    const input = screen.getByPlaceholderText("Invalid")
    expect(input).toHaveAttribute("aria-invalid", "true")
    expect(input).toHaveClass("aria-invalid:border-destructive")
  })

  it("should merge custom className", () => {
    render(<Input className="custom-class" placeholder="Custom" />)
    expect(screen.getByPlaceholderText("Custom")).toHaveClass("custom-class")
  })

  it("should forward extra props to the input element", () => {
    render(<Input id="test-id" name="test-name" placeholder="Props" />)
    const input = screen.getByPlaceholderText("Props")
    expect(input).toHaveAttribute("id", "test-id")
    expect(input).toHaveAttribute("name", "test-name")
  })

  it("should render as a file input with specific file classes", () => {
    render(<Input type="file" data-testid="file-input" />)
    const input = screen.getByTestId("file-input")
    expect(input).toHaveClass("file:font-medium", "file:border-0")
  })
})