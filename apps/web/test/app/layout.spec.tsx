import RootLayout from "@/app/layout";
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

vi.mock("next/font/google", () => ({
  Inter: () => ({ className: "inter" }),
  Geist: () => ({ className: "geist" }),
  Geist_Mono: () => ({ className: "geist-mono" }),
}))

describe("app/layout", () => {
  it("should render layout infrastructure (coverage and content)", () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => { });
    render(<RootLayout><div data-testid="children">test</div></RootLayout>);
    expect(screen.getByTestId("children")).toBeInTheDocument();
    const result = RootLayout({ children: <div /> });
    expect(result.type).toBe("html");
    consoleSpy.mockRestore();
  });
});