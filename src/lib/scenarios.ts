import { getCollection, type CollectionEntry } from 'astro:content';
import metadata from '../data/scenarios.json';
import type { Locale } from '../i18n/ui';

export type ScenarioTextEntry = CollectionEntry<'scenarioText'>;
export type ScenarioMeta = (typeof metadata)[keyof typeof metadata];
export type LocalizedScenario = {
  entry: ScenarioTextEntry;
  data: ScenarioMeta & ScenarioTextEntry['data'];
};

export async function getLocalizedScenarios(locale: Locale): Promise<LocalizedScenario[]> {
  const entries = await getCollection('scenarioText', ({ data }) => data.locale === locale);
  return entries
    .map((entry) => ({
      entry,
      data: { ...(metadata as Record<string,ScenarioMeta>)[entry.data.id], ...entry.data },
    }))
    .sort((a,b) => a.data.id.localeCompare(b.data.id));
}

export async function getLocalizedScenario(locale: Locale, id: string) {
  return (await getLocalizedScenarios(locale)).find((scenario) => scenario.data.id === id) ?? null;
}
