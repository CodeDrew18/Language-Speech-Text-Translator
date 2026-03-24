const transcriptEl = document.getElementById("transcript");
const translationEl = document.getElementById("translation");
const statusEl = document.getElementById("status");

const targetLangEl = document.getElementById("targetLang");
const micLangEl = document.getElementById("micLang");
const audioFileEl = document.getElementById("audioFile");
const allowMusicEl = document.getElementById("allowMusic");
const quickTextEl = document.getElementById("quickText");

const startMicBtn = document.getElementById("startMic");
const stopMicBtn = document.getElementById("stopMic");
const translateMicBtn = document.getElementById("translateMic");
const uploadTranslateBtn = document.getElementById("uploadTranslate");
const translateTextBtn = document.getElementById("translateText");
const speakTranslationBtn = document.getElementById("speakTranslation");

const MAX_AUDIO_UPLOAD_MB = 35;
const MAX_AUDIO_UPLOAD_BYTES = MAX_AUDIO_UPLOAD_MB * 1024 * 1024;

let recognition;
let micTranscript = "";
let currentSpeechAudio;
let currentSpeechUrl;

function setStatus(text, isError = false) {
  statusEl.textContent = text;
  statusEl.style.color = isError ? "#b52626" : "#0f6b56";
}

function detectSpeechRecognition() {
  return window.SpeechRecognition || window.webkitSpeechRecognition;
}

function updateSpeakButtonState() {
  const text = translationEl.textContent?.trim();
  speakTranslationBtn.disabled = !text || text === "No translation yet.";
}

function stopCurrentSpeech() {
  if (currentSpeechAudio) {
    currentSpeechAudio.pause();
    currentSpeechAudio = undefined;
  }

  if (currentSpeechUrl) {
    URL.revokeObjectURL(currentSpeechUrl);
    currentSpeechUrl = undefined;
  }
}

function setupMic() {
  const SpeechRecognition = detectSpeechRecognition();

  if (!SpeechRecognition) {
    startMicBtn.disabled = true;
    setStatus("Speech recognition is not supported in this browser.", true);
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onstart = () => {
    startMicBtn.disabled = true;
    stopMicBtn.disabled = false;
    translateMicBtn.disabled = true;
    micTranscript = "";
    transcriptEl.textContent = "Listening...";
    setStatus("Microphone listening started.");
  };

  recognition.onresult = (event) => {
    let finalText = "";
    let interimText = "";

    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      const text = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalText += text + " ";
      } else {
        interimText += text;
      }
    }

    if (finalText) {
      micTranscript += finalText;
    }

    transcriptEl.textContent = `${micTranscript}${interimText}`.trim() || "Listening...";
  };

  recognition.onerror = (event) => {
    setStatus(`Microphone error: ${event.error}`, true);
  };

  recognition.onend = () => {
    startMicBtn.disabled = false;
    stopMicBtn.disabled = true;
    translateMicBtn.disabled = !micTranscript.trim();
    transcriptEl.textContent = micTranscript.trim() || "No transcript captured.";

    if (micTranscript.trim()) {
      setStatus("Microphone capture stopped. Ready to translate.");
    }
  };

  startMicBtn.addEventListener("click", () => {
    recognition.lang = micLangEl.value;
    recognition.start();
  });

  stopMicBtn.addEventListener("click", () => {
    recognition.stop();
  });
}

async function translateMicText() {
  const text = micTranscript.trim();
  if (!text) {
    setStatus("Please speak first, then stop the microphone.", true);
    return;
  }

  try {
    translateMicBtn.disabled = true;
    setStatus("Translating microphone speech...");

    const response = await fetch("/api/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        sourceLang: "auto",
        targetLang: targetLangEl.value,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Translation failed.");
    }

    transcriptEl.textContent = data.transcript;
    translationEl.textContent = data.translation || "No translation returned.";
    updateSpeakButtonState();
    setStatus("Microphone speech translated.");
  } catch (error) {
    setStatus(error.message || "Translation failed.", true);
  } finally {
    translateMicBtn.disabled = false;
  }
}

async function transcribeAndTranslateUpload() {
  const file = audioFileEl.files?.[0];
  if (!file) {
    setStatus("Please choose an audio file to upload.", true);
    return;
  }

  if (file.size > MAX_AUDIO_UPLOAD_BYTES) {
    setStatus(`File is too large. Maximum size is ${MAX_AUDIO_UPLOAD_MB}MB.`, true);
    return;
  }

  try {
    uploadTranslateBtn.disabled = true;
    setStatus("Uploading audio and transcribing. This may take a bit...");

    const formData = new FormData();
    formData.append("audio", file);
    formData.append("targetLang", targetLangEl.value);
    formData.append("allowMusic", allowMusicEl?.checked ? "true" : "false");

    const response = await fetch("/api/transcribe-and-translate", {
      method: "POST",
      body: formData,
    });

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.error || `Transcribe and translate failed (HTTP ${response.status}).`);
    }

    transcriptEl.textContent = data.transcript || "No transcript returned.";
    translationEl.textContent = data.translation || "No translation returned.";
    updateSpeakButtonState();
    setStatus(data.musicMode ? "Audio (music mode) transcribed and translated." : "Audio file transcribed and translated.");
  } catch (error) {
    setStatus(error.message || "Upload failed.", true);
  } finally {
    uploadTranslateBtn.disabled = false;
  }
}

async function translateTypedText() {
  const text = quickTextEl.value.trim();
  if (!text) {
    setStatus("Please type text to translate.", true);
    return;
  }

  try {
    translateTextBtn.disabled = true;
    setStatus("Translating typed text...");

    const selectedTarget = targetLangEl.value;
    const isTagalogToIlokano = selectedTarget === "ilo";

    const response = isTagalogToIlokano
      ? await fetch("/api/tagalog-to-ilokano", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text }),
        })
      : await fetch("/api/translate", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text,
            sourceLang: "auto",
            targetLang: selectedTarget,
          }),
        });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Translation failed.");
    }

    transcriptEl.textContent = text;
    translationEl.textContent = data.translation || "No translation returned.";
    updateSpeakButtonState();
    setStatus("Typed text translated.");
  } catch (error) {
    setStatus(error.message || "Translation failed.", true);
  } finally {
    translateTextBtn.disabled = false;
  }
}

async function speakTranslation() {
  const text = translationEl.textContent?.trim();
  if (!text || text === "No translation yet.") {
    setStatus("There is no translated text to speak yet.", true);
    return;
  }

  try {
    speakTranslationBtn.disabled = true;
    setStatus("Generating voice for translated text...");
    stopCurrentSpeech();

    const response = await fetch("/api/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text,
        model: "kokoro",
        voice: "af_bella",
      }),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.error || `Voice generation failed (HTTP ${response.status}).`);
    }

    const responseType = response.headers.get("content-type") || "";
    if (!responseType.toLowerCase().includes("audio")) {
      const data = await response.json().catch(async () => ({ error: await response.text().catch(() => "Unsupported voice response.") }));
      throw new Error(data.error || "Voice provider returned a non-audio response.");
    }

    const audioBlob = await response.blob();
    currentSpeechUrl = URL.createObjectURL(audioBlob);
    currentSpeechAudio = new Audio(currentSpeechUrl);

    currentSpeechAudio.onended = () => {
      setStatus("Voice playback finished.");
      stopCurrentSpeech();
      updateSpeakButtonState();
    };

    await currentSpeechAudio.play();
    setStatus("Playing translated voice...");
  } catch (error) {
    setStatus(error.message || "Voice generation failed.", true);
  } finally {
    updateSpeakButtonState();
  }
}

setupMic();
updateSpeakButtonState();
translateMicBtn.addEventListener("click", translateMicText);
uploadTranslateBtn.addEventListener("click", transcribeAndTranslateUpload);
translateTextBtn.addEventListener("click", translateTypedText);
speakTranslationBtn.addEventListener("click", speakTranslation);
