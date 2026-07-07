import Link from "next/link";

export default function HomePage() {
  return (
    <section className="page">
      <div className="page-header">
        <p className="eyebrow">PDF question answering</p>
        <h1 className="page-title">DocuMind</h1>
        <p className="page-copy">
          Upload PDFs, ask questions, and get answers with source citations.
        </p>
      </div>
      <div className="flex flex-wrap gap-3">
        <Link href="/chat" className="button button-primary">
          Open Chat
        </Link>
        <Link href="/documents" className="button button-secondary">
          Manage Documents
        </Link>
      </div>
      <div className="grid gap-4 sm:grid-cols-3">
        {["Upload PDFs", "Ask questions", "Review sources"].map((feature) => (
          <div key={feature} className="panel">
            <h2 className="text-base font-semibold text-slate-950">{feature}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              A simple path through the core document workflow.
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
