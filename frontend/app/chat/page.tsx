"use client";

import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { apiFetch } from "../../lib/api";

type Document = {
  id: number;
  filename: string;
  status: "Uploaded" | "Processing" | "Ready" | "Failed";
};

type Message = {
  id: number;
  question: string;
  answer: string;
  noAnswer: boolean;
};

const maxQuestionLength = 1000;
const fallbackAnswer = "Not enough information in the uploaded documents.";
const noAnswerMessage =
  "The uploaded documents do not contain enough information to answer this question.";

type ChatResponse = {
  answer: string;
  sources: unknown[];
};

function friendlyError(error: unknown) {
  return error instanceof TypeError
    ? "Unable to reach the document service. Please check that the backend is running."
    : "Something went wrong while checking your documents. Please try again.";
}

export default function ChatPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState("");
  const [loadingDocuments, setLoadingDocuments] = useState(true);
  const [answerLoading, setAnswerLoading] = useState(false);

  useEffect(() => {
    async function loadDocuments() {
      try {
        setDocuments(await apiFetch<Document[]>("/api/documents"));
      } catch (err) {
        setError(friendlyError(err));
      } finally {
        setLoadingDocuments(false);
      }
    }

    void loadDocuments();
  }, []);

  const readyDocuments = documents.filter((document) => document.status === "Ready");
  const trimmedQuestion = question.trim();
  const questionTooLong = question.length > maxQuestionLength;
  const canAsk =
    trimmedQuestion.length > 0 &&
    !questionTooLong &&
    !answerLoading &&
    readyDocuments.length > 0;

  async function askQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!trimmedQuestion) {
      setError("Enter a question before asking DocuMind.");
      return;
    }

    if (questionTooLong) {
      setError("Questions must be 1,000 characters or fewer.");
      return;
    }

    if (readyDocuments.length === 0) {
      setError("Upload a PDF and wait for it to be ready before asking questions.");
      return;
    }

    setError("");
    setAnswerLoading(true);

    try {
      const response = await apiFetch<ChatResponse>("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmedQuestion }),
      });
      const noAnswer =
        response.answer === fallbackAnswer || response.sources.length === 0;
      setMessages((current) => [
        ...current,
        {
          id: Date.now(),
          question: trimmedQuestion,
          answer: noAnswer ? noAnswerMessage : response.answer,
          noAnswer,
        },
      ]);
      setQuestion("");
    } catch (err) {
      setError(
        err instanceof TypeError
          ? friendlyError(err)
          : "DocuMind could not generate an answer. Please try again.",
      );
    } finally {
      setAnswerLoading(false);
    }
  }

  return (
    <section className="page">
      <div className="page-header">
        <h1 className="page-title">Chat</h1>
        <p className="page-copy">
          Ask focused questions about PDFs that have finished processing.
        </p>
      </div>

      {loadingDocuments ? (
        <div className="loading-row">
          <span className="spinner" aria-hidden="true" />
          <span>Checking ready documents</span>
        </div>
      ) : readyDocuments.length === 0 ? (
        <div className="empty-state">
          <p>No ready documents yet.</p>
          <Link href="/documents" className="button button-primary mt-4">
            Upload PDFs
          </Link>
        </div>
      ) : null}

      <div className="grid gap-4 lg:grid-cols-[1fr_18rem]">
        <form className="panel space-y-4" onSubmit={askQuestion}>
          <div className="field">
            <label htmlFor="question" className="label">
              Question
            </label>
            <textarea
              id="question"
              rows={5}
              className="input resize-y"
              value={question}
              onChange={(event) => {
                setQuestion(event.target.value);
                setError("");
              }}
              placeholder="What does this document say about renewal terms?"
              aria-describedby="question-help"
            />
            <p id="question-help" className="text-sm text-slate-600">
              {question.length}/{maxQuestionLength} characters
            </p>
            {questionTooLong ? (
              <p className="text-sm text-rose-700">
                Questions must be 1,000 characters or fewer.
              </p>
            ) : null}
          </div>
          <button type="submit" className="button button-primary" disabled={!canAsk}>
            {answerLoading ? "Asking..." : "Ask DocuMind"}
          </button>
          {answerLoading ? (
            <div className="loading-row">
              <span className="spinner" aria-hidden="true" />
              <span>Generating answer</span>
            </div>
          ) : null}
        </form>

        <aside className="space-y-3" aria-label="Chat history">
          {messages.length === 0 ? (
            <div className="empty-state">
              Answers will appear here after you ask a question.
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="panel space-y-3">
                <p className="text-sm font-medium text-slate-500">You asked</p>
                <p className="text-sm leading-6 text-slate-900">
                  {message.question}
                </p>
                <p className="text-sm font-medium text-slate-500">DocuMind answered</p>
                <p
                  className={`text-sm leading-6 ${
                    message.noAnswer ? "text-amber-800" : "text-slate-900"
                  }`}
                >
                  {message.answer}
                </p>
              </div>
            ))
          )}
        </aside>
      </div>

      {error ? <p className="error-message">{error}</p> : null}
    </section>
  );
}
