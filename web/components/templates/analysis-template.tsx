import { cn } from "@/components/utils";
import { PropsWithChildren } from "react";


export function AnalysisTemplate({ children }: PropsWithChildren) {
  return (
    <section className="flex min-h-screen flex-col items-center justify-center bg-zinc-50 p-6 dark:bg-black gap-6">
      <header className="space-y-2 text-center">
        <h1 className="text-2xl font-bold tracking-tight">AutoU Email Analyzer</h1>
        <p className="text-sm text-accent/80">Classify and suggest replies for emails.</p>
      </header>

      <main className={cn(`
        w-full max-w-2xl rounded-xl border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800
        dark:bg-zinc-950`)}>

        {children}
      </main>

      <footer>
        <p className="text-accent/80 text-xs">
          Built by{' '}
          <a href="https://github.com/leandroluk" target="_blank" rel="noopener noreferrer" className="underline">
            Leandro Santiago Gomes
          </a>{' '}
          for{' '}
          <a
            href="https://autou-digital.notion.site/Contexto-do-Desafio-18836ce78e5580d0b59bcf9610b27769"
            target="_blank"
            rel="noopener noreferrer"
            className="underline">
            AutoU Challenge
          </a>
        </p>
      </footer>
    </section>
  );
}