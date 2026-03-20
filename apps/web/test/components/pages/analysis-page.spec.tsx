import { AnalysisPage } from "@/components/pages/analysis-page";
import { CategoryEnum } from "@/domain/email/enums";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { toast } from "sonner";
import { beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("sonner", () => ({
  toast: {
    error: vi.fn(),
  },
}));

// Mock único e flexível para o formulário
vi.mock("@/components/organisms/analysis-form", () => ({
  AnalysisForm: ({ onSubmit, loading }: any) => (
    <button
      data-testid="submit-btn"
      disabled={loading}
      onClick={() => {
        // O teste vai injetar o que for necessário no window para simular diferentes FormDatas
        const formData = (window as any).__MOCK_FORM_DATA__ || new FormData();
        onSubmit(formData);
      }}
    >
      Submit
    </button>
  ),
}));

vi.mock("@/components/molecules/result-section", () => ({
  ResultSection: ({ category, reply }: any) => (
    <div data-testid="result-section">
      <span>{category}</span>
      <span>{reply}</span>
    </div>
  ),
}));

describe("components/pages/analysis-page", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn();
    process.env.NEXT_PUBLIC_API_URL = "http://localhost:3000";
    (window as any).__MOCK_FORM_DATA__ = null;
  });

  it("should render correctly", () => {
    render(<AnalysisPage />);
    expect(screen.getByTestId("submit-btn")).toBeInTheDocument();
  });

  it("should successfully analyze email and show result", async () => {
    const mockResult = { category: CategoryEnum.PRODUCTIVE, reply: "Ok" };
    (global.fetch as any).mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockResult),
    });

    const fd = new FormData();
    fd.append("api_key", "valid-key");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(screen.getByTestId("result-section")).toBeInTheDocument();
      expect(screen.getByText(/productive/i)).toBeInTheDocument();
      expect(screen.getByText("Ok")).toBeInTheDocument();
    });
  });

  it("should handle 400 Bad Request", async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 400,
      statusText: "Bad Request",
      json: () => Promise.resolve({ detail: "Invalid input" }),
    });

    const fd = new FormData();
    fd.append("api_key", "val");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith("Bad Request", expect.anything());
    });
  });

  it("should handle 502 Bad Gateway", async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 502,
      json: () => Promise.resolve({ detail: "Gateway Error" }),
    });

    const fd = new FormData();
    fd.append("api_key", "val");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalled();
    });
  });


  it("should handle network failure in catch block", async () => {
    (global.fetch as any).mockRejectedValue(new Error("Network failure"));

    const fd = new FormData();
    fd.append("api_key", "val");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith("Error analyzing email", expect.objectContaining({
        description: "Network failure"
      }));
    });
  });

  it("should handle generic HTTP errors (e.g. 500)", async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({ detail: "Server Error" }),
    });

    const fd = new FormData();
    fd.append("api_key", "val");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith("Error analyzing email", expect.objectContaining({
        description: "Server Error"
      }));
    });
  });

  it("should handle generic HTTP errors without detail", async () => {
    (global.fetch as any).mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({}),
    });

    const fd = new FormData();
    fd.append("api_key", "val");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalled();
    });
  });

  it("should handle non-Error throw object and existing provider", async () => {
    (global.fetch as any).mockRejectedValue("String error");

    const fd = new FormData();
    fd.append("api_key", "val");
    fd.append("provider", "some-provider");
    (window as any).__MOCK_FORM_DATA__ = fd;

    render(<AnalysisPage />);
    fireEvent.click(screen.getByTestId("submit-btn"));

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalled();
    });
  });
});
