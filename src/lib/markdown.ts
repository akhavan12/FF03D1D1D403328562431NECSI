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
    // Ensure external links are safe
    transformTags: {
      a: (tagName: string, attribs: any) => {
        // External links get noopener noreferrer
        if (attribs.href && (attribs.href.startsWith('http') || attribs.href.startsWith('//'))) {
          attribs.rel = 'noopener noreferrer';
          attribs.target = '_blank';
        }
        return { tagName, attribs };
      }
    }
  });
}
