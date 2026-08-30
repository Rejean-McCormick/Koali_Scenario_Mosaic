export type PublicActivityKey =
  | 'understand'
  | 'learn'
  | 'create'
  | 'decide'
  | 'act'
  | 'respond'
  | 'remember';

export const publicActivityGroups: Array<{
  key: PublicActivityKey;
  label: string;
  palette: string[];
}> = [
  { key: 'understand', label: 'Understand', palette: ['find', 'understand', 'verify'] },
  { key: 'learn', label: 'Learn & share', palette: ['learn', 'teach-share'] },
  { key: 'create', label: 'Create together', palette: ['collaborate', 'create'] },
  { key: 'decide', label: 'Decide', palette: ['deliberate', 'choose'] },
  { key: 'act', label: 'Organize & act', palette: ['organize', 'act'] },
  { key: 'respond', label: 'Respond', palette: ['respond', 'coordinate'] },
  { key: 'remember', label: 'Remember & share', palette: ['remember', 'disseminate'] },
];

export function getPublicActivities(palette: string[] = []) {
  const active = new Set(palette);
  return Object.fromEntries(
    publicActivityGroups.map((group) => [
      group.key,
      group.palette.some((verb) => active.has(verb)),
    ]),
  ) as Record<PublicActivityKey, boolean>;
}

export function humanizePublicValue(value: string) {
  return value
    .replace(/[-_]+/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}
