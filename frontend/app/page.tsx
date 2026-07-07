import Link from "next/link";

const features = [
  {
    title: "Upload PDFs",
    copy: "Add the documents you want DocuMind to search.",
  },
  {
    title: "Ask questions",
    copy: "Use plain language instead of hunting through pages.",
  },
  {
    title: "Get answers with sources",
    copy: "See the response and the document evidence behind it.",
  },
];

export default function HomePage() {
  return (
    <section className="page">
      <div className="grid gap-8 lg:grid-cols-[1fr_22rem] lg:items-center">
        <div className="page-header">
          <p className="eyebrow">PDF question answering</p>
          <h1 className="page-title">DocuMind</h1>
          <p className="page-copy">
            Upload PDFs, ask questions, and get concise answers backed by
            source citations.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link href="/chat" className="button button-primary">
              Ask a question
            </Link>
            <Link href="/documents" className="button button-secondary">
              Upload PDFs
            </Link>
          </div>
        </div>

        <div className="panel space-y-4" aria-label="DocuMind workflow preview">
          <div className="flex items-center justify-between gap-3">
            <span className="text-sm font-medium text-slate-700">
              contract.pdf
            </span>
            <span className="badge badge-ready">Ready</span>
          </div>
          <div className="rounded-md bg-slate-100 p-4 text-sm leading-6 text-slate-700">
            What are the renewal terms?
          </div>
          <div className="rounded-md border border-slate-200 p-4 text-sm leading-6 text-slate-700">
            Renewal starts after the initial term unless either party gives
            notice. Sources: page 4.
          </div>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        {features.map((feature) => (
          <div key={feature.title} className="panel">
            <h2 className="text-base font-semibold text-slate-950">
              {feature.title}
            </h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              {feature.copy}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}
