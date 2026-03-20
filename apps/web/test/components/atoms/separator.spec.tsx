import { Separator } from "@/components/atoms/separator"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/atoms/separator", () => {
  it("should render as a horizontal separator by default", () => {
    render(<Separator data-testid="separator" />)
    const separator = screen.getByTestId("separator")

    expect(separator).toBeInTheDocument()
    expect(separator).toHaveAttribute("data-orientation", "horizontal")
    expect(separator).toHaveClass("data-horizontal:h-px", "data-horizontal:w-full")
  })

  it("should render as a vertical separator", () => {
    render(<Separator orientation="vertical" data-testid="separator" />)
    const separator = screen.getByTestId("separator")

    expect(separator).toHaveAttribute("data-orientation", "vertical")
    expect(separator).toHaveClass("data-vertical:w-px", "data-vertical:self-stretch")
  })

  it("should apply custom className", () => {
    render(<Separator className="custom-test-class" data-testid="separator" />)
    expect(screen.getByTestId("separator")).toHaveClass("custom-test-class")
  })

  it("should forward extra props", () => {
    render(<Separator id="sep-01" data-testid="separator" />)
    expect(screen.getByTestId("separator")).toHaveAttribute("id", "sep-01")
  })

  it("should have the correct data-slot attribute", () => {
    render(<Separator data-testid="separator" />)
    expect(screen.getByTestId("separator")).toHaveAttribute("data-slot", "separator")
  })
})