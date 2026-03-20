import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectSeparator,
  SelectTrigger,
  SelectValue,
} from "@/components/atoms/select"
import { fireEvent, render, screen, waitFor } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

// Mock para evitar problemas com componentes de scroll do Base UI no JSDOM
vi.mock("@base-ui/react/select", async () => {
  const actual = await vi.importActual("@base-ui/react/select")
  return {
    ...actual,
    Select: {
      ...(actual as any).Select,
      ScrollUpArrow: ({ children, ...props }: any) => (
        <div {...props}>{children}</div>
      ),
      ScrollDownArrow: ({ children, ...props }: any) => (
        <div {...props}>{children}</div>
      ),
    },
  }
})

describe("components/atoms/select", () => {
  const TestSelect = ({ triggerProps = {}, contentProps = {} } = {}) => (
    <Select defaultValue="apple">
      <SelectTrigger data-testid="trigger" {...triggerProps}>
        <SelectValue placeholder="Select a fruit" />
      </SelectTrigger>
      <SelectContent {...contentProps}>
        <SelectGroup>
          <SelectLabel>Fruits</SelectLabel>
          <SelectItem value="apple">Apple</SelectItem>
          <SelectItem value="orange">Orange</SelectItem>
          <SelectSeparator data-testid="separator" />
          <SelectItem value="banana" disabled>Banana</SelectItem>
        </SelectGroup>
      </SelectContent>
    </Select>
  )

  it("should render the trigger and value correctly", () => {
    render(<TestSelect />)
    expect(screen.getByTestId("trigger")).toBeInTheDocument()
    expect(screen.getByText(/apple/i)).toBeInTheDocument()
  })

  it("should open content and display items on click", async () => {
    render(<TestSelect />)
    fireEvent.click(screen.getByTestId("trigger"))

    // findByRole lida com o estado assíncrono do portal/positioner
    expect(await screen.findByText("Fruits")).toBeInTheDocument()
    expect(screen.getByRole("option", { name: "Orange" })).toBeInTheDocument()
  })

  it("should change value when an item is selected", async () => {
    const onValueChange = vi.fn()

    render(
      <Select onValueChange={onValueChange}>
        <SelectTrigger data-testid="trigger">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="orange">Orange</SelectItem>
        </SelectContent>
      </Select>
    )

    fireEvent.click(screen.getByTestId("trigger"))

    const option = await screen.findByRole("option", { name: /orange/i })
    fireEvent.click(option)

    expect(onValueChange).toHaveBeenCalledWith("orange", expect.anything())
  })

  it.each([
    ["default", "data-[size=default]:h-8"],
    ["sm", "data-[size=sm]:h-7"],
  ])("should apply size %s to trigger", (size, expectedClass) => {
    render(<TestSelect triggerProps={{ size: size as any }} />)
    const trigger = screen.getByTestId("trigger")
    expect(trigger).toHaveClass(expectedClass)
    expect(trigger).toHaveAttribute("data-size", size)
  })

  it("should apply custom classNames to all sub-components", async () => {
    render(
      <Select open>
        <SelectTrigger className="custom-trigger" data-testid="trigger">
          <SelectValue className="custom-value" data-testid="value" />
        </SelectTrigger>
        <SelectContent className="custom-content" data-testid="content">
          <SelectGroup className="custom-group" data-testid="group">
            <SelectLabel className="custom-label" data-testid="label">L</SelectLabel>
            <SelectItem value="1" className="custom-item" data-testid="item">I</SelectItem>
            <SelectSeparator className="custom-sep" data-testid="sep" />
          </SelectGroup>
        </SelectContent>
      </Select>
    )

    expect(screen.getByTestId("trigger")).toHaveClass("custom-trigger")
    expect(screen.getByTestId("value")).toHaveClass("custom-value")

    // Elementos dentro do Portal/Positioner devem ser aguardados
    const content = await screen.findByTestId("content")
    expect(content).toHaveClass("custom-content")
    expect(screen.getByTestId("group")).toHaveClass("custom-group")
    expect(screen.getByTestId("label")).toHaveClass("custom-label")
    expect(screen.getByTestId("item")).toHaveClass("custom-item")
    expect(screen.getByTestId("sep")).toHaveClass("custom-sep")
  })

  it("should render disabled item correctly", async () => {
    render(<TestSelect />)
    fireEvent.click(screen.getByTestId("trigger"))

    const disabledItem = await screen.findByRole("option", { name: "Banana" })
    expect(disabledItem).toHaveAttribute("data-disabled", "")
    expect(disabledItem).toHaveClass("data-disabled:opacity-50")
  })

  it("should forward positioner props to SelectContent", async () => {
    render(
      <Select open>
        <SelectTrigger data-testid="trigger" />
        <SelectContent
          data-testid="content"
          side="top"
          align="start"
          alignItemWithTrigger={false}
        />
      </Select>
    )

    // Aguarda o positioner calcular e montar
    const content = await screen.findByTestId("content")
    expect(content).toHaveAttribute("data-align-trigger", "false")
    expect(content).toHaveAttribute("data-side", "top")
  })

  it("should render scroll buttons when content is long", async () => {
    render(
      <Select open>
        <SelectTrigger data-testid="trigger">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="1">1</SelectItem>
        </SelectContent>
      </Select>
    )

    await waitFor(() => {
      const upButton = document.querySelector("[data-slot='select-scroll-up-button']")
      const downButton = document.querySelector("[data-slot='select-scroll-down-button']")

      expect(upButton).toBeInTheDocument()
      expect(downButton).toBeInTheDocument()
      expect(upButton).toHaveClass("top-0")
      expect(downButton).toHaveClass("bottom-0")
    })
  })
})