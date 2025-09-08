  # DecayLog — Lab Notes App

  DecayLog is a playful, chemistry-inspired writing tool designed for **lab reports and note-taking**.
  If you stop typing for more than **5 seconds**, your text will begin to **fade away and disappear** — simulating decay.

  It combines the feel of a **notebook page** with structured lab note fields (title, date, and content). Users can also **export their notes to PDF** for safekeeping before decay erases them.

  ---

  ## ✨ Features

  * 🧪 **Notebook-style UI** with darker ruled lines for a lab journal feel.
  * ⏳ **Decay mechanic**: Inactivity for 5 seconds clears your text.
  * 📅 **Auto-date insertion**: Fills in today’s date by default, editable by the user.
  * 💾 **Save to PDF**: Export your notes (title, date, and content) in fixed lab-report format.
  * 🎨 **Minimal, focused workspace** built with [SvelteKit](https://kit.svelte.dev).

  ---

  ## 🚀 Getting Started

  ### Prerequisites

  * [Node.js](https://nodejs.org/) (v16+ recommended)
  * [npm](https://www.npmjs.com/) or [pnpm](https://pnpm.io/)

  ### Installation

  ```bash
  # Clone the repo
  git clone https://github.com/your-username/decaylog.git
  cd decaylog

  # Install dependencies
  npm install

  # Start development server
  npm run dev
  ```

  Then visit [http://localhost:5173](http://localhost:5173).

  ---

  ## 🗂 Project Structure

  ```
  decaylog/
  ├── src/
  │   ├── routes/
  │   │   └── +page.svelte   # Main Lab Notes page
  │   ├── app.css            # Styles (notebook lines, fade effect, etc.)
  │   └── lib/               # (optional future utilities)
  ├── static/                # Static assets
  ├── package.json
  └── README.md
  ```

  ---

  ## 📄 Usage

  1. Start typing in the **title**, **date**, or **content** fields.
  2. Stay active — if you pause typing for more than 5s, your content fades away.
  3. When ready, click **Save as PDF** to export your notes.
  4. Keep experimenting!

  ---

  ## 🛠 Tech Stack

  * [SvelteKit](https://kit.svelte.dev) — Frontend framework
  * [TypeScript](https://www.typescriptlang.org/) — Type safety
  * [CSS Grid / Flexbox](https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout) — Notebook styling
  * [pdf-lib](https://pdf-lib.js.org/) or [jsPDF](https://github.com/parallax/jsPDF) (planned) — PDF export

  ---

  ## 📌 Roadmap

  * [ ] Improve PDF export styling (headers, page breaks, signatures).
  * [ ] Add persistent local storage (drafts don’t vanish on refresh).
  * [ ] Optional "gamified chemistry mode" with activation-energy typing.
  * [ ] Theming support (dark mode, parchment mode).# DecayLog — Lab Notes App

DecayLog is an experimental **lab notes and report-writing tool** with a chemistry-inspired twist. It now supports **voice and audio features** alongside the original decay mechanic.

If you stop typing for more than **5 seconds**, your text will still **fade away and disappear**, but you can now also **convert text or entire PDFs into audio narration** for playback.

---

## ✨ Features

* 🧪 **Notebook-style UI** with a lab journal aesthetic.
* ⏳ **Decay mechanic**: Inactivity clears your text after 5 seconds.
* 📅 **Auto-date insertion**: Defaults to today’s date, editable.
* 💾 **Export to PDF**: Save your lab notes with proper formatting.
* 🔊 **Text-to-Speech**: Convert notes or PDFs into spoken audio.
* 📂 **Multi-page PDF handling**: Splits long documents into page-by-page audio.
* 🎨 **Minimal, focused workspace** powered by [SvelteKit](https://kit.svelte.dev).

---

## 🚀 Getting Started

### Prerequisites

* [Node.js](https://nodejs.org/) (v16+ recommended)
* [npm](https://www.npmjs.com/) or [pnpm](https://pnpm.io/)
* [Python 3](https://www.python.org/) with [FastAPI](https://fastapi.tiangolo.com) backend

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/decaylog.git
cd decaylog

# Install frontend dependencies
npm install

# Start both frontend and backend
dev: npm run dev
```

Then visit [http://localhost:5173](http://localhost:5173).

---

## 🗂 Project Structure

```
decaylog/
├── src/
│   ├── routes/
│   │   └── +page.svelte   # Main Lab Notes page
│   ├── lib/audio.ts       # Audio handling (TTS client)
│   └── app.css            # Notebook and fade styles
├── server.py              # FastAPI backend (text/PDF → audio)
├── static/                # Exported PDFs & MP3s
├── package.json
└── README.md
```

---

## 📄 Usage

1. Type in the **title**, **date**, or **content** fields.
2. Stay active — pause typing for 5s and your notes will fade away.
3. Use **Save as PDF** to export your work.
4. Or use **Convert to Audio** to listen to your notes or uploaded PDFs.

---

## 🛠 Tech Stack

* [SvelteKit](https://kit.svelte.dev) — Frontend
* [TypeScript](https://www.typescriptlang.org/) — Type safety
* [FastAPI](https://fastapi.tiangolo.com) — Backend API
* [gTTS](https://pypi.org/project/gTTS/) + [pydub](https://github.com/jiaaro/pydub) — Text-to-Speech & audio handling
* [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction

---

## 📌 Roadmap

* [ ] Improve voice selection (multiple accents, neutral English).
* [ ] Smarter chunking for long text-to-speech.
* [ ] Persistent local storage (notes survive refresh).
* [ ] Advanced PDF export with lab report styling.
* [ ] Theming support (dark mode, parchment mode).
* [ ] PDF => WORD

---

## 🤝 Contributing

Contributions are welcome! Fork the repo and open a PR with improvements.

---

## 📜 License

MIT License © 2025 \Dickson Samuel


  ---

  ## 🤝 Contributing

  Contributions are welcome! Fork the repo and open a PR with improvements.

  ---

  ## 📜 License

  MIT License © 2025 \Dickson Samuel
