# Midnight Nebula Design System

### 1. Overview & Creative North Star
**Creative North Star: The Neon Noir Gallery**
Midnight Nebula is a design system built for high-immersion editorial experiences. It moves away from the sterile, "app-like" utility of modern SaaS and instead embraces the moody, atmospheric depth of cinematic interfaces. By utilizing deep violets, glassmorphism, and intentional "glow" states, the system creates a sense of digital craftsmanship. The layout is intentionally spacious, using wide gutters and asymmetric element placement to guide the eye through content rather than forcing it through a grid.

### 2. Colors
The palette is rooted in a deep, spectral purple (#5d0dde) that acts as the primary "energy" source.

- **The "No-Line" Rule:** Visual boundaries must be established through color shifts or atmospheric effects. Standard 1px solid hex borders are strictly prohibited for sectioning. Instead, use background transitions from `surface` to `surface_container_high`.
- **Surface Hierarchy & Nesting:** Objects closer to the user should use progressively lighter surface tokens or increased glass opacity.
- **The Glass & Gradient Rule:** Interactive floating elements (like the Navbar or Hover Cards) must use `rgba(23, 16, 34, 0.6)` with a `12px` backdrop blur.
- **Signature Textures:** A radial "glow" gradient (`rgba(93, 13, 222, 0.15)` at the top center) should be present on main landing screens to provide a sense of verticality and light source.

### 3. Typography
The system uses **Inter** as a singular, versatile variable font, relying on drastic scale shifts and tracking rather than multiple families.

- **Display Scale:** For massive headlines, use `3rem` (48px) with `tracking-tighter` to create a bold, "poster" aesthetic.
- **Headline Hierarchy:** 
    - **H1:** `1.875rem` (30px) - Tight leading for impact.
    - **H2:** `1.25rem` (20px) - High tracking for section titles.
- **Body & Labels:** Use `1rem` (16px) for standard body and `0.875rem` (14px) for meta-information.
- **Energy Metaphor:** Primary labels and numeric values often use a specific "bolt" icon or increased font weight to highlight performance metrics or "energy" levels within the context.

### 4. Elevation & Depth
Elevation is achieved through light refraction and "glow" rather than traditional drop shadows.

- **The Layering Principle:** 
    - **Base:** `surface` (#171022)
    - **Panels:** `glass-panel` (0.6 opacity, 12px blur)
    - **Cards:** `glass-card` (0.03 opacity, 8px blur)
- **Ambient Shadows:** Use `0 4px 30px rgba(0, 0, 0, 0.1)` for soft depth.
- **Neon Interaction:** Active states use a "Neon Bar" or glow effect. For example, a primary button uses `shadow-[0_0_15px_rgba(93,13,222,0.4)]` to appear as if it is emitting light onto the surface below.

### 5. Components
- **Buttons:** Pill-shaped with a heavy glow. Primary buttons are solid #5d0dde; secondary buttons are "glass-card" styles with `white/10` text.
- **Glass Cards:** High-transparency containers that use a subtle white/5 border to catch the "light." On hover, the border-color shifts to a translucent primary purple.
- **Progress Bars:** Referred to as "Neon Bars." These utilize a primary purple fill with a `0 0 8px` blur to simulate light-tube illumination.
- **Navigation:** Sticky headers use the `glass-panel` class with a `white/5` bottom border to maintain separation without breaking the atmospheric flow.
- **Chips & Tags:** Small, low-contrast `white/5` backgrounds that bloom into full primary color on hover.

### 6. Do's and Don'ts
**Do:**
- Use wide spacing (Token 3) to allow elements to breathe.
- Combine `backdrop-filter` with low-opacity backgrounds for all overlays.
- Use `text-slate-400` or `text-slate-500` for secondary text to maintain a low-contrast, moody aesthetic.

**Don't:**
- Use sharp corners; the system requires a minimum of `0.5rem` (roundedness: 2) to maintain its "soft-tech" feel.
- Use white backgrounds; the system is strictly dark-mode-first to preserve the neon luminosity.
- Use multiple font families; stick to the Inter variable weight scale to keep the editorial look clean.