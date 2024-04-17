const puppeteer = require('puppeteer');

async function getApplyLink(jobUrl) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  // Navigate to the job posting URL
  await page.goto(jobUrl);
  
  // Find the "Apply" button
  const applyButton = await page.$('.jobs-apply-button');
  
  // Click the button to trigger the JavaScript event
  await applyButton.click();
  
  // Wait for navigation to complete
  await page.waitForNavigation();
  
  // Get the URL after the click event
  const applyLink = page.url();
  
  await browser.close();
  
  return applyLink;
}

// Example usage
const jobUrl = 'https://www.linkedin.com/jobs/view/3871588853/?alternateChannel=search&refId=idY2xTvEOPXzQEF3U0zfXQ%3D%3D&trackingId=4n%2BzVl9ay8iloXgUBuuEJw%3D%3D';
getApplyLink(jobUrl)
  .then(applyLink => console.log("Job Application Link:", applyLink))
  .catch(error => console.error("Error:", error));
