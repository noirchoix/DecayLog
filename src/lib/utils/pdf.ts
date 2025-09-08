import jsPDF from "jspdf";

/**
 * Save a lab note as PDF.
 */
export function saveToPDF(title: string, date: string, content: string) {
  const doc = new jsPDF();
  doc.setFont("times", "normal");

  doc.setFontSize(18);
  doc.text(title || "Lab Notes", 10, 20);

  doc.setFontSize(12);
  doc.text(`Date: ${date || new Date().toLocaleDateString()}`, 10, 30);

  doc.setFontSize(14);
  doc.text("Content:", 10, 40);

  doc.setFontSize(12);
  doc.text(content || "", 10, 50, { maxWidth: 180 });

  doc.save(`${title || "labnotes"}.pdf`);
}

/**
 * Extracts text content from the lab note for TTS or external use.
 */
export function extractNoteText(
  title: string,
  date: string,
  content: string
): string {
  return `Title: ${title || "Lab Notes"}\nDate: ${
    date || new Date().toLocaleDateString()
  }\n\n${content || ""}`;
}
