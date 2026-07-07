"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";

type DocumentStatus = "Uploaded" | "Processing" | "Ready" | "Failed";

type Document = {
  id: number;
  filename: string;
  status: DocumentStatus;
  size_bytes: number;
};

const statusClass: Record<DocumentStatus, string> = {
  Uploaded: "badge-loading",
  Processing: "badge-loading",
  Ready: "badge-ready",
  Failed: "badge-error",
};

function friendlyError(error: unknown) {
  return error instanceof TypeError
    ? "Unable to reach the document service. Please check that the backend is running."
    : "Something went wrong. Please try again.";
}

function isPdf(file: File) {
  return file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf");
}

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  async function loadDocuments() {
    setLoading(true);
    setError("");
    try {
      setDocuments(await apiFetch<Document[]>("/api/documents"));
    } catch (err) {
      setError(friendlyError(err));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDocuments();
  }, []);

  function selectFile(nextFile?: File) {
    if (!nextFile) return;
    if (!isPdf(nextFile)) {
      setFile(null);
      setError("Please choose a PDF file.");
      return;
    }
    setError("");
    setFile(nextFile);
  }

  async function uploadDocument() {
    if (!file) {
      setError("Choose a PDF before uploading.");
      return;
    }

    setUploading(true);
    setError("");
    const body = new FormData();
    body.append("file", file);

    try {
      const uploaded = await apiFetch<Document>("/api/documents", {
        method: "POST",
        body,
      });
      setDocuments((current) => [uploaded, ...current]);
      setFile(null);
    } catch (err) {
      setError(
        err instanceof TypeError
          ? friendlyError(err)
          : "Upload failed. Make sure the file is a valid PDF.",
      );
    } finally {
      setUploading(false);
    }
  }

  async function deleteDocument(id: number) {
    setDeletingId(id);
    setError("");
    try {
      await apiFetch<void>(`/api/documents/${id}`, { method: "DELETE" });
      setDocuments((current) => current.filter((document) => document.id !== id));
    } catch (err) {
      setError(friendlyError(err));
    } finally {
      setDeletingId(null);
    }
  }

  const hasFailedDocument = documents.some((document) => document.status === "Failed");

  return (
    <section className="page">
      <div className="page-header">
        <h1 className="page-title">Documents</h1>
        <p className="page-copy">
          Upload PDFs, track processing, and remove documents you no longer need.
        </p>
      </div>

      <div className="panel space-y-4">
        <label
          htmlFor="document-upload"
          className="block cursor-pointer rounded-lg border border-dashed border-slate-300 bg-slate-50 p-6 text-center transition hover:border-teal-600 hover:bg-white"
          onDragOver={(event) => event.preventDefault()}
          onDrop={(event) => {
            event.preventDefault();
            selectFile(event.dataTransfer.files[0]);
          }}
        >
          <span className="block text-sm font-medium text-slate-900">
            {file ? file.name : "Drop a PDF here or choose one"}
          </span>
          <span className="mt-1 block text-sm text-slate-600">
            PDF files only
          </span>
        </label>
        <input
          id="document-upload"
          type="file"
          accept="application/pdf,.pdf"
          className="sr-only"
          onChange={(event) => selectFile(event.target.files?.[0])}
        />

        <div className="flex flex-wrap items-center gap-3">
          <button
            type="button"
            className="button button-primary"
            disabled={uploading}
            onClick={uploadDocument}
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
          {uploading ? (
            <span className="loading-row py-2">
              <span className="spinner" aria-hidden="true" />
              <span>Uploading document</span>
            </span>
          ) : null}
        </div>
      </div>

      {error ? <p className="error-message">{error}</p> : null}
      {hasFailedDocument ? (
        <p className="error-message">
          One or more documents failed processing. Delete the failed document and
          try uploading it again.
        </p>
      ) : null}

      {loading ? (
        <div className="loading-row">
          <span className="spinner" aria-hidden="true" />
          <span>Loading documents</span>
        </div>
      ) : documents.length === 0 ? (
        <div className="empty-state">
          No documents yet. Uploaded PDFs will appear here with their processing
          status.
        </div>
      ) : (
        <div className="space-y-3">
          {documents.map((document) => (
            <div
              key={document.id}
              className="panel flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <div className="min-w-0">
                <h2 className="truncate text-base font-semibold text-slate-950">
                  {document.filename}
                </h2>
                <p className="mt-1 text-sm text-slate-600">
                  {(document.size_bytes / 1024).toFixed(1)} KB
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-3">
                <span className={`badge ${statusClass[document.status]}`}>
                  {document.status}
                </span>
                <button
                  type="button"
                  className="button button-secondary"
                  disabled={deletingId === document.id}
                  onClick={() => void deleteDocument(document.id)}
                >
                  {deletingId === document.id ? "Deleting..." : "Delete"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
