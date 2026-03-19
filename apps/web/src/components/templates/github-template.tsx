"use client"

import dynamic from 'next/dynamic';
import { PropsWithChildren } from "react";

const GitHubCorners = dynamic(
  () => import('@uiw/react-github-corners'),
  { ssr: false }
);

export function GithubTemplate({ children }: PropsWithChildren) {
  return (
    <div className="relative flex min-h-screen flex-col">
      <header className="absolute top-4 right-4 z-50">
        <GitHubCorners
          position="right"
          size={60}
          fixed
          bgColor='var(--accent)'
          target="_blank"
          href="https://github.com/leandroluk/autou-challenge"
        />
      </header>
      {children}
    </div>
  );
}