KOALI_USAGE_MOSAIC — mobile profile text unclipping

Fixes the truncated two-column list visible in the mobile screenshot.

On <= 720px:
- "Ce qui se passe ici" spans the full profile-card width
- it remains a 2-column list
- labels may wrap naturally instead of showing ellipses
- "Échelle / Contexte / Conditions particulières" also span full width
- context values may wrap instead of being truncated
- heading + typical motion remain side by side at the top

Desktop is unchanged.

Files:
- src/styles/mosaic.css
- preview/assets/styles.css

Apply after:
KOALI_USAGE_MOSAIC_mobile_unclipped_backlights_overlay.zip
