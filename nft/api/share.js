export default function handler(req, res) {
  const { img, course } = req.query;

  // This simple HTML returns the required OpenGraph meta tags so Twitter and LinkedIn can fetch the image
  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      
      <!-- OpenGraph Meta Tags for LinkedIn / Facebook -->
      <meta property="og:title" content="Verified Certificate for ${course}" />
      <meta property="og:description" content="I just verified my blockchain credential on CertiChain!" />
      <meta property="og:image" content="${img}" />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      
      <!-- Twitter Card Meta Tags -->
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content="Verified Certificate for ${course}" />
      <meta name="twitter:description" content="I just verified my blockchain credential on CertiChain!" />
      <meta name="twitter:image" content="${img}" />
      
      <title>Certificate - ${course}</title>
      <script>
        // Once the crawler is done, real users who click the link get redirected to the actual Verify page
        window.location.href = "/verify";
      </script>
    </head>
    <body>
      Loading Certificate...
    </body>
    </html>
  `;

  res.setHeader('Content-Type', 'text/html');
  res.status(200).send(html);
}
