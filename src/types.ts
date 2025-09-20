export interface PageData {
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
    menu: Array<{
      label: string;
      href: string;
    }>;
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
  footerLinks: Array<{
    label: string;
    href: string;
  }>;
  // Type-specific fields
  researches?: Array<{
    title: string | null;
    href: string;
    summary: string | null;
    image: string | null;
  }>;
  research?: {
    sections: Array<{
      heading: string | null;
      text: string | null;
    }>;
  };
  learnMore?: Array<{
    label: string;
    href: string;
  }>;
  signUp?: Array<{
    label: string;
    href: string;
  }>;
  compassions?: Array<{
    title: string | null;
    href: string;
    summary: string | null;
    image: string | null;
  }>;
}
