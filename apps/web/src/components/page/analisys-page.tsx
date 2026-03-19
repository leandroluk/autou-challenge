'use client'

import { ResultSection } from "@/components/molecules/result-section";
import { AnalysisForm } from "@/components/organisms/analysis-form";
import { EmailAnalyzerPortProviderEnum } from "@/domain/_shared/ports/email-analyzer";
import { CategoryEnum } from "@/domain/email/enums";
import { XIcon } from "lucide-react";
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

    try {
      if (!formData.get('provider')) {
        formData.set('provider', EmailAnalyzerPortProviderEnum.GEMINI_2_5_FLASH);
      }

      if (!formData.get('api_key')) {
        toast.error("API Key is required");
        setState(initialState);
        return;
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/email/analyze`, {
        method: "POST",
        body: formData,
        cache: "no-store",
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setState({ loading: false, result: data });

    } catch (e) {
      toast.error("Error analyzing email", {
        description: e instanceof Error ? e.message : "Please try again.",
        dismissible: true,
        icon: <XIcon />
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