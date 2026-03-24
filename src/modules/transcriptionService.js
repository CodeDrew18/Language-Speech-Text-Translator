import axios from "axios";

function countMeaningfulWords(text) {
  if (!text || typeof text !== "string") {
    return 0;
  }

  return (text.match(/[A-Za-z0-9]+/g) || []).length;
}

export function validateSpeechContent(transcriptData, options = {}) {
  const { allowMusic = false } = options;
  const text = (transcriptData?.text || "").trim();
  const words = Array.isArray(transcriptData?.words) ? transcriptData.words : [];
  const confidence = typeof transcriptData?.confidence === "number" ? transcriptData.confidence : null;
  const audioDurationMs =
    typeof transcriptData?.audio_duration === "number" ? transcriptData.audio_duration : null;

  const wordCount = countMeaningfulWords(text);
  if (!wordCount) {
    return {
      ok: false,
      reason: "No clear speech detected in the uploaded audio.",
      metrics: { wordCount, confidence, audioDurationMs },
    };
  }

  if (words.length > 0) {
    const avgWordConfidence =
      words.reduce((sum, item) => sum + (item?.confidence || 0), 0) / words.length;
    if (!allowMusic && avgWordConfidence < 0.45 && wordCount < 8) {
      return {
        ok: false,
        reason: "Audio looks like music or noise (low speech confidence).",
        metrics: { wordCount, confidence, avgWordConfidence, audioDurationMs },
      };
    }

    if (!allowMusic && audioDurationMs && audioDurationMs >= 60000) {
      const spokenMs = words.reduce((sum, item) => {
        const start = typeof item?.start === "number" ? item.start : 0;
        const end = typeof item?.end === "number" ? item.end : 0;
        return sum + Math.max(0, end - start);
      }, 0);

      const speechRatio = spokenMs / audioDurationMs;
      if (speechRatio < 0.01 && wordCount < 10) {
        return {
          ok: false,
          reason: "Most of the file appears non-speech audio (music/background sound).",
          metrics: { wordCount, confidence, avgWordConfidence, speechRatio, audioDurationMs },
        };
      }
    }

    if (allowMusic && avgWordConfidence < 0.25 && wordCount < 4) {
      return {
        ok: false,
        reason: "No reliable sung/spoken words detected. Try a clearer section with vocals.",
        metrics: { wordCount, confidence, avgWordConfidence, audioDurationMs },
      };
    }
  }

  if (!allowMusic && confidence !== null && confidence < 0.5 && wordCount < 6) {
    return {
      ok: false,
      reason: "Speech is too unclear to translate reliably.",
      metrics: { wordCount, confidence, audioDurationMs },
    };
  }

  if (!allowMusic && audioDurationMs && audioDurationMs >= 120000 && wordCount < 8) {
    return {
      ok: false,
      reason: "Long audio has too little spoken content. Please upload clearer speech audio.",
      metrics: { wordCount, confidence, audioDurationMs },
    };
  }

  return {
    ok: true,
    reason: null,
    metrics: { wordCount, confidence, audioDurationMs },
  };
}

export async function uploadAudioToAssemblyAi({ fileBuffer, mimeType, apiKey }) {
  if (!apiKey) {
    throw new Error("Missing ASSEMBLYAI_API_KEY in .env.");
  }

  const response = await axios.post("https://api.assemblyai.com/v2/upload", fileBuffer, {
    headers: {
      authorization: apiKey,
      "content-type": mimeType || "application/octet-stream",
    },
    maxBodyLength: Infinity,
    timeout: 120000,
  });

  const audioUrl = response.data?.upload_url;
  if (!audioUrl) {
    throw new Error("Failed to upload audio.");
  }

  return audioUrl;
}

export async function requestTranscription({ audioUrl, apiKey }) {
  const response = await axios.post(
    "https://api.assemblyai.com/v2/transcript",
    {
      audio_url: audioUrl,
      speech_models: ["universal-3-pro", "universal-2"],
      language_detection: true,
    },
    {
      headers: {
        authorization: apiKey,
        "content-type": "application/json",
      },
      timeout: 30000,
    },
  );

  const transcriptId = response.data?.id;
  if (!transcriptId) {
    throw new Error("Failed to start transcription job.");
  }

  return transcriptId;
}

export async function waitForTranscription({ transcriptId, apiKey }) {
  const maxAttempts = 60;

  for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
    const response = await axios.get(`https://api.assemblyai.com/v2/transcript/${transcriptId}`, {
      headers: {
        authorization: apiKey,
      },
      timeout: 30000,
    });

    const status = response.data?.status;
    if (status === "completed") {
      return response.data;
    }

    if (status === "error") {
      throw new Error(response.data?.error || "Transcription failed.");
    }

    await new Promise((resolve) => setTimeout(resolve, 2500));
  }

  throw new Error("Transcription timed out.");
}
