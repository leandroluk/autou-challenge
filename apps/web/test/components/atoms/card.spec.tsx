import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/atoms/card"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/atoms/card", () => {
  it("should render all card sub-components correctly", () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Title</CardTitle>
          <CardDescription>Description</CardDescription>
          <CardAction>Action</CardAction>
        </CardHeader>
        <CardContent>Content</CardContent>
        <CardFooter>Footer</CardFooter>
      </Card>
    )

    expect(screen.getByText("Title")).toBeInTheDocument()
    expect(screen.getByText("Description")).toBeInTheDocument()
    expect(screen.getByText("Action")).toBeInTheDocument()
    expect(screen.getByText("Content")).toBeInTheDocument()
    expect(screen.getByText("Footer")).toBeInTheDocument()
  })

  it("should apply size 'sm' attributes and classes", () => {
    const { container } = render(
      <Card size="sm">
        <CardHeader />
        <CardContent />
        <CardFooter />
      </Card>
    )

    const card = container.firstChild as HTMLElement
    expect(card).toHaveAttribute("data-size", "sm")
    expect(card).toHaveClass("data-[size=sm]:gap-3")
  })

  it("should apply conditional classes based on slots", () => {
    const { container } = render(
      <Card>
        <CardFooter>Footer</CardFooter>
      </Card>
    )
    const card = container.firstChild as HTMLElement
    expect(card).toHaveClass("has-data-[slot=card-footer]:pb-0")
  })

  it("should apply rounding to first-child images", () => {
    const { container } = render(
      <Card>
        <img src="test.jpg" alt="test" />
      </Card>
    )
    const card = container.firstChild as HTMLElement
    expect(card).toHaveClass("has-[>img:first-child]:pt-0")
  })

  it("should render CardAction with correct grid classes", () => {
    render(
      <CardHeader>
        <CardAction>Action</CardAction>
      </CardHeader>
    )
    expect(screen.getByText("Action")).toHaveClass("col-start-2")
  })

  it("should allow custom classNames on all components", () => {
    const components = [
      { Comp: Card, name: "card" },
      { Comp: CardHeader, name: "header" },
      { Comp: CardTitle, name: "title" },
      { Comp: CardDescription, name: "desc" },
      { Comp: CardAction, name: "action" },
      { Comp: CardContent, name: "content" },
      { Comp: CardFooter, name: "footer" },
    ]

    components.forEach(({ Comp, name }) => {
      render(<Comp className={`custom-${name}`}>{name}</Comp>)
      expect(screen.getByText(name)).toHaveClass(`custom-${name}`)
    })
  })

  it("should forward extra props to the underlying div", () => {
    render(<Card id="main-card" data-testid="card-test" />)
    const card = screen.getByTestId("card-test")
    expect(card).toHaveAttribute("id", "main-card")
  })

  it("should verify data-slot attributes for all components", () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>T</CardTitle>
          <CardDescription>D</CardDescription>
          <CardAction>A</CardAction>
        </CardHeader>
        <CardContent>C</CardContent>
        <CardFooter>F</CardFooter>
      </Card>
    )

    expect(screen.getByText("T")).toHaveAttribute("data-slot", "card-title")
    expect(screen.getByText("D")).toHaveAttribute("data-slot", "card-description")
    expect(screen.getByText("A")).toHaveAttribute("data-slot", "card-action")
    expect(screen.getByText("C")).toHaveAttribute("data-slot", "card-content")
    expect(screen.getByText("F")).toHaveAttribute("data-slot", "card-footer")
  })
})