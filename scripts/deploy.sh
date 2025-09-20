#!/bin/bash

# GitHub Pages Deployment Script
# This script helps prepare your site for GitHub Pages deployment

echo "🚀 Preparing NECSI Astro Site for GitHub Pages Deployment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if astro.config.mjs exists
if [ ! -f "astro.config.mjs" ]; then
    echo "❌ Error: astro.config.mjs not found"
    exit 1
fi

echo "📝 Current configuration:"
echo "=========================="

# Extract current site and base URLs
SITE_URL=$(grep -o "'https://[^']*'" astro.config.mjs | head -1 | tr -d "'")
BASE_PATH=$(grep -o "base: '[^']*'" astro.config.mjs | cut -d"'" -f2)

echo "Site URL: $SITE_URL"
echo "Base Path: $BASE_PATH"
echo ""

# Check if configuration needs updating
if [[ "$SITE_URL" == *"yourusername"* ]] || [[ "$BASE_PATH" == *"necsi-astro-site"* ]]; then
    echo "⚠️  WARNING: Configuration contains placeholder values!"
    echo ""
    echo "Before deploying, please update astro.config.mjs with:"
    echo "1. Your actual GitHub username"
    echo "2. Your actual repository name"
    echo ""
    echo "Example:"
    echo "  site: 'https://john-doe.github.io'"
    echo "  base: '/my-necsi-site'"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to exit and update config first..."
fi

echo ""
echo "🔨 Building the site..."
echo "========================"

# Run the build command
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo ""
    echo "📁 Built files are in the 'dist/' directory"
    echo ""
    echo "🌐 Next steps for GitHub Pages:"
    echo "==============================="
    echo "1. Push your code to GitHub repository"
    echo "2. Go to repository Settings > Pages"
    echo "3. Select 'GitHub Actions' as source"
    echo "4. The workflow will automatically deploy your site"
    echo ""
    echo "🔗 Your site will be available at:"
    echo "   $SITE_URL$BASE_PATH"
    echo ""
    echo "📋 Files ready for deployment:"
    echo "   - dist/ (upload contents to any static host)"
    echo "   - .github/workflows/deploy.yml (for GitHub Actions)"
    echo ""
    echo "🎉 Ready for deployment!"
else
    echo ""
    echo "❌ Build failed! Please check the errors above."
    exit 1
fi
