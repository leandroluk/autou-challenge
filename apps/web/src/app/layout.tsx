import { GithubTemplate } from "@/components/templates/github-template";
import { cn } from "@/components/utils";
import type { Metadata } from "next";
import { Geist, Geist_Mono, Inter } from "next/font/google";
import { PropsWithChildren } from "react";
import { Toaster } from "sonner";
import "./globals.css";

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AutoU Challenge",
  description: "AutoU Challenge",
  authors: [{ name: "Leandro Santiago Gomes", url: "https://www.linkedin.com/in/leandroluk" }],
  keywords: ["AutoU", "Challenge", "Leandro Santiago Gomes"],
  creator: "Leandro Santiago Gomes",
  publisher: "Leandro Santiago Gomes",
  openGraph: {
    type: "website",
    title: "AutoU Challenge",
    description: "AutoU Challenge",
    emails: ['leandroluk@gmail.com'],
    phoneNumbers: ['+55 11 98702-7807'],
    siteName: "AutoU Challenge",
  },
};

export default function RootLayout({ children }: Readonly<PropsWithChildren>) {
  return (
    <html lang="en" className={cn("font-sans", inter.variable)}>
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <Toaster />
        <GithubTemplate>
          {children}
        </GithubTemplate>
      </body>
    </html>
  );
}
