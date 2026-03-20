import { AnalysisTemplate } from "@/components/templates/analysis-template"
import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

describe("components/templates/analysis-template", () => {
  it("should render children correctly", () => {
    render(
      <AnalysisTemplate>
        <div data-testid="child-content">Test Child</div>
      </AnalysisTemplate>
    )

    expect(screen.getByTestId("child-content")).toBeInTheDocument()
    expect(screen.getByText("Test Child")).toBeInTheDocument()
  })

  it("should render header with correct title and description", () => {
    render(<AnalysisTemplate>Content</AnalysisTemplate>)

    expect(screen.getByText("AutoU Email Analyzer")).toBeInTheDocument()
    expect(screen.getByText("Classify and suggest replies for emails.")).toBeInTheDocument()
  })

  it("should render footer links with correct attributes", () => {
    render(<AnalysisTemplate>Content</AnalysisTemplate>)

    const authorLink = screen.getByRole("link", { name: /leandro santiago gomes/i })
    const challengeLink = screen.getByRole("link", { name: /autou challenge/i })

    expect(authorLink).toHaveAttribute("href", "https://github.com/leandroluk")
    expect(authorLink).toHaveAttribute("target", "_blank")
    expect(authorLink).toHaveAttribute("rel", "noopener noreferrer")

    expect(challengeLink).toHaveAttribute(
      "href",
      "https://autou-digital.notion.site/Contexto-do-Desafio-18836ce78e5580d0b59bcf9610b27769"
    )
    expect(challengeLink).toHaveAttribute("target", "_blank")
    expect(challengeLink).toHaveAttribute("rel", "noopener noreferrer")
  })

  it("should have correct layout classes on the main container", () => {
    render(<AnalysisTemplate>Content</AnalysisTemplate>)

    const main = screen.getByRole("main")
    expect(main).toHaveClass("max-w-2xl", "rounded-xl", "border")
  })
})