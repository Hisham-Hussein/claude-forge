---
name: youtube-transcript
description: Download YouTube video transcripts when user provides a YouTube URL or asks to download/get/fetch a transcript from YouTube. Also use when user wants to transcribe or get captions/subtitles from a YouTube video.
allowed-tools: Bash,Read,Write
---

<objective>
Download and convert YouTube video transcripts to clean, readable text files using yt-dlp.
</objective>

<triggers>
Use this skill when the user:
- Provides a YouTube URL and wants the transcript
- Asks to "download transcript from YouTube"
- Wants to "get captions" or "get subtitles" from a video
- Asks to "transcribe a YouTube video"
- Needs text content from a YouTube video
</triggers>

<quick_start>
1. Check yt-dlp installed: `which yt-dlp`
2. List available subtitles: `yt-dlp --list-subs "URL"`
3. Download subtitles: `yt-dlp --write-auto-sub --skip-download -o "transcript" "URL"`
4. Convert to plain text (see conversion script below)
</quick_start>

<success_criteria>
- yt-dlp is installed or user instructed how to install
- Subtitles downloaded as .vtt file
- Converted to clean .txt file with video title as filename
- Duplicate lines removed from auto-generated captions
- User shown file location and preview
</success_criteria>

<process>
<subtitle_priority>
1. Check available subtitles first (--list-subs)
2. Try manual subtitles (--write-sub) - highest quality
3. Fallback to auto-generated (--write-auto-sub) - usually available
4. Last resort: Whisper transcription (requires user confirmation)
</subtitle_priority>

<download_commands>
Manual subtitles (preferred):
```bash
yt-dlp --write-sub --skip-download --output "OUTPUT_NAME" "YOUTUBE_URL"
```

Auto-generated subtitles (fallback):
```bash
yt-dlp --write-auto-sub --skip-download --output "OUTPUT_NAME" "YOUTUBE_URL"
```

Get video title for filename:
```bash
yt-dlp --print "%(title)s" "YOUTUBE_URL"
```
</download_commands>

<vtt_to_text_conversion>
YouTube auto-generated VTT files contain duplicate lines due to progressive caption display. Always deduplicate:

```bash
python3 -c "
import sys, re
seen = set()
with open('transcript.en.vtt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > transcript.txt
```
</vtt_to_text_conversion>
</process>

<installation>
<check>
```bash
which yt-dlp || command -v yt-dlp
```
</check>

<install_methods>
macOS (Homebrew):
```bash
brew install yt-dlp
```

Linux (apt):
```bash
sudo apt update && sudo apt install -y yt-dlp
```

Any system (pip):
```bash
pip3 install yt-dlp
```
</install_methods>

If installation fails, direct user to: https://github.com/yt-dlp/yt-dlp#installation
</installation>

<reference>
<complete_workflow>
```bash
VIDEO_URL="https://www.youtube.com/watch?v=VIDEO_ID"

# Get video title for filename
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$VIDEO_URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '')
OUTPUT_NAME="transcript_temp"

# Check yt-dlp installed
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp not found, attempting to install..."
    if command -v brew &> /dev/null; then
        brew install yt-dlp
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y yt-dlp
    else
        pip3 install yt-dlp
    fi
fi

# Check available subtitles
echo "Checking available subtitles..."
yt-dlp --list-subs "$VIDEO_URL"

# Try manual subtitles first
echo "Attempting manual subtitles..."
if yt-dlp --write-sub --skip-download --output "$OUTPUT_NAME" "$VIDEO_URL" 2>/dev/null; then
    echo "Manual subtitles downloaded!"
else
    # Fallback to auto-generated
    echo "Trying auto-generated subtitles..."
    yt-dlp --write-auto-sub --skip-download --output "$OUTPUT_NAME" "$VIDEO_URL"
fi

# Convert to plain text with deduplication
VTT_FILE=$(ls ${OUTPUT_NAME}*.vtt 2>/dev/null | head -n 1)
if [ -f "$VTT_FILE" ]; then
    python3 -c "
import sys, re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > "${VIDEO_TITLE}.txt"
    rm "$VTT_FILE"
    echo "Saved to: ${VIDEO_TITLE}.txt"
fi
```
</complete_workflow>

<whisper_fallback>
Only use if no subtitles available. Requires user confirmation due to download size.

Check file size first:
```bash
yt-dlp --print "%(filesize,filesize_approx)s" -f "bestaudio" "YOUTUBE_URL"
```

Check Whisper installed:
```bash
command -v whisper
```

Install if needed:
```bash
pip3 install openai-whisper
```

Download and transcribe:
```bash
# Download audio
yt-dlp -x --audio-format mp3 --output "audio_%(id)s.%(ext)s" "YOUTUBE_URL"

# Transcribe (use base model for balance of speed/accuracy)
whisper audio_VIDEO_ID.mp3 --model base --output_format vtt

# Clean up audio after
rm audio_VIDEO_ID.mp3
```

Model options: tiny (~1GB), base (~1GB, recommended), small (~2GB), medium (~5GB), large (~10GB)
</whisper_fallback>
</reference>

<troubleshooting>
<no_subtitles>
If --list-subs shows no subtitles:
1. Try both --write-sub and --write-auto-sub
2. If both fail, offer Whisper transcription with file size warning
3. Wait for user confirmation before downloading audio
</no_subtitles>

<invalid_video>
- Verify URL format: https://www.youtube.com/watch?v=VIDEO_ID
- Video may be private, age-restricted, or geo-blocked
- Show specific error from yt-dlp to user
</invalid_video>

<installation_fails>
- May require system dependencies
- Try alternative install method (brew → apt → pip)
- Provide manual installation link as fallback
</installation_fails>

<multiple_languages>
- Default downloads all available languages
- Specify language: `--sub-langs en` for English only
- List available with `--list-subs` first
</multiple_languages>
</troubleshooting>

<best_practices>
- Always check available subtitles before download (--list-subs)
- Verify success at each step before proceeding
- Ask user before large downloads (audio files, Whisper models)
- Clean up temporary files (VTT after conversion, audio after transcription)
- Provide clear feedback about progress
- Use video title for meaningful filenames
</best_practices>
