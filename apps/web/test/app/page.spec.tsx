import Page from "@/app/page";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

describe("app/page", () => {
  it("should render page", () => {
    render(<Page />)
    expect(screen.getByText("AutoU Email Analyzer")).toBeInTheDocument()
    expect(screen.getByTestId("analysis-form_button_submit")).toBeInTheDocument()
  })
})