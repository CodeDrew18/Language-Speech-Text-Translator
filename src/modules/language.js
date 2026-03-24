const translateLanguageMap = {
  "zh-cn": "zh-CN",
  "fil-ph": "tl",
  "tagalog": "tl",
  "ilocano": "ilo",
  "ilokano": "ilo",
};

export function normalizeLanguageCode(code) {
  if (!code || typeof code !== "string") {
    return "auto";
  }

  const cleaned = code.trim().toLowerCase();
  if (!cleaned) {
    return "auto";
  }

  if (translateLanguageMap[cleaned]) {
    return translateLanguageMap[cleaned];
  }

  return cleaned.includes("-") ? cleaned.split("-")[0] : cleaned;
}
