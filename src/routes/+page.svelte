<script lang="ts">
  import { onMount } from 'svelte';
  import { saveToPDF, extractNoteText } from "$lib/utils/pdf";
  import {
    handleInput,
    handleKeydown,
    resetAll,
    resetInactivityTimer,
  } from "$lib/utils/editor";
  import { textToAudio } from '$lib/utils/audio';

  let typingArea: HTMLDivElement;
  let noteDate: HTMLDivElement;

  function handleSave() {
    const title = (document.getElementById("note-title") as HTMLDivElement)
      ?.innerText;
    const date = (document.getElementById("note-date") as HTMLDivElement)
      ?.innerText;
    const content = typingArea?.innerText || "";

    saveToPDF(title || "", date || "", content || "");
  }

  function handleListen() {
    const title = (document.getElementById("note-title") as HTMLDivElement)
      ?.innerText;
    const date = (document.getElementById("note-date") as HTMLDivElement)
      ?.innerText;
    const content = typingArea?.innerText || "";

    const fullText = extractNoteText(title || "", date || "", content || "");
    // call audio API here with fullText
    textToAudio(fullText);
  }

  onMount(() => {
    typingArea?.focus();

    if (noteDate && noteDate.innerText.trim() === "") {
      const today = new Date();
      const formatted = today.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
      });
      noteDate.innerText = formatted;
    }

    if (typingArea && typingArea.innerText.trim().length > 0) {
      resetInactivityTimer(typingArea);
    }
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
        <button class="btn"  on:click={() => resetAll(typingArea)} aria-label="Reset notes"> ♻️ Reset</button>
      </div>
    </div>

    <div style="margin-top:12px" class="footer-note">
      Tip: keep typing to preserve your notes. Pause for 5 seconds and the page gently fades your text away.
    </div>
    <a href="/upload" class="text-blue-600 hover:underline">PDF → Audio</a>
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
    on:input={(e) => handleInput(e, typingArea)}
    on:keydown={handleKeydown}
    placeholder="Begin writing lab notes..."
  ></div>
</div>

<button class="btn" on:click={handleSave}>💾 Save as PDF</button>
<button on:click={handleListen}>🔊 Listen</button>


    </div>
  </main>
</div>
