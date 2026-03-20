import { Badge } from "@/components/atoms/badge"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/atoms/badge", () => {
  it("should render as a span by default", () => {
    render(<Badge>Content</Badge>)
    const badge = screen.getByText("Content")
    expect(badge.tagName).toBe("SPAN")
    expect(badge).toHaveClass("bg-primary")
  })

  it.each([
    ["default", "bg-primary"],
    ["secondary", "bg-secondary"],
    ["destructive", "bg-destructive/10"],
    ["outline", "border-border"],
    ["ghost", "hover:bg-muted"],
    ["link", "text-primary"],
  ])("should render the %s variant correctly", (variant, expectedClass) => {
    render(<Badge variant={variant as any}>Content</Badge>)
    expect(screen.getByText("Content")).toHaveClass(expectedClass)
  })

  it("should apply custom className", () => {
    render(<Badge className="custom-class">Content</Badge>)
    expect(screen.getByText("Content")).toHaveClass("custom-class")
  })

  it("should support polymorphic rendering via render prop", () => {
    render(
      <Badge render={(props) => <a {...props} href="https://google.com" />}>
        Link Badge
      </Badge>
    )
    const badge = screen.getByRole("link")
    expect(badge.tagName).toBe("A")
    expect(badge).toHaveAttribute("href", "https://google.com")
    expect(badge).toHaveClass("bg-primary")
  })

  it("should forward additional props to the element", () => {
    render(<Badge data-testid="badge-element" id="test-id">Content</Badge>)
    const badge = screen.getByTestId("badge-element")
    expect(badge).toHaveAttribute("id", "test-id")
  })

  it("should handle aria-invalid state for accessibility styles", () => {
    render(<Badge aria-invalid="true">Invalid</Badge>)
    expect(screen.getByText("Invalid")).toHaveAttribute("aria-invalid", "true")
  })
})