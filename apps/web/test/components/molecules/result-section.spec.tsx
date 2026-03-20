import { ResultSection } from "@/components/molecules/result-section"
import { CategoryEnum } from "@/domain/email/enums"
import { render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

vi.mock("@/components/atoms/badge", () => ({
  Badge: ({ children, variant }: any) => <span data-testid="badge" data-variant={variant}>{children}</span>
}))

vi.mock("@/components/atoms/card", () => ({
  Card: ({ children, className }: any) => <div data-testid="card" className={className}>{children}</div>,
  CardHeader: ({ children, className }: any) => <header className={className}>{children}</header>,
  CardTitle: ({ children, className }: any) => <h2 className={className}>{children}</h2>,
  CardContent: ({ children, className }: any) => <section className={className}>{children}</section>,
}))

describe("components/molecules/result-section", () => {
  const mockReply = "Dear Sir/Madam, the requested information follows."

  it("should render productive category with correct badge and styles", () => {
    render(<ResultSection category={CategoryEnum.PRODUCTIVE} reply={mockReply} />)

    const badge = screen.getByTestId("badge")
    expect(badge).toHaveTextContent("Productive")
    expect(badge).toHaveAttribute("data-variant", "default")
    expect(screen.getByText(mockReply)).toBeInTheDocument()
  })

  it("should render unproductive category with destructive badge", () => {
    render(<ResultSection category={CategoryEnum.UNPRODUCTIVE} reply={mockReply} />)

    const badge = screen.getByTestId("badge")
    expect(badge).toHaveTextContent("Unproductive")
    expect(badge).toHaveAttribute("data-variant", "destructive")
  })

  it("should apply animation and layout classes to the card wrapper", () => {
    render(<ResultSection category={CategoryEnum.PRODUCTIVE} reply={mockReply} />)

    const card = screen.getByTestId("card")
    expect(card).toHaveClass("animate-in", "fade-in", "slide-in-from-top-4", "ring-0")
  })

  it("should render the suggested reply header", () => {
    render(<ResultSection category={CategoryEnum.PRODUCTIVE} reply={mockReply} />)
    expect(screen.getByText("Suggested Reply")).toBeInTheDocument()
  })
})