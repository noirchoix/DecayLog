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
* [ ] Theming support (dark mode, parchment mode).

---

## 🤝 Contributing

Contributions are welcome! Fork the repo and open a PR with improvements.

---

## 📜 License

MIT License © 2025 \Dickson Samuel
