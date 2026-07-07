import Link from "next/link";

export default function HomePage() {
  return (
    <section className="space-y-6">
      <div className="space-y-3">
        <h1 className="text-4xl font-bold tracking-tight">DocuMind</h1>
        <p className="max-w-2xl text-lg text-slate-700">
          Upload PDFs, ask questions, and get answers with source citations.
        </p>
      </div>
      <div className="flex flex-wrap gap-3">
        <Link
          href="/chat"
          className="rounded bg-slate-950 px-4 py-2 font-medium text-white hover:bg-slate-800"
        >
          Open Chat
        </Link>
        <Link
          href="/documents"
          className="rounded border border-slate-300 px-4 py-2 font-medium hover:bg-white"
        >
          Manage Documents
        </Link>
      </div>
    </section>
  );
}
