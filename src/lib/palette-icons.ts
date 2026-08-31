export const paletteIconFiles = {
  "find": "search.svg",
  "understand": "lightbulb.svg",
  "verify": "badge-check.svg",
  "learn": "book-open.svg",
  "teach-share": "graduation-cap.svg",
  "collaborate": "users.svg",
  "create": "sparkles.svg",
  "deliberate": "messages-square.svg",
  "choose": "git-branch.svg",
  "organize": "list-checks.svg",
  "act": "zap.svg",
  "respond": "message-circle-reply.svg",
  "coordinate": "network.svg",
  "remember": "history.svg",
  "disseminate": "radio.svg"
} as const;

export function paletteIconPath(key: string) {
  const filename = (paletteIconFiles as Record<string,string>)[key];
  return filename ? `/icons/palette/${filename}` : null;
}

export const paletteBacklightGroups = [
  {
    "key": "find",
    "palette": [
      "find",
      "verify"
    ],
    "icon": "search.svg",
    "label": {
      "en": "Find",
      "fr": "Trouver"
    }
  },
  {
    "key": "understand",
    "palette": [
      "understand"
    ],
    "icon": "lightbulb.svg",
    "label": {
      "en": "Understand",
      "fr": "Comprendre"
    }
  },
  {
    "key": "learn",
    "palette": [
      "learn",
      "teach-share"
    ],
    "icon": "book-open.svg",
    "label": {
      "en": "Learn",
      "fr": "Apprendre"
    }
  },
  {
    "key": "collaborate",
    "palette": [
      "collaborate",
      "create"
    ],
    "icon": "users.svg",
    "label": {
      "en": "Collaborate",
      "fr": "Collaborer"
    }
  },
  {
    "key": "choose",
    "palette": [
      "deliberate",
      "choose"
    ],
    "icon": "git-branch.svg",
    "label": {
      "en": "Choose",
      "fr": "Choisir"
    }
  },
  {
    "key": "act",
    "palette": [
      "organize",
      "act"
    ],
    "icon": "zap.svg",
    "label": {
      "en": "Act",
      "fr": "Agir"
    }
  },
  {
    "key": "respond",
    "palette": [
      "respond",
      "coordinate"
    ],
    "icon": "message-circle-reply.svg",
    "label": {
      "en": "Respond",
      "fr": "Répondre"
    }
  },
  {
    "key": "remember",
    "palette": [
      "remember",
      "disseminate"
    ],
    "icon": "history.svg",
    "label": {
      "en": "Remember",
      "fr": "Se souvenir"
    }
  }
] as const;
