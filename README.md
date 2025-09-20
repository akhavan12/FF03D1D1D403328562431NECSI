# NECSI Astro Website

This is an Astro-based website that consumes the JSON data exported from the Squarespace site conversion script.

## Project Structure

```
src/
├── components/          # Reusable Astro components
│   ├── Layout.astro    # Main layout wrapper
│   ├── Navbar.astro    # Navigation component
│   ├── Footer.astro    # Footer component
│   ├── Hero.astro      # Hero section component
│   ├── ContentBlocks.astro # Content blocks component
│   ├── ResearchCards.astro # Research cards component
│   └── CTAButtons.astro    # Call-to-action buttons
├── data/               # JSON data files (exported from Squarespace)
├── pages/              # Astro pages
│   ├── index.astro     # Home page
│   ├── [...slug].astro # Dynamic route for all other pages
│   └── 404.astro       # 404 error page
├── styles/             # Global styles
├── types.ts            # TypeScript type definitions
└── utils/              # Utility functions
    └── data.ts         # Data loading utilities
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:4321`

### Building for Production

1. Generate static paths and build the site:
```bash
npm run build
```

2. Preview the production build:
```bash
npm run preview
```

## Data Structure

The website consumes JSON data files located in `src/data/`. Each page has a corresponding JSON file with the following structure:

```typescript
interface PageData {
  sourcePath: string;
  routePath: string;
  title: string | null;
  meta: {
    description: string | null;
    ogImage: string | null;
  };
  site: {
    title: string | null;
    logo: string | null;
  };
  type: 'main' | 'about' | 'allResearch' | 'singleResearch' | 'engage' | 'compassionateScience';
  navbar: {
    logo: string | null;
    menu: Array<{label: string; href: string}>;
  };
  hero: {
    title: string | null;
    subtitle: string | null;
    image: string | null;
  };
  contentBlocks?: Array<{
    heading: string | null;
    text: string | null;
  }>;
  footerLinks: Array<{label: string; href: string}>;
  // Type-specific fields...
}
```

## Page Types

The website supports different page types with specific layouts:

- **main**: Homepage with hero and content blocks
- **about**: About page with content blocks
- **allResearch**: Research listing page with research cards
- **singleResearch**: Individual research page with content sections
- **engage**: Engagement page with content blocks and CTA buttons
- **compassionateScience**: Compassionate science page with research cards

## Adding New Content

1. Add new JSON data files to `src/data/`
2. Run `npm run generate-paths` to update the static paths
3. The new pages will be automatically available

## Customization

### Styling

The website uses Tailwind CSS for styling. You can:

1. Modify the global styles in `src/styles/global.css`
2. Update component-specific styles in each `.astro` file
3. Add custom Tailwind classes to components

### Components

All components are located in `src/components/`. Each component is self-contained with its own styles and can be easily modified or extended.

### Layout

The main layout is defined in `src/components/Layout.astro` and includes:
- HTML structure
- Meta tags
- Global styles
- Navigation and footer

## Development Workflow

1. Make changes to components or pages
2. The development server will automatically reload
3. Test your changes in the browser
4. When ready, build for production with `npm run build`

## Deployment

The built site can be deployed to any static hosting service such as:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

Simply run `npm run build` and deploy the contents of the `dist/` directory.