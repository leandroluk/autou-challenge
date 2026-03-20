import { Label } from "@/components/atoms/label"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/atoms/label", () => {
  it("should render correctly as a label element", () => {
    render(<Label>Username</Label>)
    const label = screen.getByText("Username")
    expect(label.tagName).toBe("LABEL")
    expect(label).toBeInTheDocument()
  })

  it("should have the correct data-slot attribute", () => {
    render(<Label>Label</Label>)
    expect(screen.getByText("Label")).toHaveAttribute("data-slot", "label")
  })

  it("should apply default classes", () => {
    render(<Label>Label</Label>)
    const label = screen.getByText("Label")
    expect(label).toHaveClass("text-sm", "font-medium", "flex", "items-center")
  })

  it("should apply classes for disabled and peer-disabled states", () => {
    render(<Label>Label</Label>)
    const label = screen.getByText("Label")
    expect(label).toHaveClass("group-data-[disabled=true]:opacity-50")
    expect(label).toHaveClass("peer-disabled:opacity-50")
  })

  it("should merge custom className", () => {
    render(<Label className="custom-label-class">Label</Label>)
    expect(screen.getByText("Label")).toHaveClass("custom-label-class")
  })

  it("should forward standard label props like htmlFor", () => {
    render(<Label htmlFor="input-id">Label</Label>)
    expect(screen.getByText("Label")).toHaveAttribute("for", "input-id")
  })

  it("should forward additional props", () => {
    render(<Label data-testid="test-label" id="unique-id">Label</Label>)
    const label = screen.getByTestId("test-label")
    expect(label).toHaveAttribute("id", "unique-id")
  })
})