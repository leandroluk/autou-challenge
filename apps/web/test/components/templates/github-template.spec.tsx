import { GithubTemplate } from "@/components/templates/github-template"
import { render, screen } from "@testing-library/react"
import { describe, expect, it, vi } from "vitest"

vi.mock("@uiw/react-github-corners", () => ({
  default: ({ href }: { href: string }) => <div data-testid="github-corner" data-href={href} />
}))

describe("components/templates/github-template", () => {
  it("should render children correctly", () => {
    render(
      <GithubTemplate>
        <div data-testid="child">Content</div>
      </GithubTemplate>
    )

    expect(screen.getByTestId("child")).toBeInTheDocument()
    expect(screen.getByText("Content")).toBeInTheDocument()
  })

  it("should render the github corner with correct repository link", async () => {
    render(<GithubTemplate>Content</GithubTemplate>)

    const corner = await screen.findByTestId("github-corner")
    expect(corner).toBeInTheDocument()
    expect(corner).toHaveAttribute("data-href", "https://github.com/leandroluk/autou-challenge")
  })

  it("should have correct layout classes", () => {
    const { container } = render(<GithubTemplate>Content</GithubTemplate>)
    const wrapper = container.firstChild as HTMLElement

    expect(wrapper).toHaveClass("relative", "flex", "min-h-screen", "flex-col")
  })
})