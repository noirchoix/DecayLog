export async function textToAudio(content: string): Promise<void> {
  const formData = new FormData();
  formData.append("content", content);

  const response = await fetch("http://127.0.0.1:8000/text-to-audio", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  const blob = await response.blob();
  playBlob(blob);
}

export async function pdfToAudio(file: File, merge: boolean = true): Promise<void> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("merge", String(merge));

  const response = await fetch("http://127.0.0.1:8000/pdf-to-audio", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }

  const data = await response.json();

  if (data.mode === "merged") {
    playFromUrl(`http://127.0.0.1:8000${data.url}`);
  } else if (data.mode === "split") {
    // play each file sequentially
    for (const fileUrl of data.files) {
      await playSequentially(`http://127.0.0.1:8000${fileUrl}`);
    }
  }
}

function playBlob(blob: Blob) {
  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);
  audio.play();
  audio.onended = () => {
    URL.revokeObjectURL(url);
  };
}

function playFromUrl(url: string) {
  const audio = new Audio(url);
  audio.play();
}

function playSequentially(url: string): Promise<void> {
  return new Promise((resolve) => {
    const audio = new Audio(url);
    audio.play();
    audio.onended = () => resolve();
  });
}
