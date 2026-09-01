const publicCapabilityKeywordsByScenario: Record<string,string[]> = {
  'SCN-003': ['SemantiK'],
  'SCN-015': ['EkoH'],
  'SCN-021': ['SemantiK'],
  'SCN-022': ['SemantiK'],
  'SCN-028': ['SemantiK'],
  'SCN-029': ['EkoH'],
  'SCN-032': ['EkoH', 'SemantiK'],
  'SCN-034': ['EkoH'],
  'SCN-035': ['Smart Vote'],
  'SCN-046': ['Smart Vote'],
  'SCN-047': ['Smart Vote', 'EkoH'],
  'SCN-053': ['Smart Vote', 'EkoH'],
  'SCN-056': ['Smart Vote', 'EkoH'],
  'SCN-058': ['Smart Vote'],
  'SCN-060': ['Smart Vote'],
  'SCN-077': ['SemantiK'],
  'SCN-078': ['SemantiK'],
  'SCN-079': ['SemantiK'],
  'SCN-107': ['SemantiK'],
  'SCN-110': ['SemantiK'],
  'SCN-118': ['SemantiK'],
};

export function getCapabilityKeywords(data:any): string[] {
  return publicCapabilityKeywordsByScenario[data?.id] ?? [];
}
