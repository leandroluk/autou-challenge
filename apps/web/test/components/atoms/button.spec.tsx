import { Button } from "@/components/atoms/button"
import { fireEvent, render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

describe("components/atoms/button", () => {
  it("should render correctly with default props", () => {
    render(<Button>Click me</Button>)
    const button = screen.getByRole("button", { name: /click me/i })
    expect(button).toBeInTheDocument()
    expect(button).toHaveClass("bg-primary", "h-8")
  })

  it.each([
    ["default", "bg-primary"],
    ["outline", "border-border"],
    ["secondary", "bg-secondary"],
    ["ghost", "hover:bg-muted"],
    ["destructive", "bg-destructive/10"],
    ["link", "text-primary"],
  ])("should render the %s variant", (variant, expectedClass) => {
    render(<Button variant={variant as any}>Button</Button>)
    expect(screen.getByRole("button")).toHaveClass(expectedClass)
  })

  it.each([
    ["default", "h-8"],
    ["xs", "h-6"],
    ["sm", "h-7"],
    ["lg", "h-9"],
    ["icon", "size-8"],
    ["icon-xs", "size-6"],
    ["icon-sm", "size-7"],
    ["icon-lg", "size-9"],
  ])("should render the %s size", (size, expectedClass) => {
    render(<Button size={size as any}>Button</Button>)
    expect(screen.getByRole("button")).toHaveClass(expectedClass)
  })

  it("should handle click events", () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click</Button>)
    fireEvent.click(screen.getByRole("button"))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it("should be disabled when the disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>)
    const button = screen.getByRole("button")
    expect(button).toBeDisabled()
    expect(button).toHaveClass("disabled:opacity-50")
  })

  it("should apply custom className", () => {
    render(<Button className="custom-test-class">Button</Button>)
    expect(screen.getByRole("button")).toHaveClass("custom-test-class")
  })

  it("should support polymorphic rendering via render prop", () => {
    render(
      <Button
        nativeButton={false}
        render={<a href="https://github.com/leandroluk">GitHub</a>}
      />
    )

    const link = screen.getByText(/github/i)

    expect(link).toBeInTheDocument()
    expect(link).toHaveAttribute("href", "https://github.com/leandroluk")
    expect(link.tagName).toBe("A")
  })

  it("should forward additional props", () => {
    render(<Button title="button-title" data-custom="value">Button</Button>)
    const button = screen.getByRole("button")
    expect(button).toHaveAttribute("title", "button-title")
    expect(button).toHaveAttribute("data-custom", "value")
  })

  it("should have the correct data-slot attribute", () => {
    render(<Button>Button</Button>)
    expect(screen.getByRole("button")).toHaveAttribute("data-slot", "button")
  })
})