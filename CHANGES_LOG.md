# Research Data Changes Log

This file tracks all changes made to research data files to add images to hero sections.

## Changes Made

### Date: $(date)

#### Files Modified:
- [x] research-overview/index.json
- [x] teams-a-manifesto/index.json
- [x] multiscale-information-and-universality/index.json
- [x] evolution-of-lifespans/index.json
- [x] ending-pandemics/index.json
- [x] stopping-zika-and-microcephaly/index.json
- [x] social-complexity/index.json
- [x] precautionary-principle/index.json
- [x] social-media/index.json
- [x] ethnic-violence/index.json
- [x] financial-crisis/index.json
- [x] food-crisis/index.json
- [x] social-systems/index.json
- [x] economics/index.json
- [x] economic-dynamics/index.json
- [x] multiscale-methods/index.json
- [x] networks/index.json
- [x] evolution-and-systems-biology/index.json
- [x] biodiversity/index.json
- [x] group-selection/index.json
- [x] healthcare/index.json
- [x] sports/index.json
- [x] engineering/index.json
- [x] military/index.json
- [x] business/index.json
- [x] complexity-logic-and-cognition/index.json
- [x] education/index.json

#### Changes Summary:
- Added image field to hero section of each research data file
- Images sourced from the research index.json file
- Maintained existing hero structure while adding image property

#### Revert Instructions:
To revert these changes, restore the original hero sections from backup or remove the "image" field from each hero object.

---

## Image URL Updates - 2025-09-19T02:35:05.926Z

Updated image URLs in data folder based on data-old folder:

- **biodiversity**: Updated hero.image from "../assets/images/meta_9f1441eb1e3f684e.jpg" to "../assets/images/biodiversity.png"
- **business**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/negotiation1.png"
- **complexity-logic-and-cognition**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/logic.png"
- **economic-dynamics**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/econdynamics.png"
- **economics**: Updated hero.image from "../assets/images/meta_79f41b13f3962ecf.png" to "../assets/images/economics1.png"
- **education**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/education1.png"
- **ending-pandemics**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/pandemics.png"
- **engineering**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/socialmedia.png"
- **ethnic-violence**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/violence.png"
- **evolution-and-systems-biology**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/evolution1.png"
- **evolution-of-lifespans**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/lifespans.png"
- **financial-crisis**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/financialcrisis.png"
- **food-crisis**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/foodcrisis.png"
- **group-selection**: Updated hero.image from "../assets/images/meta_e6d0541b59d46bc8.png" to "../assets/images/kinselection.png"
- **healthcare**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/healthcare1.png"
- **military**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/military.png"
- **multiscale-information-and-universality**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/multiscale.png"
- **multiscale-methods**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/multiscale1.png"
- **networks**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/networks1.png"
- **precautionary-principle**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/precautionary.png"
- **research-overview**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/overview1.png"
- **social-complexity**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/socialcomplexity.png"
- **social-media**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/socialmedia.png"
- **social-systems**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/social1.png"
- **sports**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/teambuilding.png"
- **stopping-zika-and-microcephaly**: Updated hero.image from "../assets/images/meta_e84648730718f1f7.png" to "../assets/images/petare.png"
- **teams-a-manifesto**: Updated hero.image from "../assets/images/meta_ec7089b0ca1fc0e8.jpg" to "../assets/images/teams.png"

---

## Research Papers Layout Update - 2025-09-19T02:45:00.000Z

Created new layout component for displaying research papers with enhanced visual design:

### New Component Created:
- **ResearchPapersLayout.astro**: New component for displaying research papers with modern card-based layout

### Features Added:
- **Modern Card Design**: Clean, professional card layout with hover effects
- **Image Integration**: Proper display of research paper images with overlay effects
- **Responsive Grid**: Auto-fitting grid layout that adapts to different screen sizes
- **Interactive Elements**: Hover animations, smooth transitions, and visual feedback
- **Typography**: Improved readability with proper font hierarchy
- **Accessibility**: Proper semantic HTML structure and ARIA labels

### Layout Features:
- **Header Section**: Title and subtitle for the research papers section
- **Grid Layout**: Responsive grid that adapts from 3 columns to 1 column on mobile
- **Card Components**: Each paper displayed as an individual card with:
  - Image with hover zoom effect
  - Overlay with category badge
  - Title with hover color change
  - Summary text (when available)
  - "Read More" button with arrow icon
- **Footer**: Paper count display
- **Animations**: Staggered fade-in animations for cards

### Integration:
- **Updated `[...slug].astro`**: Replaced ResearchCards with ResearchPapersLayout for `allResearch` type pages
- **Maintained Compatibility**: Existing ResearchCards component still available for other uses

### Technical Details:
- **CSS Grid**: Modern responsive grid system
- **CSS Animations**: Smooth transitions and hover effects
- **Mobile-First**: Responsive design with mobile optimizations
- **Performance**: Lazy loading for images
- **Accessibility**: Proper semantic structure and keyboard navigation

