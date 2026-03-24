import axios from "axios";

export async function generateSpeechAudio({ text, apiKey, model = "kokoro", voice = "af_bella" }) {
  if (!apiKey) {
    throw new Error("Missing TTS_AI_API_KEY in .env.");
  }

  const trimmed = (text || "").trim();
  if (!trimmed) {
    throw new Error("Text is required for speech generation.");
  }

  const response = await axios.post(
    "https://api.tts.ai/v1/tts/",
    {
      model,
      voice,
      text: trimmed,
      format: "mp3",
    },
    {
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      responseType: "arraybuffer",
      timeout: 60000,
    },
  );

  const dataBuffer = Buffer.from(response.data);
  const contentType = String(response.headers?.["content-type"] || "").toLowerCase();

  const isJsonLike = contentType.includes("application/json") || dataBuffer[0] === 0x7b;
  if (!isJsonLike) {
    return dataBuffer;
  }

  let payload;
  try {
    payload = JSON.parse(dataBuffer.toString("utf-8"));
  } catch {
    throw new Error("TTS.ai returned an invalid response.");
  }

  const resultUrl = payload?.result_url;
  if (!resultUrl) {
    const providerMessage = payload?.error?.message || payload?.error || payload?.message;
    throw new Error(providerMessage || "TTS.ai did not return audio output.");
  }

  const audioResponse = await axios.get(resultUrl, {
    responseType: "arraybuffer",
    timeout: 60000,
  });

  return Buffer.from(audioResponse.data);
}
