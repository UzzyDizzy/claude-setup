---
name: document-processing
description: Automatically use Marker to convert PDFs and other supported documents into high-quality Markdown before analysis. Trigger whenever working with PDFs, scanned documents, Word, PowerPoint, Excel, EPUB, HTML, or images.
---

# Document Processing

## Goal

Always use Marker as the default document ingestion pipeline instead of attempting to directly read PDFs or using lightweight OCR/text extraction libraries.

Supported document types include:

- PDF
- Images
- DOCX
- PPTX
- XLSX
- HTML
- EPUB

Preferred output formats:

1. Markdown
2. JSON (when structured data is useful)
3. HTML (only when layout preservation is specifically needed)

---

## Why Marker

Marker provides significantly better document understanding than traditional PDF parsers and OCR.

It preserves:

- headings
- document hierarchy
- tables
- equations
- code blocks
- references
- hyperlinks
- figures
- captions
- lists

It removes:

- headers
- footers
- page artifacts
- duplicated text

Always prefer Marker whenever it supports the input document.

---

## Cross-platform Compatibility

This skill must work on:

- Linux
- Windows
- macOS

Never assume Bash.

Use commands compatible with the user's operating system.

Preferred execution order:

```
python -m marker
```

If unavailable:

```
python3 -m marker
```

If unavailable (Windows):

```
py -m marker
```

---

## Verify Installation

Before converting a document, verify Marker is available.

Try in this order:

```
marker_single --help
```

then

```
python -m marker --help
```

then

```
python3 -m marker --help
```

then

```
py -m marker --help
```

Only install Marker if none of the above succeed.

Install using:

```
pip install marker-pdf
```

or

```
uv pip install marker-pdf
```

If installation issues occur due to package versions:

```
pip install git+https://github.com/datalab-to/marker.git
```

Never reinstall Marker if it is already available.

---

## Output Directory

For every input document:

```
<filename>.<extension>
```

always create:

```
<filename>_md/
```

Example:

```
paper.pdf
```

↓

```
paper_md/
    paper.md
    paper.json
    images/
```

Example:

```
report.pdf
```

↓

```
report_md/
    report.md
    report.json
    images/
```

Example:

```
slides.pptx
```

↓

```
slides_md/
    slides.md
    slides.json
    images/
```

Rules:

- Create the directory if it does not exist.
- Never write generated files into the current working directory.
- Never mix outputs from multiple documents.
- Reuse the existing `<filename>_md` directory if the source document has not changed.
- Overwrite only generated outputs when reconverting.

---

## Default Workflow

Whenever the user provides one or more supported documents:

1. Detect the file type.
2. Verify Marker is installed.
3. Convert every document into its own `<filename>_md/` directory.
4. Read the generated Markdown.
5. Perform all downstream reasoning from the Markdown.
6. Never analyze the original PDF after successful conversion.

Example:

```
paper.pdf
```

↓

```
paper_md/
    paper.md
```

All summaries, question answering, extraction, searching, chunking, embeddings, RAG pipelines, and analysis should use:

```
paper_md/paper.md
```

instead of reopening the PDF.

---

## Preferred Output

General document understanding:

```
Markdown
```

Structured extraction:

```
JSON
```

Layout-sensitive applications:

```
HTML
```

---

## Images

If image extraction is enabled:

- preserve extracted figures
- preserve captions
- preserve Markdown image references

Never discard extracted figures unless explicitly requested.

---

## Tables

Always preserve table structure.

Never flatten tables into plain text unless explicitly requested.

---

## Equations

Preserve equations as LaTeX whenever possible.

Never OCR mathematical expressions into plain text.

---

## OCR

If the document is scanned:

- enable OCR
- preserve layout
- preserve tables
- preserve equations
- preserve figures

---

## Batch Processing

If multiple documents are supplied:

Convert every document first.

Example:

```
paper1.pdf
paper2.pdf
notes.docx
```

↓

```
paper1_md/
paper2_md/
notes_md/
```

Only begin analysis after every conversion finishes successfully.

---

## Large Documents

For books, theses, manuals, or large reports:

- convert once
- reuse the generated Markdown
- never reconvert unless the source document changes

---

## Error Handling

If Marker fails:

1. retry once
2. verify Marker installation
3. verify Python environment
4. report the exact error

Do not silently fall back to poor-quality OCR or basic PDF parsers.

---

## Performance

Prefer GPU acceleration if available.

Otherwise:

- CPU execution is acceptable.
- Apple Silicon should use MPS automatically.

---

## Best Practices

Always:

- convert before analysis
- preserve headings
- preserve hierarchy
- preserve tables
- preserve equations
- preserve figures
- preserve captions
- preserve hyperlinks
- analyze Markdown instead of PDFs
- keep every document inside its own `<filename>_md` directory

Avoid:

- PyPDF text extraction
- pdfplumber-only parsing
- OCR-only workflows
- manual PDF parsing
- reading raw PDFs after conversion

Marker should always be the default document ingestion pipeline whenever it supports the supplied document type.