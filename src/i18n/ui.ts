import frTags from './fr-tags.json';

export const locales = ['en', 'fr'] as const;
export type Locale = (typeof locales)[number];

export const ui = {
  en: {
    languageName: 'English',
    alternateLanguageName: 'Français',
    brandTagline: 'the Sociotechnical Operating System',
    scenarioMosaic: 'Scenario Mosaic',
    scenarios: 'scenarios',
    exploreWays: (count:number) => `Explore ${count} ways to use Koali`,
    hoverIntro: 'Hover a cell to discover a concrete situation and its public scenario profile.',
    hoverHint: 'Hover or focus a cell',
    readScenario: 'Read the scenario',
    scenarioProfile: 'Scenario profile',
    exploreMosaic: 'Explore the Mosaic',
    typicalMotion: 'Typical motion',
    hoverInspect: 'Hover a cell to inspect it.',
    whatHappens: 'What happens here',
    scale: 'Scale',
    context: 'Context',
    specialConditions: 'Special conditions',
    noneHighlighted: 'None highlighted',
    searchScenarios: 'Search scenarios',
    searchPlaceholder: 'Search the mosaic…',
    surprise: 'Surprise me',
    reset: 'Reset',
    colorLegend: 'Scenario color legend',
    mosaicTitle: 'Koali Scenario Mosaic',
    mosaicDescription: '120 scenarios arranged as a compact 20 by 6 honeycomb panorama. Colors identify eight scenario families shown in the legend.',
    mosaicHint: 'Each color is a scenario family. Hover or focus one hexagon to inspect it above.',
    backToMosaic: '← Back to mosaic',
    allScenarios: 'All scenarios',
    detailStartsWith: 'Starts with',
    detailWhatGetsLost: 'What can get lost',
    detailKoaliContinuity: 'Koali keeps connected',
    detailFlow: 'Flow',
    detailTransferable: 'Transferable to',
    detailBack: 'Back to the full Mosaic',
    activityLabels: {
      understand: 'Understand', learn: 'Learn & share', create: 'Create together', decide: 'Decide', act: 'Organize & act', respond: 'Respond', remember: 'Remember & share',
    },
  },
  fr: {
    languageName: 'Français',
    alternateLanguageName: 'English',
    brandTagline: 'the Sociotechnical Operating System',
    scenarioMosaic: 'Mosaïque de scénarios',
    scenarios: 'scénarios',
    exploreWays: (count:number) => `Explorez ${count} façons d’utiliser Koali`,
    hoverIntro: 'Survolez une cellule pour découvrir une situation concrète et son profil public.',
    hoverHint: 'Survolez ou ciblez une cellule',
    readScenario: 'Lire le scénario',
    scenarioProfile: 'Profil du scénario',
    exploreMosaic: 'Explorer la mosaïque',
    typicalMotion: 'Dynamique typique',
    hoverInspect: 'Survolez une cellule pour l’examiner.',
    whatHappens: 'Ce qui se passe ici',
    scale: 'Échelle',
    context: 'Contexte',
    specialConditions: 'Conditions particulières',
    noneHighlighted: 'Aucune mise en évidence',
    searchScenarios: 'Rechercher des scénarios',
    searchPlaceholder: 'Rechercher dans la mosaïque…',
    surprise: 'Au hasard',
    reset: 'Réinitialiser',
    colorLegend: 'Légende des couleurs des scénarios',
    mosaicTitle: 'Mosaïque de scénarios Koali',
    mosaicDescription: '120 scénarios disposés dans un panorama compact en nid d’abeilles de 20 par 6. Les couleurs identifient huit familles de scénarios présentées dans la légende.',
    mosaicHint: 'Chaque couleur représente une famille de scénarios. Survolez ou ciblez un hexagone pour l’examiner ci-dessus.',
    backToMosaic: '← Retour à la mosaïque',
    allScenarios: 'Tous les scénarios',
    detailStartsWith: 'Point de départ',
    detailWhatGetsLost: 'Ce qui peut se perdre',
    detailKoaliContinuity: 'Koali maintient le lien',
    detailFlow: 'Déroulé',
    detailTransferable: 'Transposable à',
    detailBack: 'Retour à la mosaïque complète',
    activityLabels: {
      understand: 'Comprendre', learn: 'Apprendre & transmettre', create: 'Créer ensemble', decide: 'Décider', act: 'Organiser & agir', respond: 'Répondre', remember: 'Se souvenir & partager',
    },
  },
} as const;

export function getUi(locale: Locale) { return ui[locale]; }

export function humanizeTag(locale: Locale, value: string) {
  if (locale === 'fr') {
    return (frTags as Record<string,string>)[value] ?? value.replace(/[-_]+/g, ' ').replace(/^./, c => c.toUpperCase());
  }
  return value.replace(/[-_]+/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

export function localizePalette(locale: Locale, value: string) {
  if (locale === 'fr') return (frTags as Record<string,string>)[value] ?? value;
  return value.replace(/[-_]+/g, ' ');
}


const entryTriggerLabels: Record<Locale, Record<string,string>> = {
  en: {
    'question-or-signal': 'A question, signal, or anomaly',
    'knowledge-to-transfer': 'Knowledge that needs to be transmitted',
    'idea-or-goal': 'An idea or goal to develop together',
    'decision-to-make': 'A choice that needs to be made',
    'mandate-or-plan': 'A mandate or plan that must become action',
    'incident-or-change': 'An incident or changing situation',
    'result-or-lessons-learned': 'A result or lesson worth preserving',
    'knowledge-to-publish': 'Knowledge that needs to reach a public',
  },
  fr: {
    'question-or-signal': 'Une question, un signal ou une anomalie',
    'knowledge-to-transfer': 'Un savoir qui doit être transmis',
    'idea-or-goal': 'Une idée ou un objectif à développer ensemble',
    'decision-to-make': 'Un choix qui doit être fait',
    'mandate-or-plan': 'Un mandat ou un plan qui doit devenir action',
    'incident-or-change': 'Un incident ou une situation qui évolue',
    'result-or-lessons-learned': 'Un résultat ou une leçon à préserver',
    'knowledge-to-publish': 'Un savoir qui doit rejoindre un public',
  },
};

export function localizeEntryTrigger(locale: Locale, value: string) {
  return entryTriggerLabels[locale][value] ?? humanizeTag(locale, value);
}
