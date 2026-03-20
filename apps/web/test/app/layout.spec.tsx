import RootLayout from "@/app/layout";
import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

vi.mock("next/font/google", () => ({
  Inter: () => ({ className: "inter" }),
  Geist: () => ({ className: "geist" }),
  Geist_Mono: () => ({ className: "geist-mono" }),
}))

describe("app/layout", () => {
  it("should render layout", () => {
    const { container } = render(
      <RootLayout>
        <div>test</div>
      </RootLayout>
    )
    expect(container).toBeDefined()
  })
})