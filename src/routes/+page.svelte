<script lang="ts">
  import { onMount } from 'svelte';
  import jsPDF from 'jspdf';

  function saveToPDF() {
    const title = (document.getElementById('note-title') as HTMLInputElement)?.innerText || '';
    const date = (document.getElementById('note-date') as HTMLInputElement)?.innerText || '';
    const content = (document.getElementById('note-content') as HTMLInputElement)?.innerText || '';

    const doc = new jsPDF();
    doc.setFont('times', 'normal');

    doc.setFontSize(18);
    doc.text(title || 'Lab Notes', 10, 20);

    doc.setFontSize(12);
    doc.text(`Date: ${date || new Date().toLocaleDateString()}`, 10, 30);

    doc.setFontSize(14);
    doc.text('Content:', 10, 40);

    doc.setFontSize(12);
    doc.text(content || '', 10, 50, { maxWidth: 180 });

    doc.save(`${title || 'labnotes'}.pdf`);
  }

  // Inactivity timeout (5 seconds)
  const WRITE_INACTIVITY_MS = 5000;
  const FADE_MS = 700; // duration of the fade animation before clearing

  // DOM refs / timers
  let typingArea: HTMLDivElement | null = null;
  let inactivityTimer: ReturnType<typeof setTimeout> | null = null;
  let fading = false;
  let noteDate: HTMLDivElement | null = null;
  let prevText = '';

  // Called on each input (typing / paste) in the contenteditable div
  function handleInput(e: Event): void {
    const target = (e.currentTarget ?? e.target) as HTMLDivElement | null;
    if (!target) return;
    const text = (target.innerText ?? '').toString();

    // Cancel fade if the user typed during fade
    if (fading) {
      cancelFade();
    }

    prevText = text;
    resetInactivityTimer();
  }

  // Reset/start the inactivity timer
  function resetInactivityTimer(): void {
    if (inactivityTimer) clearTimeout(inactivityTimer);
    inactivityTimer = setTimeout(() => beginFadeAndClear(), WRITE_INACTIVITY_MS);
  }

  // Begin fade animation and clear after FADE_MS
  function beginFadeAndClear(): void {
    if (fading) return;
    fading = true;
    if (typingArea) typingArea.classList.add('decay-fade');

    setTimeout(() => {
      if (typingArea) {
        typingArea.innerText = '';
        typingArea.classList.remove('decay-fade');
      }
      prevText = '';
      fading = false;
    }, FADE_MS);
  }

  // Cancel a currently active fade (user resumed typing)
  function cancelFade(): void {
    if (inactivityTimer) {
      clearTimeout(inactivityTimer);
      inactivityTimer = null;
    }
    if (typingArea) {
      typingArea.classList.remove('decay-fade');
    }
    fading = false;
  }

  // Small keyboard handler: allow Enter but avoid inserting huge nodes
  function handleKeydown(e: KeyboardEvent): void {
    if (e.key === 'Enter') {
      // Insert a single newline (keeps contenteditable tidy)
      // execCommand is deprecated but works for simple insert; acceptable for prototyping.
      document.execCommand('insertHTML', false, '\n');
      e.preventDefault();
    }
  }

  // Reset button: clear content and timers
  function resetAll(): void {
    if (inactivityTimer) {
      clearTimeout(inactivityTimer);
      inactivityTimer = null;
    }
    if (typingArea) typingArea.innerText = '';
    prevText = '';
    fading = false;
    if (typingArea) typingArea.classList.remove('decay-fade');
  }

  onMount(() => {

// Focus cursor into content area at start
    typingArea?.focus();

    // Auto-fill today's date if the field is empty
    if (noteDate && noteDate.innerText.trim() === "") {
      const today = new Date();
      const formatted = today.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric"
      });
      noteDate.innerText = formatted;
    }

    // start the inactivity timer only when mounted and if there's pre-filled content
    if (typingArea && typingArea.innerText.trim().length > 0) {
      resetInactivityTimer();
    }
    return () => {
      if (inactivityTimer) clearTimeout(inactivityTimer);
    };


  });
</script>

<svelte:head>
  <!-- cursive font for handwriting vibe -->
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap" rel="stylesheet" />
  <title>DecayLog — Lab Report (Write Mode)</title>
</svelte:head>

<div class="app">
  <aside class="panel">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <div>
        <h3>Lab Notebook</h3>
        <div class="muted">Write mode — your text clears after 5s inactivity</div>
      </div>
      <div>
        <button class="btn" on:click={resetAll} aria-label="Reset notes">Reset</button>
      </div>
    </div>

    <div style="margin-top:12px" class="footer-note">
      Tip: keep typing to preserve your notes. Pause for 5 seconds and the page gently fades your text away.
    </div>
  </aside>

  <main class="workbench">
    <div class="grid-paper">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <div>
          <strong style="font-size:18px;">DecayLog — Lab Report</strong>
        </div>
      </div>

    <div class="labnote">
  <div
    id="note-title"
    class="note-title"
    role="textbox"
    contenteditable="true"
    placeholder="Enter title..."
  ></div>

  <div
    id="note-date"
    class="note-date"
    bind:this={noteDate}
    role="textbox"
    contenteditable="true"
    placeholder="Enter date..."
  ></div>

  <div
    id="note-content"
    class="typing-area"
    bind:this={typingArea}
    role="textbox"
    aria-multiline="true"
    tabindex="0"
    contenteditable="true"
    on:input={handleInput}
    on:keydown={handleKeydown}
    placeholder="Begin writing lab notes..."
  ></div>
</div>

<button class="btn" on:click={saveToPDF}>Save as PDF</button>


    </div>
  </main>
</div>
