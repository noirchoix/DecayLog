<script lang="ts">
  import { onMount } from "svelte";

  let audioFiles: string[] = [];
  let selectedFile: File | null = null;
  let audioUrl: string | null = null;
  let loading = false;
  let error: string | null = null;
  let selectedWord: File | null = null;
  let mergeMode = "merged"; // "merged" or "split"



  async function convertWord() {
    if (!selectedWord) return;

    const formData = new FormData();
    formData.append("file", selectedWord);

    const res = await fetch("http://localhost:8000/word-to-pdf", {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = selectedWord.name.replace(".docx", ".pdf");
      a.click();
      URL.revokeObjectURL(url);
    }
  }

  function deleteAudio() {
    if (audioUrl) {
      URL.revokeObjectURL(audioUrl); // free memory
      audioUrl = null;
      audioFiles = [];
    }
  }


  function handleWordChange(e: Event) {
    const target = e.target as HTMLInputElement | null;
    if (target?.files && target.files.length > 0) {
      selectedWord = target.files[0];
    }
  }
  async function handleFileUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target?.files && target.files.length > 0) {
      selectedFile = target.files[0];
      error = null;
    } else {
      selectedFile = null;
      error = "No file selected.";}
  }

   async function convertToAudio() {
    if (!selectedFile) return;
    loading = true;
    error = null;
    audioUrl = null;
    audioFiles = [];

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);
      formData.append("merge", mergeMode === "merged" ? "true" : "false");

      const res = await fetch("http://localhost:8000/pdf-to-audio", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (data.error) {
        error = data.error;
      } else if (data.mode === "merged") {
        audioUrl = "http://localhost:8000" + data.url;
      } else if (data.mode === "split") {
        audioFiles = data.files.map((f: string) => "http://localhost:8000" + f);
      }
    } catch (err) {
      error = "Failed to convert PDF to audio.";
    } finally {
      loading = false;
    }
  }
</script>

<div class="app">
  <!-- Instruction panel -->
  <aside class="panel mb-6">
    <div class="flex justify-between items-center">
      <nav class="text-sm">
        <a href="/" class="text-blue-600 hover:underline">← Back to Lab Notes</a>
      </nav>
    </div>

    <div>
      <h3 class="text-lg font-semibold">Lab AudioHub</h3>
      <div class="muted">
        Convert files into accessible formats — PDF → Audio or Word → PDF.
      </div>
    </div>

  <br/>
  <br/>

<!-- Word → PDF Section -->
  <section class="mt-10 space-y-4">
    <h4 class="text-md font-semibold">Word → PDF</h4>

    <input
      type="file"
      accept=".docx"
      on:change={handleWordChange}
      class="block w-full border p-2 rounded"
    />

    <div class="text-sm text-gray-500 italic">
      {#if selectedWord}
        Selected Word file: <span class="font-medium">{selectedWord.name}</span>
      {:else}
        No Word file selected yet — please choose a .docx file to continue.
      {/if}
    </div>

    <button
      on:click={convertWord}
      class="px-4 py-2 bg-blue-600 text-white rounded"
      disabled={!selectedWord}
    >
      Convert Word → PDF
    </button>
  </section>

  </aside>

  <!-- PDF → Audio Section -->
  <section class="mt-6 space-y-4">
    <h4 class="text-md font-semibold">PDF → Audio</h4>
    <input
      type="file"
      accept="application/pdf"
      on:change={handleFileUpload}
      class="block w-full border p-2 rounded"
    />

    <!-- Mode selector -->
    <div class="flex space-x-4 items-center">
      <label class="flex items-center space-x-2">
        <input type="radio" bind:group={mergeMode} value="merged" />
        <span>Single file (merged)</span>
      </label>
      <label class="flex items-center space-x-2">
        <input type="radio" bind:group={mergeMode} value="split" />
        <span>Split per page</span>
      </label>
    </div>

    <button
      class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      on:click={convertToAudio}
      disabled={loading || !selectedFile}
    >
      {loading ? "Converting..." : "Convert to Audio"}
    </button>

    {#if error}
      <p class="text-red-600">{error}</p>
    {/if}

    <!-- Preview merged audio -->
    {#if audioUrl}
      <div class="mt-6">
        <h2 class="text-lg font-semibold">Preview (Merged)</h2>
        <audio controls src={audioUrl} class="mt-2 w-full"></audio>

        <a
          href={audioUrl}
          download="converted_audio.mp3"
          class="mt-4 inline-block bg-green-600 text-white px-4 py-2 rounded"
        >
          Download MP3
        </a>

        <button
          on:click={deleteAudio}
          class="ml-4 inline-block bg-red-600 text-white px-4 py-2 rounded"
        >
          Delete
        </button>
      </div>
    {/if}

    <!-- Preview split audios -->
    {#if audioFiles.length > 0}
      <div class="mt-6">
        <h2 class="text-lg font-semibold">Preview (Split per Page)</h2>
        {#each audioFiles as url, i}
          <div class="mb-4">
            <p class="font-medium">Page {i + 1}</p>
            <audio controls src={url} class="mt-2 w-full"></audio>
            <a
              href={url}
              download="page_{i+1}.mp3"
              class="mt-2 inline-block bg-green-600 text-white px-3 py-1 rounded"
            >
              Download
            </a>
          </div>
        {/each}

        <button
          on:click={deleteAudio}
          class="mt-4 inline-block bg-red-600 text-white px-4 py-2 rounded"
        >
          Delete All
        </button>
      </div>
    {/if}
</section>
</div>
