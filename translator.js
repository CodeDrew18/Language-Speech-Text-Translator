import dotenv from "dotenv";
import { createApp } from "./src/app.js";

dotenv.config();

const port = Number(process.env.PORT || 3000);
const assemblyAiApiKey = process.env.ASSEMBLYAI_API_KEY;
const ttsAiApiKey = process.env.TTS_AI_API_KEY;
const app = createApp({ assemblyAiApiKey, ttsAiApiKey });

app.listen(port, () => {
	console.log(`Audio translator running at http://localhost:${port}`);
});
