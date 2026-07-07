import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "DocuMind",
  description: "Ask questions about uploaded PDFs.",
};

const links = [
  { href: "/", label: "Home" },
  { href: "/documents", label: "Documents" },
  { href: "/chat", label: "Chat" },
];

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 text-slate-950">
        <header className="border-b bg-white">
          <nav className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-4 py-4">
            <Link href="/" className="text-lg font-semibold">
              DocuMind
            </Link>
            <div className="flex gap-2 text-sm">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="rounded px-3 py-2 text-slate-700 hover:bg-slate-100 hover:text-slate-950"
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </nav>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-10">{children}</main>
      </body>
    </html>
  );
}
