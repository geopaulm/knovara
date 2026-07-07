export default function ChatPage() {
  return (
    <section className="page">
      <div className="page-header">
        <h1 className="page-title">Chat</h1>
        <p className="page-copy">
          Ask questions here once the chat API is connected.
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_18rem]">
        <form className="panel space-y-4">
          <div className="field">
            <label htmlFor="question" className="label">
              Question
            </label>
            <textarea
              id="question"
              rows={5}
              className="input resize-y"
              placeholder="What does this document say about renewal terms?"
            />
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <button type="submit" className="button button-primary" disabled>
              Ask DocuMind
            </button>
            <span className="badge badge-ready">Ready for chat API</span>
          </div>
        </form>

        <aside className="space-y-3" aria-label="Chat states">
          <div className="empty-state">
            Answers will appear here after you ask a question.
          </div>
          <div className="loading-row">
            <span className="spinner" aria-hidden="true" />
            <span>Generating answer</span>
          </div>
          <p className="error-message">
            Something went wrong while asking DocuMind. Please try again.
          </p>
        </aside>
      </div>
    </section>
  );
}
