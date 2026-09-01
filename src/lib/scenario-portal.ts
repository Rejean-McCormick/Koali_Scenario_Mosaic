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

function lowerFirst(value:string) {
  return value ? value[0].toLocaleLowerCase() + value.slice(1) : value;
}

function stripTerminalPunctuation(value:string) {
  return value.trim().replace(/[.!?;:]+$/u, '');
}

function extractExampleLead(summary:string) {
  const marker = summary.indexOf('Koali');
  return marker > 0 ? summary.slice(0, marker).trim() : '';
}

function flowEndpoints(body:string, locale:Locale) {
  const flow = extractScenarioPublicDetails(body, locale).flow;
  const steps = flow
    .split('→')
    .map((step) => stripTerminalPunctuation(step))
    .filter(Boolean);

  return {
    flow,
    start: steps[0] ?? '',
    end: steps.length > 1 ? steps[steps.length - 1] : '',
  };
}

/**
 * Public preview copy deliberately does not restate the capability headline.
 *
 * The headline names the concrete action. This paragraph explains Koali's own
 * architectural role: keep one context continuous while specialized
 * capabilities contribute at different points in the journey.
 */
export function buildKoaliContinuityCopy(body:string, continuityGap:string, locale:Locale) {
  const { start, end } = flowEndpoints(body, locale);
  const gap = stripTerminalPunctuation(continuityGap ?? '');

  const continuitySentence = start && end
    ? (locale === 'fr'
      ? `Dans Koali, le même contexte passe d’une capacité spécialisée à l’autre sans être recréé, du point de départ « ${start} » jusqu’à « ${end} ».`
      : `In Koali, the same context moves across specialized capabilities without being recreated, from “${start}” through “${end}”.`)
    : (locale === 'fr'
      ? 'Dans Koali, le même contexte passe d’une capacité spécialisée à l’autre sans être recréé.'
      : 'In Koali, the same context moves across specialized capabilities without being recreated.');

  if (!gap) return continuitySentence;

  const gapSentence = locale === 'fr'
    ? `Sans ce fil commun, ${lowerFirst(gap)}.`
    : `Without that shared thread, ${lowerFirst(gap)}.`;

  return `${continuitySentence} ${gapSentence}`;
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
  const systems = getScenarioSystemRoutes(data, body, locale);
  return {
    capabilityTitle: scenarioCapabilityTitles[data.id]?.[locale] ?? data.pattern_label,
    patternFamily: data.pattern_label,
    koaliHelp: buildKoaliContinuityCopy(body, data.continuity_gap, locale),
    exampleTitle: data.title,
    exampleLead: extractExampleLead(data.preview_summary),
    systems,
  };
}
