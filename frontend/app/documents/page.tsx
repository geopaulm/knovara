export default function DocumentsPage() {
  return (
    <section className="page">
      <div className="page-header">
        <h1 className="page-title">Documents</h1>
        <p className="page-copy">
          Upload and manage PDFs here once the document API is connected.
        </p>
      </div>

      <div className="panel space-y-4">
        <div className="field">
          <label htmlFor="document-upload" className="label">
            PDF file
          </label>
          <input
            id="document-upload"
            type="file"
            accept="application/pdf"
            className="input"
          />
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <button type="button" className="button button-primary" disabled>
            Upload
          </button>
          <span className="badge badge-loading">Waiting for API</span>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_18rem]">
        <div className="empty-state">
          No documents yet. Uploaded PDFs will appear here with their
          processing status.
        </div>
        <div className="space-y-3">
          <div className="loading-row">
            <span className="spinner" aria-hidden="true" />
            <span>Loading documents</span>
          </div>
          <p className="error-message">
            Unable to reach the document service. Please check that the backend
            is running.
          </p>
        </div>
      </div>
    </section>
  );
}
