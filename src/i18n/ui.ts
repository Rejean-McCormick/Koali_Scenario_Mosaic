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
    examples: 'concrete examples',
    exploreWays: (count:number) => `Explore ${count} concrete ways Koali helps`,
    hoverIntro: 'Select an example to see the specific Koali action, the system path behind it, and how the pattern transfers elsewhere.',
    selectCellPrompt: 'Select an example to reveal the specific Koali action behind it.',
    hoverHint: 'Hover or focus a cell',
    readScenario: 'Read the scenario',
    scenarioProfile: 'Scenario profile',
    exampleLabel: 'Example',
    openExample: 'Open the full example',
    insideKoali: 'Inside Koali',
    systemPath: 'System path',
    selectSystemHint: 'Select an example to see the specific Koali systems involved.',
    usuallyVia: 'Usually via',
    swipeHint: 'Swipe left for next · right for previous',
    exploreMosaic: 'Explore the Mosaic',
    typicalMotion: 'Typical motion',
    hoverInspect: 'Hover a cell to inspect it.',
    whatHappens: 'What happens here',
    scale: 'Scale',
    context: 'Context',
    specialConditions: 'Special conditions',
    noneHighlighted: 'None highlighted',
    searchScenarios: 'Search scenarios',
    searchPlaceholder: 'Search a need, system, or example…',
    surprise: 'Surprise me',
    reset: 'Reset',
    colorLegend: 'Scenario families',
    territoryMapLabels: {
      'CAT-01': ['Find &', 'Understand'],
      'CAT-02': ['Learn &', 'Share'],
      'CAT-03': ['Collaborate &', 'Create'],
      'CAT-04': ['Choose &', 'Govern'],
      'CAT-05': ['Organize &', 'Act'],
      'CAT-06': ['Respond &', 'Coordinate'],
      'CAT-07': ['Remember &', 'Improve'],
      'CAT-08': ['Disseminate &', 'Connect'],
    },
    mosaicTitle: 'Koali Scenario Mosaic',
    mosaicDescription: '120 concrete examples arranged as a compact 20 by 6 honeycomb panorama. Selecting one reveals a specific Koali action, its recurring pattern, and the systems that carry it.',
    mosaicHint: 'Each hexagon is an example. Select one to see the specific Koali action and its system path above.',
    backToMosaic: '← Back to mosaic',
    allScenarios: 'All scenarios',
    detailStartsWith: 'Starts from',
    detailWhatGetsLost: 'Koali mechanism',
    detailKoaliContinuity: 'System path',
    detailFlow: 'How it moves',
    detailTransferable: 'Also useful for',
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
    examples: 'exemples concrets',
    exploreWays: (count:number) => `Explorez ${count} façons concrètes dont Koali aide`,
    hoverIntro: 'Sélectionnez un exemple pour voir l’action précise de Koali, le chemin système qui la porte et comment le pattern se transpose ailleurs.',
    selectCellPrompt: 'Sélectionnez un exemple pour révéler l’action précise de Koali derrière la situation.',
    hoverHint: 'Survolez ou ciblez une cellule',
    readScenario: 'Lire le scénario',
    scenarioProfile: 'Profil du scénario',
    exampleLabel: 'Exemple',
    openExample: 'Ouvrir l’exemple complet',
    insideKoali: 'Dans Koali',
    systemPath: 'Chemin système',
    selectSystemHint: 'Sélectionnez un exemple pour voir les systèmes Koali précisément concernés.',
    usuallyVia: 'Généralement via',
    swipeHint: 'Balayez à gauche : suivant · à droite : précédent',
    exploreMosaic: 'Explorer la mosaïque',
    typicalMotion: 'Dynamique typique',
    hoverInspect: 'Survolez une cellule pour l’examiner.',
    whatHappens: 'Ce qui se passe ici',
    scale: 'Échelle',
    context: 'Contexte',
    specialConditions: 'Conditions particulières',
    noneHighlighted: 'Aucune mise en évidence',
    searchScenarios: 'Rechercher des scénarios',
    searchPlaceholder: 'Rechercher un besoin, un système ou un exemple…',
    surprise: 'Au hasard',
    reset: 'Réinitialiser',
    colorLegend: 'Familles de scénarios',
    territoryMapLabels: {
      'CAT-01': ['Trouver &', 'comprendre'],
      'CAT-02': ['Apprendre &', 'transmettre'],
      'CAT-03': ['Collaborer &', 'créer'],
      'CAT-04': ['Choisir &', 'gouverner'],
      'CAT-05': ['Organiser &', 'agir'],
      'CAT-06': ['Répondre &', 'coordonner'],
      'CAT-07': ['Se souvenir &', 'améliorer'],
      'CAT-08': ['Diffuser &', 'connecter'],
    },
    mosaicTitle: 'Mosaïque de scénarios Koali',
    mosaicDescription: '120 exemples concrets disposés dans un panorama compact en nid d’abeilles de 20 par 6. Chaque sélection révèle une action précise de Koali, son pattern récurrent et les systèmes qui la portent.',
    mosaicHint: 'Chaque hexagone est un exemple. Sélectionnez-en un pour voir l’action précise de Koali et son chemin système au-dessus.',
    backToMosaic: '← Retour à la mosaïque',
    allScenarios: 'Tous les scénarios',
    detailStartsWith: 'Part de',
    detailWhatGetsLost: 'Mécanisme Koali',
    detailKoaliContinuity: 'Chemin système',
    detailFlow: 'Comment ça circule',
    detailTransferable: 'Aussi utile pour',
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
