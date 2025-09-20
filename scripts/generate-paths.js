import fs from 'fs';
import path from 'path';

// Read all the JSON files and generate static paths
function generateStaticPaths() {
  const dataDir = path.join(process.cwd(), 'src', 'data');
  const paths = [];
  
  // Add the root path - for the home page, we don't need a slug
  // The home page is handled by index.astro, so we skip it here
  
  // Read all directories in the data folder
  const items = fs.readdirSync(dataDir, { withFileTypes: true });
  
  for (const item of items) {
    if (item.isDirectory()) {
      // Check if this directory has an index.json file
      const indexPath = path.join(dataDir, item.name, 'index.json');
      if (fs.existsSync(indexPath)) {
        paths.push({ params: { slug: item.name } });
      }
    }
  }
  
  return paths;
}

// Write the paths to a file that can be imported
const paths = generateStaticPaths();
const outputPath = path.join(process.cwd(), 'src', 'static-paths.json');

fs.writeFileSync(outputPath, JSON.stringify(paths, null, 2));
console.log(`Generated ${paths.length} static paths to ${outputPath}`);
