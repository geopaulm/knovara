def pdf_with_text(*texts: str) -> bytes:
    objects = [
        None,
        b"<< /Type /Catalog /Pages 2 0 R >>",
        None,
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    page_ids = []
    for text in texts:
        page_id = len(objects)
        content_id = page_id + 1
        stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
        objects.extend(
            [
                f"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 3 0 R >> >> /MediaBox [0 0 612 792] /Contents {content_id} 0 R >>".encode(),
                b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
            ]
        )
        page_ids.append(page_id)
    objects[2] = (
        b"<< /Type /Pages /Kids ["
        + b" ".join(f"{page_id} 0 R".encode() for page_id in page_ids)
        + b"] /Count "
        + str(len(page_ids)).encode()
        + b" >>"
    )

    parts = [b"%PDF-1.4\n"]
    offsets = [0]
    for object_id, value in enumerate(objects[1:], start=1):
        offsets.append(sum(len(part) for part in parts))
        parts.append(f"{object_id} 0 obj\n".encode() + value + b"\nendobj\n")
    xref_at = sum(len(part) for part in parts)
    parts.append(f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode())
    parts.extend(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:])
    parts.append(f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref_at}\n%%EOF\n".encode())
    return b"".join(parts)
