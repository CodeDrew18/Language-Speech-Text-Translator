import express from "express";
import multer from "multer";
import { normalizeLanguageCode } from "./modules/language.js";
import { translateText, translateTagalogToIlokano } from "./modules/translationService.js";
import {
  uploadAudioToAssemblyAi,
  requestTranscription,
  waitForTranscription,
  validateSpeechContent,
} from "./modules/transcriptionService.js";
import { generateSpeechAudio } from "./modules/ttsService.js";

const MAX_AUDIO_UPLOAD_MB = 35;

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: MAX_AUDIO_UPLOAD_MB * 1024 * 1024 },
});

export function createApp({ assemblyAiApiKey, ttsAiApiKey }) {
  const app = express();

  app.use(express.json({ limit: "1mb" }));
  app.use("/assets", express.static("assets"));
  app.use(express.static("public"));

  app.post("/api/translate", async (req, res) => {
    try {
      const { text, sourceLang, targetLang } = req.body || {};
      if (!text || typeof text !== "string") {
        return res.status(400).json({ error: "'text' is required." });
      }

      if (!targetLang || typeof targetLang !== "string") {
        return res.status(400).json({ error: "'targetLang' is required." });
      }

      const result = await translateText({ text, sourceLang, targetLang });

      return res.json({
        transcript: text,
        translation: result.translation,
        sourceLang: result.sourceLang,
        targetLang: result.targetLang,
      });
    } catch (error) {
      return res.status(500).json({
        error: error.response?.data?.error || error.message || "Translation failed.",
      });
    }
  });

  app.post("/api/tagalog-to-ilokano", async (req, res) => {
    try {
      const { text } = req.body || {};
      if (!text || typeof text !== "string") {
        return res.status(400).json({ error: "'text' is required." });
      }

      const result = await translateTagalogToIlokano(text);
      return res.json({
        transcript: text,
        translation: result.translation,
        sourceLang: "tl",
        targetLang: "ilo",
      });
    } catch (error) {
      return res.status(500).json({
        error: error.response?.data?.error || error.message || "Tagalog to Ilokano translation failed.",
      });
    }
  });

  app.post("/api/tts", async (req, res) => {
    try {
      const { text, model, voice } = req.body || {};
      if (!text || typeof text !== "string") {
        return res.status(400).json({ error: "'text' is required." });
      }

      const audioBuffer = await generateSpeechAudio({
        text,
        apiKey: ttsAiApiKey,
        model,
        voice,
      });

      res.setHeader("Content-Type", "audio/mpeg");
      res.setHeader("Cache-Control", "no-store");
      return res.status(200).send(audioBuffer);
    } catch (error) {
      const providerMessage =
        error.response?.data?.error?.message ||
        error.response?.data?.error ||
        error.response?.data?.message;

      return res.status(500).json({
        error: providerMessage || error.message || "Text-to-speech failed.",
      });
    }
  });

  app.post("/api/transcribe-and-translate", upload.single("audio"), async (req, res) => {
    try {
      if (!req.file?.buffer) {
        return res.status(400).json({ error: "Audio file is required (field name: audio)." });
      }

      const { targetLang, allowMusic } = req.body || {};
      if (!targetLang || typeof targetLang !== "string") {
        return res.status(400).json({ error: "'targetLang' is required." });
      }

      const enableMusicMode =
        allowMusic === true ||
        allowMusic === "true" ||
        allowMusic === "1";

      const audioUrl = await uploadAudioToAssemblyAi({
        fileBuffer: req.file.buffer,
        mimeType: req.file.mimetype,
        apiKey: assemblyAiApiKey,
      });

      const transcriptId = await requestTranscription({
        audioUrl,
        apiKey: assemblyAiApiKey,
      });

      const transcriptData = await waitForTranscription({
        transcriptId,
        apiKey: assemblyAiApiKey,
      });

      const speechValidation = validateSpeechContent(transcriptData, {
        allowMusic: enableMusicMode,
      });
      if (!speechValidation.ok) {
        return res.status(422).json({
          error: speechValidation.reason,
          details: speechValidation.metrics,
        });
      }

      const transcript = (transcriptData.text || "").trim();
      if (!transcript) {
        return res.status(422).json({ error: "No speech detected in the uploaded audio." });
      }

      const result = await translateText({
        text: transcript,
        sourceLang: "auto",
        targetLang,
      });

      return res.json({
        transcript,
        translation: result.translation,
        sourceLang: "auto",
        targetLang: normalizeLanguageCode(targetLang),
        speechModelUsed: transcriptData.speech_model_used || null,
        musicMode: enableMusicMode,
      });
    } catch (error) {
      return res.status(500).json({
        error: error.response?.data?.error || error.message || "Transcribe and translate failed.",
      });
    }
  });

  app.use((error, req, res, next) => {
    if (error instanceof multer.MulterError && error.code === "LIMIT_FILE_SIZE") {
      return res.status(413).json({
        error: `File is too large. Maximum size is ${MAX_AUDIO_UPLOAD_MB}MB.`,
      });
    }

    return next(error);
  });

  return app;
}
