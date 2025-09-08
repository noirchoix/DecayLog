let inactivityTimer: ReturnType<typeof setTimeout> | null = null;
let fading = false;
let prevText = "";

const WRITE_INACTIVITY_MS = 15000;
const FADE_MS = 700;

/**
 * Reset/start the inactivity timer.
 */
export function resetInactivityTimer(typingArea: HTMLDivElement) {
  if (inactivityTimer) clearTimeout(inactivityTimer);
  inactivityTimer = setTimeout(
    () => beginFadeAndClear(typingArea),
    WRITE_INACTIVITY_MS
  );
}

/**
 * Begin fade animation and clear after FADE_MS.
 */
export function beginFadeAndClear(typingArea: HTMLDivElement) {
  if (fading) return;
  fading = true;
  typingArea.classList.add("decay-fade");

  setTimeout(() => {
    typingArea.innerText = "";
    typingArea.classList.remove("decay-fade");
    prevText = "";
    fading = false;
  }, FADE_MS);
}

/**
 * Cancel a currently active fade (user resumed typing).
 */
export function cancelFade(typingArea: HTMLDivElement) {
  if (inactivityTimer) {
    clearTimeout(inactivityTimer);
    inactivityTimer = null;
  }
  typingArea.classList.remove("decay-fade");
  fading = false;
}

/**
 * Handle typing input.
 */
export function handleInput(e: Event, typingArea: HTMLDivElement) {
  const text = (typingArea.innerText ?? "").toString();

  if (fading) {
    cancelFade(typingArea);
  }

  prevText = text;
  resetInactivityTimer(typingArea);
}

/**
 * Keyboard handler: allow Enter but avoid inserting big DOM nodes.
 */
export function handleKeydown(e: KeyboardEvent) {
  if (e.key === "Enter") {
    document.execCommand("insertHTML", false, "\n"); // prototyping ok
    e.preventDefault();
  }
}

/**
 * Reset the note.
 */
export function resetAll(typingArea: HTMLDivElement) {
  if (inactivityTimer) {
    clearTimeout(inactivityTimer);
    inactivityTimer = null;
  }
  typingArea.innerText = "";
  prevText = "";
  fading = false;
  typingArea.classList.remove("decay-fade");
}
