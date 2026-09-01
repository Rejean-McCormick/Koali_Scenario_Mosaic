import type { Locale } from '../i18n/ui';
import systemCatalogJson from '../data/system-catalog.json';
import scenarioSystemRoutesJson from '../data/scenario-system-routes.json';
import scenarioCapabilityTitlesJson from '../data/scenario-capability-titles.json';
import { extractScenarioPublicDetails } from './scenario-public';

export type SystemRouteKey = keyof typeof systemCatalogJson;
export type SystemRoute = {
  key: SystemRouteKey;
  label: string;
  description: string;
};

const systemCatalog = systemCatalogJson as Record<SystemRouteKey,{
  label:string;
  description:Record<Locale,string>;
}>;
const scenarioSystemRoutes = scenarioSystemRoutesJson as Record<string,SystemRouteKey[]>;
const scenarioCapabilityTitles = scenarioCapabilityTitlesJson as Record<string,Record<Locale,string>>;

function wordCount(value:string) {
  return value.trim().split(/\s+/).filter(Boolean).length;
}

function lowerFirst(value:string) {
  return value ? value[0].toLocaleLowerCase() + value.slice(1) : value;
}

export function splitScenarioSummary(summary:string, pattern:string, body:string, locale:Locale) {
  const marker = summary.indexOf('Koali');
  const exampleLead = marker > 0 ? summary.slice(0, marker).trim() : '';
  let koaliHelp = marker >= 0 ? summary.slice(marker).trim() : summary.trim();

  // Public copy is deliberately Koali-first. Short mechanism sentences are
  // completed with the already-curated transferable pattern, not filler.
  if (wordCount(koaliHelp) < 36 && pattern) {
    const patternSentence = locale === 'fr'
      ? `L’objectif de continuité est de ${lowerFirst(pattern).replace(/[.]$/, '')}.`
      : `The continuity goal is to ${lowerFirst(pattern).replace(/[.]$/, '')}.`;
    koaliHelp = `${koaliHelp.replace(/\s+$/,'')} ${patternSentence}`;
  }

  if (wordCount(koaliHelp) < 36 && body) {
    const flow = extractScenarioPublicDetails(body, locale).flow;
    if (flow) {
      const flowSentence = locale === 'fr'
        ? `Dans cet exemple, le contexte reste relié tout au long de : ${flow}.`
        : `In this example, the context stays connected across: ${flow}.`;
      koaliHelp = `${koaliHelp.replace(/\s+$/,'')} ${flowSentence}`;
    }
  }

  return { exampleLead, koaliHelp };
}

export function getScenarioSystemRoutes(data:any, _body:string, locale:Locale): SystemRoute[] {
  return (scenarioSystemRoutes[data?.id] ?? []).map((key) => {
    const item = systemCatalog[key];
    return {
      key,
      label: item.label,
      description: item.description[locale],
    };
  });
}

export function getScenarioPortal(data:any, body:string, locale:Locale) {
  const { exampleLead, koaliHelp } = splitScenarioSummary(data.preview_summary, data.pattern, body, locale);
  const systems = getScenarioSystemRoutes(data, body, locale);
  return {
    capabilityTitle: scenarioCapabilityTitles[data.id]?.[locale] ?? data.pattern_label,
    patternFamily: data.pattern_label,
    koaliHelp,
    exampleTitle: data.title,
    exampleLead,
    systems,
  };
}
