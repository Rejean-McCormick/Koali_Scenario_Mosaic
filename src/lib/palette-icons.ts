export const paletteIconFiles = {
  find: 'search.svg',
  understand: 'lightbulb.svg',
  verify: 'badge-check.svg',
  learn: 'book-open.svg',
  'teach-share': 'graduation-cap.svg',
  collaborate: 'users.svg',
  create: 'sparkles.svg',
  deliberate: 'messages-square.svg',
  choose: 'git-branch.svg',
  organize: 'list-checks.svg',
  act: 'zap.svg',
  respond: 'message-circle-reply.svg',
  coordinate: 'network.svg',
  remember: 'history.svg',
  disseminate: 'radio.svg',
} as const;

export function paletteIconPath(key: string) {
  const filename = (paletteIconFiles as Record<string,string>)[key];
  return filename ? `/icons/palette/${filename}` : null;
}

export const paletteBacklightGroups = [
  { key: 'find', palette: ['find','verify'], icon: 'search.svg', label: { en: 'Find', fr: 'Trouver' }, architecture: ['Kristal','Konnaxion'] },
  { key: 'understand', palette: ['understand'], icon: 'lightbulb.svg', label: { en: 'Understand', fr: 'Comprendre' }, architecture: ['Kristal','SemantiK'] },
  { key: 'learn', palette: ['learn','teach-share'], icon: 'book-open.svg', label: { en: 'Learn', fr: 'Apprendre' }, architecture: ['Konnaxion','UCKK'] },
  { key: 'collaborate', palette: ['collaborate','create'], icon: 'users.svg', label: { en: 'Collaborate', fr: 'Collaborer' }, architecture: ['Konnaxion'] },
  { key: 'choose', palette: ['deliberate','choose'], icon: 'git-branch.svg', label: { en: 'Choose', fr: 'Choisir' }, architecture: ['Konnaxion','Smart Vote','EkoH'] },
  { key: 'act', palette: ['organize','act'], icon: 'zap.svg', label: { en: 'Act', fr: 'Agir' }, architecture: ['Orgo'] },
  { key: 'respond', palette: ['respond','coordinate'], icon: 'message-circle-reply.svg', label: { en: 'Respond', fr: 'Répondre' }, architecture: ['Orgo','Konnaxion'] },
  { key: 'remember', palette: ['remember','disseminate'], icon: 'history.svg', label: { en: 'Remember', fr: 'Se souvenir' }, architecture: ['Kristal','UCKK'] },
] as const;
