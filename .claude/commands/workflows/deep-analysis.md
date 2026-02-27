# Deep Analysis Workflow

> Comprehensive analysis of folders with mixed content (documents, audio, video, images)

## Usage

```
/Custom:deep-analysis [path]
```

## What This Workflow Does

1. **Scans** the folder to inventory all files
2. **Estimates** processing costs (free vs paid options)
3. **Processes** all content:
   - Documents (PDF, Word, Excel, PowerPoint)
   - Audio files (transcription)
   - Video files (extract audio + transcribe)
   - Images (OCR + description)
   - Web links (fetch content)
4. **Consolidates** all extracted content
5. **Generates** summary and key topics
6. **Creates** actionable brief
7. **Hands off** to development or marketing

## Workflow Steps

### Step 1: Load Analyst Agent

```
/analyst
```

### Step 2: Run Deep Scan

```
*deep-scan {path}
```

This will:
- Scan all files in the folder
- Show inventory with file counts and sizes
- Estimate API costs
- Ask user to choose processing level

### Step 3: Process Content

Based on user choice:
- **Quick (FREE):** Documents + YouTube + OCR only
- **Full (PAID):** All content including Whisper API + GPT-4 Vision

### Step 4: Generate Brief

```
*generate-brief {type}
```

Types:
- `development` - PRD-ready brief
- `marketing` - Campaign brief
- `research` - Research summary
- `general` - Overview

### Step 5: Handoff (Optional)

```
*to-development    # Generates PRD + architecture
*to-marketing      # Generates campaign brief
```

## Output Files

All outputs go to `docs/analysis/`:

```
docs/analysis/
├── {session}-inventory.json    # File inventory
├── {session}-findings.md       # Extracted content
├── {session}-summary.md        # Executive summary
├── {session}-topics.json       # Key topics
└── {session}-brief-{type}.md   # Project brief
```

## Cost Tiers

### FREE Options
- All document parsing (PDF, Word, Excel, PowerPoint)
- YouTube/Vimeo transcript extraction
- Tesseract OCR for images
- Local Whisper transcription (slower)

### PAID Options
- Whisper API: $0.006/minute audio
- GPT-4 Vision: $0.01-0.03/image

## Requirements

### System Dependencies

```bash
# macOS
brew install tesseract tesseract-lang ffmpeg

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-spa ffmpeg
```

### API Keys (for PAID options)

```bash
export OPENAI_API_KEY="sk-..."
```

## Example Usage

### Analyze Client Documentation

```
/Custom:deep-analysis ~/Documents/ClientProject

# Or step by step:
/analyst
*deep-scan ~/Documents/ClientProject
*generate-brief development
*to-development
```

### Analyze Research Materials

```
/analyst
*deep-scan ~/Research/MarketStudy
*generate-brief research
```

### Analyze Marketing Assets

```
/analyst
*deep-scan ~/Marketing/Campaign2026
*generate-brief marketing
*to-marketing
```

## Supported Formats

| Category | Formats |
|----------|---------|
| Documents | PDF, DOCX, XLSX, PPTX, CSV, JSON, TXT, MD |
| Audio | MP3, WAV, M4A, OGG, FLAC, AAC |
| Video | MP4, MOV, AVI, MKV, WebM |
| Images | JPG, PNG, GIF, BMP, TIFF, WebP |
| Archives | ZIP, TAR, GZ, RAR, 7Z |
| Web | YouTube, Vimeo, any URL |

## MCP Server

This workflow uses the `analysis-server` MCP with 48 tools.

See: `mcp-servers/analysis-server/README.md`
