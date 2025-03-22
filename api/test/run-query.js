#!/usr/bin/env node

/**
 * This script runs a query against the chatbot API and displays the results.
 * Usage: npm run test-query "your query here" "http://your-api-url.com"
 */

import { configureApi, streamChat } from '../api.ts';

// Get the query and API URL from command line arguments
const query = process.argv[2];
const apiUrl = process.argv[3] || 'http://localhost:3000';

if (!query) {
  console.error('Error: No query provided');
  console.error('Usage: npm run test-query "your query here" "http://your-api-url.com"');
  process.exit(1);
}

console.log(`Using API URL: ${apiUrl}`);
console.log(`\n🔍 Testing query: "${query}"\n`);

// Configure the API with the provided URL
configureApi(apiUrl);

async function runQuery() {
  try {
    // Use our SDK's streamChat function instead of raw fetch
    for await (const response of streamChat(query, false)) {
      if (response.text) {
        console.log(response.text);
      } else if (response.content) {
        console.log(response.content);
      }
      
      if (response.done) {
        console.log('\n✅ Query test completed successfully');
      }
    }
  } catch (error) {
    console.error('\n❌ Error during test:', error);
    process.exit(1);
  }
}

// Run the query
runQuery(); 