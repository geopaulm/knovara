# Knovara Frontend Plan

This plan breaks the Knovara frontend into implementation milestones. Each milestone should leave the UI in a working or demonstrable state and build toward the success criteria in `frontend_requirements.txt`.

## Milestone 1: Frontend Project Foundation

### Goals

- Create the Next.js frontend application structure.
- Add TypeScript and Tailwind CSS.
- Establish shared configuration for backend API access.
- Provide a simple, responsive application shell.

### Deliverables

- Next.js app with TypeScript.
- Tailwind CSS configuration.
- Environment variable support for `NEXT_PUBLIC_API_BASE_URL`.
- Basic layout with navigation links for:
  - Home
  - Documents
  - Chat
- Shared API client using Fetch API or Axios.
- Initial README notes for running the frontend locally.

### Completion Criteria

- The frontend starts locally.
- The app renders without runtime errors.
- Navigation works across the main pages.
- Backend base URL is read from an environment variable.

## Milestone 2: Visual Design and Application Shell

### Goals

- Create a clean, screenshot-ready interface suitable for a portfolio demo.
- Ensure the core layout works on desktop, tablet, and mobile.

### Deliverables

- Responsive page container and navigation.
- Consistent button, input, status badge, loading, and empty-state styles.
- Friendly error message pattern.
- Mobile-friendly navigation behavior.
- Basic accessible labels and focus states.

### Completion Criteria

- The UI is readable and usable at common desktop, tablet, and mobile widths.
- Shared UI patterns are consistent across pages.
- Empty, loading, success, and error states have clear visual treatment.

## Milestone 3: Home Page

### Goals

- Explain Knovara quickly and provide clear paths into the product workflow.
- Make the first screen polished enough for portfolio screenshots.

### Deliverables

- Product name and concise description.
- Primary action linking to the chat page.
- Secondary action linking to the documents page.
- Feature highlights:
  - Upload PDFs
  - Ask questions
  - Get answers with sources

### Completion Criteria

- A visitor understands what Knovara does from the home page.
- Primary and secondary buttons navigate to the correct pages.
- Feature highlights are visible without making the page feel cluttered.

## Milestone 4: Documents Page and Document API Integration

### Goals

- Allow users to upload PDFs and manage uploaded documents.
- Display document processing status clearly.

### Deliverables

- `GET /api/documents` integration for listing documents.
- `POST /api/documents` integration for PDF uploads.
- `DELETE /api/documents/{id}` integration for deletion.
- Upload button.
- Drag-and-drop upload area.
- Document list with document name and status.
- Status badges for:
  - `Uploaded`
  - `Processing`
  - `Ready`
  - `Failed`
- Delete action for each document.
- Loading states for list loading, upload, and delete.
- Error messages for upload failure, unsupported file type, backend connection failure, and processing failure.

### Completion Criteria

- A user can upload a PDF from the documents page.
- Non-PDF files are rejected before upload with a friendly message.
- Uploaded documents appear in the list.
- Each document shows its current processing status.
- A user can delete a document and see the list update.

## Milestone 5: Chat Page Structure

### Goals

- Provide a focused question-and-answer workflow.
- Handle the case where no documents are ready.

### Deliverables

- Question input box.
- Submit button.
- Local chat message state.
- Empty state when no ready documents are available.
- Disabled submit state when the question is empty or an answer is loading.
- Question validation:
  - Required question text.
  - Maximum 1,000 characters.
- Friendly validation message for empty submissions.

### Completion Criteria

- The chat page lets users type a question.
- Empty and over-limit questions are blocked with clear feedback.
- The page directs users to upload documents when no ready documents are available.
- The chat layout remains usable on desktop, tablet, and mobile.

## Milestone 6: Chat API Integration and Answer Display

### Goals

- Connect the chat UI to the backend question-answering endpoint.
- Display answers and clear loading/error states.

### Deliverables

- `POST /api/chat` integration.
- Loading state while an answer is generated.
- Answer display area.
- Local chat history for the current page session.
- Error handling for backend connection failure.
- Friendly no-answer message, such as:
  - "The uploaded documents do not contain enough information to answer this question."

### Completion Criteria

- A user can submit a question and receive an answer.
- The submit button is disabled while an answer is being generated.
- API errors are shown in a friendly way.
- No-answer responses are easy to distinguish from system errors.

## Milestone 7: Source Citations

### Goals

- Make answers auditable by showing the document sources used by the backend.
- Support concise citation display with expandable excerpts.

### Deliverables

- Citation list below each answer.
- Citation fields:
  - Document name
  - Page number, where available
  - Relevant text excerpt
- Expand/collapse control for longer excerpts.
- Empty citation handling when no sources are returned.

### Completion Criteria

- Each answer can show its source citations.
- Users can expand longer excerpts without disrupting the chat layout.
- Citations remain readable on mobile screens.

## Milestone 8: Frontend Hardening and Demo Readiness

### Goals

- Polish the MVP for local demos, screenshots, and portfolio presentation.
- Verify core workflows against the frontend requirements.

### Deliverables

- End-to-end manual test pass for:
  - Opening the application
  - Uploading a PDF
  - Viewing document status
  - Asking a question
  - Viewing an answer
  - Viewing source citations
- Basic component or integration tests for high-risk UI behavior, if a test setup is added.
- Final responsive review across desktop, tablet, and mobile.
- README updates for frontend setup and environment variables.
- Scope review against the out-of-scope list.

### Completion Criteria

- The frontend can be started from a clean checkout using documented steps.
- The main workflow is usable without hidden setup knowledge.
- The UI is polished enough for Upwork, GitHub, and portfolio screenshots.
- Out-of-scope MVP features are not included.

## Frontend Acceptance Checklist

- The application has Home, Documents, and Chat pages.
- Navigation works between all main pages.
- The backend base URL is configured through `NEXT_PUBLIC_API_BASE_URL`.
- A user can upload a PDF.
- A user can see uploaded documents and processing status.
- A user can delete a document.
- A user can ask a question about ready documents.
- The app displays loading states during upload, deletion, list loading, and answer generation.
- The app displays friendly validation and error messages.
- The app displays AI-generated answers with source citations.
- Longer source excerpts can be expanded and collapsed.
- The UI works well on desktop, tablet, and mobile.
- The frontend is suitable for portfolio screenshots.
