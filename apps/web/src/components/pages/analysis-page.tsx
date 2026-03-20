'use client'

import { ResultSection } from "@/components/molecules/result-section";
import { AnalysisForm } from "@/components/organisms/analysis-form";
import { CategoryEnum } from "@/domain/email/enums";
import { useState } from "react";
import { toast } from "sonner";

type State = {
  loading: boolean;
  result: { category: CategoryEnum; reply: string } | null;
}

const initialState: State = { loading: false, result: null }

export function AnalysisPage() {
  const [{ loading, result }, setState] = useState<State>(initialState);

  const onSubmit = async (formData: FormData) => {
    setState({ loading: true, result: null });
    let response: Awaited<ReturnType<typeof fetch>>;
    try {
      response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/email/analyze`, {
        method: "POST",
        body: formData,
        cache: "no-store",
      });

      if (!response.ok) {
        const data = await response.json()
        if (response.status === 400) {
          toast.error(response.statusText, {
            dismissible: true,
            description: <pre className="text-xs whitespace-pre-wrap">{data.detail}</pre>
          });
          return setState(initialState);
        }
        if (response.status === 502) {
          toast.error("Bad Gateway. Please try again later.", {
            dismissible: true,
            description: <pre className="text-xs whitespace-pre-wrap">{data.detail}</pre>
          });
          return setState(initialState);
        }
        throw new Error(data.detail);
      }

      setState({ loading: false, result: await response.json() });
    } catch (e) {
      toast.error("Error analyzing email", {
        dismissible: true,
        description: (e as Error).message,
      });
      setState(initialState);
    }
  };

  return (
    <>
      <AnalysisForm onSubmit={onSubmit} loading={loading} />
      {result && <ResultSection {...result} />}
    </>
  )
}