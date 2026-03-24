import axios from "axios";
import { normalizeLanguageCode } from "./language.js";

export async function translateText({ text, sourceLang, targetLang }) {
  const from = normalizeLanguageCode(sourceLang);
  const to = normalizeLanguageCode(targetLang);

  const response = await axios.get("https://translate.googleapis.com/translate_a/single", {
    params: {
      client: "gtx",
      sl: from,
      tl: to,
      dt: "t",
      q: text,
    },
    timeout: 15000,
  });

  const chunks = response.data?.[0];
  if (!Array.isArray(chunks)) {
    throw new Error("Unexpected translation response format.");
  }

  return {
    translation: chunks.map((item) => item?.[0] || "").join("").trim(),
    sourceLang: from,
    targetLang: to,
  };
}

export async function translateTagalogToIlokano(text) {
  return translateText({ text, sourceLang: "tl", targetLang: "ilo" });
}
