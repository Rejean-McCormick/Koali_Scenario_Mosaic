import type { Locale } from '../i18n/ui';

function cleanInlineMarkdown(value: string) {
  return value
    .replace(/`([^`]+)`/g, '$1')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
}

function section(body: string, heading: string) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const source = `${body.trimEnd()}\n## __END__\n`;
  const match = source.match(new RegExp(`^## ${escaped}\\s*$([\\s\\S]*?)(?=^## )`, 'm'));
  return match ? cleanInlineMarkdown(match[1]) : '';
}

export function extractScenarioPublicDetails(body: string, locale: Locale) {
  const continuityHeading = locale === 'fr'
    ? 'Ce qui rend ce scénario caractéristique de Koali'
    : 'What makes this characteristically Koali';
  const loopHeading = locale === 'fr' ? 'Boucle' : 'Loop';

  return {
    continuity: section(body, continuityHeading),
    flow: section(body, loopHeading),
  };
}
