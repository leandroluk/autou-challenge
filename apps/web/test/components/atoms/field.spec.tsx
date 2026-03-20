import {
  Field,
  FieldContent,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldLegend,
  FieldSeparator,
  FieldSet,
  FieldTitle,
} from "@/components/atoms/field"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/atoms/field", () => {
  it("should render FieldSet with correct data-slot", () => {
    render(<FieldSet data-testid="fieldset">Content</FieldSet>)
    const element = screen.getByTestId("fieldset")
    expect(element.tagName).toBe("FIELDSET")
    expect(element).toHaveAttribute("data-slot", "field-set")
  })

  it.each([
    ["legend", "data-[variant=legend]:text-base"],
    ["label", "data-[variant=label]:text-sm"],
  ])("should render FieldLegend with %s variant", (variant, expectedClass) => {
    render(<FieldLegend variant={variant as any}>Legend</FieldLegend>)
    const element = screen.getByText("Legend")
    expect(element).toHaveAttribute("data-variant", variant)
    expect(element).toHaveClass(expectedClass)
  })

  it("should render FieldGroup with correct data-slot", () => {
    render(<FieldGroup>Group Content</FieldGroup>)
    expect(screen.getByText("Group Content")).toHaveAttribute("data-slot", "field-group")
  })

  it.each([
    ["vertical", "flex-col"],
    ["horizontal", "flex-row"],
    ["responsive", "flex-col"],
  ])("should render Field with %s orientation", (orientation, expectedClass) => {
    render(<Field orientation={orientation as any}>Field Content</Field>)
    const element = screen.getByRole("group")
    expect(element).toHaveAttribute("data-orientation", orientation)
    expect(element).toHaveClass(expectedClass)
  })

  it("should render FieldContent correctly", () => {
    render(<FieldContent>Content</FieldContent>)
    expect(screen.getByText("Content")).toHaveAttribute("data-slot", "field-content")
  })

  it("should render FieldLabel and FieldTitle", () => {
    render(
      <>
        <FieldLabel>Label</FieldLabel>
        <FieldTitle>Title</FieldTitle>
      </>
    )
    expect(screen.getByText("Label")).toHaveAttribute("data-slot", "field-label")
    expect(screen.getByText("Title")).toHaveAttribute("data-slot", "field-label")
  })

  it("should render FieldDescription", () => {
    render(<FieldDescription>Description</FieldDescription>)
    const element = screen.getByText("Description")
    expect(element.tagName).toBe("P")
    expect(element).toHaveAttribute("data-slot", "field-description")
  })

  describe("FieldSeparator", () => {
    it("should render without children", () => {
      const { container } = render(<FieldSeparator />)
      const element = container.firstChild as HTMLElement
      expect(element).toHaveAttribute("data-content", "false")
    })

    it("should render with children", () => {
      render(<FieldSeparator>OR</FieldSeparator>)
      const content = screen.getByText("OR")
      expect(content).toHaveAttribute("data-slot", "field-separator-content")
      expect(content.parentElement).toHaveAttribute("data-content", "true")
    })
  })

  describe("FieldError", () => {
    it("should return null if no errors and no children", () => {
      const { container } = render(<FieldError />)
      expect(container.firstChild).toBeNull()
    })

    it("should render children if provided", () => {
      render(<FieldError>Custom Error</FieldError>)
      expect(screen.getByText("Custom Error")).toBeInTheDocument()
    })

    it("should render a single error message as text", () => {
      const errors = [{ message: "Required field" }]
      render(<FieldError errors={errors} />)
      expect(screen.getByText("Required field")).toBeInTheDocument()
      expect(screen.queryByRole("list")).not.toBeInTheDocument()
    })

    it("should render unique multiple errors as a list", () => {
      const errors = [
        { message: "Error 1" },
        { message: "Error 2" },
        { message: "Error 1" },
      ]
      render(<FieldError errors={errors} />)
      const listItems = screen.getAllByRole("listitem")
      expect(listItems).toHaveLength(2)
      expect(listItems[0]).toHaveTextContent("Error 1")
      expect(listItems[1]).toHaveTextContent("Error 2")
    })

    it("should ignore errors without messages", () => {
      const errors = [{ message: "Valid error" }, { message: undefined }, undefined] as any
      render(<FieldError errors={errors} />)

      expect(screen.getByText("Valid error")).toBeInTheDocument()
      // The component renders a list because uniqueErrors.length is 2 ([{message}, undefined])
      expect(screen.getByRole("list")).toBeInTheDocument()
      expect(screen.getAllByRole("listitem")).toHaveLength(1)
    })
  })

  it("should apply custom classNames to all sub-components", () => {
    render(<Field className="custom-field" />)
    expect(screen.getByRole("group")).toHaveClass("custom-field")

    render(<FieldLabel className="custom-label">L</FieldLabel>)
    expect(screen.getByText("L")).toHaveClass("custom-label")
  })
})