# GitHub Pages Deployment Guide

This guide will help you deploy your NECSI Astro site to GitHub Pages.

## Prerequisites

1. A GitHub account
2. Your code pushed to a GitHub repository

## Step 1: Update Repository Configuration

Before deploying, you need to update the `astro.config.mjs` file with your actual repository details:

```javascript
// Replace these values in astro.config.mjs
export default defineConfig({
  site: 'https://YOUR_USERNAME.github.io', // Replace with your GitHub username
  base: '/YOUR_REPOSITORY_NAME', // Replace with your repository name
  // ... rest of config
});
```

## Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** tab
3. Scroll down to **Pages** section in the left sidebar
4. Under **Source**, select **GitHub Actions**
5. The deployment workflow will automatically trigger

## Step 3: Automatic Deployment

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will:

1. **Build** your Astro site when you push to `main` branch
2. **Deploy** the built files to GitHub Pages
3. **Update** your live site automatically

## Step 4: Access Your Site

Your site will be available at:
`https://YOUR_USERNAME.github.io/YOUR_REPOSITORY_NAME`

## Manual Deployment (Alternative)

If you prefer to deploy manually:

```bash
# Build the site
npm run build

# The dist/ folder contains your built site
# You can upload the contents of dist/ to any static hosting service
```

## Troubleshooting

### Build Errors
- Check that all image paths are correct
- Ensure all dependencies are in package.json
- Verify that the build command completes without errors

### 404 Errors
- Make sure the `base` path in astro.config.mjs matches your repository name
- Check that all routes are properly configured in static-paths.json

### Assets Not Loading
- Verify that all assets are in the `public/` folder
- Check that image paths use absolute paths starting with `/`

## Features Included

✅ **Engage Page** - Custom newsletter signup form
✅ **Research Pages** - Dynamic research paper listings
✅ **Individual Research Pages** - Detailed research content
✅ **Responsive Design** - Mobile-friendly layout
✅ **SEO Optimized** - Meta tags and structured data
✅ **Fast Loading** - Optimized static site generation

## Support

If you encounter any issues:
1. Check the GitHub Actions logs in your repository
2. Verify your repository settings
3. Ensure all files are committed and pushed to the main branch
