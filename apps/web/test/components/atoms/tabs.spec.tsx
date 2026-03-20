import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/atoms/tabs"
import { fireEvent, render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/atoms/tabs", () => {
  const TestTabs = ({
    tabsProps = {},
    listProps = {}
  }: {
    tabsProps?: any,
    listProps?: any
  } = {}) => (
    <Tabs defaultValue="tab1" {...tabsProps}>
      <TabsList {...listProps}>
        <TabsTrigger value="tab1">Tab 1</TabsTrigger>
        <TabsTrigger value="tab2" disabled>Tab 2</TabsTrigger>
      </TabsList>
      <TabsContent value="tab1">Content 1</TabsContent>
      <TabsContent value="tab2">Content 2</TabsContent>
    </Tabs>
  )

  it("should render and switch tabs correctly", () => {
    render(<TestTabs />)

    expect(screen.getByText("Content 1")).toBeInTheDocument()
    expect(screen.queryByText("Content 2")).not.toBeInTheDocument()

    const trigger2 = screen.getByRole("tab", { name: /tab 2/i })
    expect(trigger2).toHaveAttribute("aria-disabled", "true")
    expect(trigger2).toHaveAttribute("data-disabled")
  })

  it("should change content when clicking an enabled tab", () => {
    render(
      <Tabs defaultValue="1">
        <TabsList>
          <TabsTrigger value="1">T1</TabsTrigger>
          <TabsTrigger value="2" data-testid="t2">T2</TabsTrigger>
        </TabsList>
        <TabsContent value="1">C1</TabsContent>
        <TabsContent value="2">C2</TabsContent>
      </Tabs>
    )

    fireEvent.click(screen.getByTestId("t2"))
    expect(screen.getByText("C2")).toBeInTheDocument()
    expect(screen.queryByText("C1")).not.toBeInTheDocument()
  })

  it.each([
    ["horizontal", "data-horizontal:flex-col"],
    ["vertical", "group/tabs"],
  ])("should apply orientation classes: %s", (orientation, expectedClass) => {
    const { container } = render(<TestTabs tabsProps={{ orientation }} />)
    const tabsRoot = container.firstChild as HTMLElement
    expect(tabsRoot).toHaveAttribute("data-orientation", orientation)
    if (orientation === "horizontal") {
      expect(tabsRoot).toHaveClass(expectedClass)
    }
  })

  it.each([
    ["default", "bg-muted"],
    ["line", "bg-transparent"],
  ])("should apply list variant: %s", (variant, expectedClass) => {
    render(<TestTabs listProps={{ variant }} />)
    const list = screen.getByRole("tablist")
    expect(list).toHaveAttribute("data-variant", variant)
    expect(list).toHaveClass(expectedClass)
  })

  it("should apply custom classNames to all components", () => {
    render(
      <Tabs className="custom-tabs">
        <TabsList className="custom-list">
          <TabsTrigger value="1" className="custom-trigger">T1</TabsTrigger>
        </TabsList>
        <TabsContent value="1" className="custom-content">C1</TabsContent>
      </Tabs>
    )

    expect(document.querySelector(".custom-tabs")).toBeInTheDocument()
    expect(screen.getByRole("tablist")).toHaveClass("custom-list")
    expect(screen.getByRole("tab")).toHaveClass("custom-trigger")
    expect(screen.getByText("C1")).toHaveClass("custom-content")
  })

  it("should verify data-slot attributes", () => {
    render(
      <Tabs>
        <TabsList>
          <TabsTrigger value="1">T1</TabsTrigger>
        </TabsList>
        <TabsContent value="1">C1</TabsContent>
      </Tabs>
    )

    expect(document.querySelector('[data-slot="tabs"]')).toBeInTheDocument()
    expect(screen.getByRole("tablist")).toHaveAttribute("data-slot", "tabs-list")
    expect(screen.getByRole("tab")).toHaveAttribute("data-slot", "tabs-trigger")
    expect(screen.getByText("C1")).toHaveAttribute("data-slot", "tabs-content")
  })

  it("should handle aria-disabled and disabled states on triggers", () => {
    render(
      <Tabs defaultValue="test">
        <TabsList>
          <TabsTrigger value="test" disabled aria-disabled="true">
            Disabled
          </TabsTrigger>
        </TabsList>
      </Tabs>
    )

    const trigger = screen.getByRole("tab")

    expect(trigger).toHaveAttribute("aria-disabled", "true")
    expect(trigger).toHaveAttribute("data-disabled")
    expect(trigger).toHaveClass("disabled:opacity-50", "aria-disabled:opacity-50")
  })
})