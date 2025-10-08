import { marked } from 'marked';
import sanitizeHtml from 'sanitize-html';

export function mdToHtml(md?: string): string {
  if (!md) return '';
  const html = marked.parse(md) as string;
  // Allow basic formatting and images/links
  return sanitizeHtml(html, {
    allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img', 'h1','h2','h3','h4','h5','h6','pre','code']),
    allowedAttributes: {
      a: ['href', 'name', 'target', 'rel'],
      img: ['src', 'alt', 'title', 'width', 'height'],
      code: ['class']
    },
    // Transform links and images to use base path
    transformTags: {
      a: (tagName: string, attribs: any) => {
        // Add base path to internal links
        if (attribs.href && attribs.href.startsWith('/') && !attribs.href.startsWith('//')) {
          attribs.href = `/FF03D1D1D403328562431NECSI${attribs.href}`;
        }
        // External links get noopener noreferrer
        if (attribs.href && (attribs.href.startsWith('http') || attribs.href.startsWith('//'))) {
          attribs.rel = 'noopener noreferrer';
          attribs.target = '_blank';
        }
        return { tagName, attribs };
      },
      img: (tagName: string, attribs: any) => {
        // Add base path to image sources
        if (attribs.src && attribs.src.startsWith('/') && !attribs.src.startsWith('//')) {
          attribs.src = `/FF03D1D1D403328562431NECSI${attribs.src}`;
        }
        return { tagName, attribs };
      }
    }
  });
}
