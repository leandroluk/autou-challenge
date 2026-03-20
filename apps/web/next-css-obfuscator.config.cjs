/** @type {import('next-css-obfuscator').Options} */
module.exports = {
  enable: true,
  mode: "simplify",
  buildFolderPath: ".next",
  refreshClassConversionJson: true,
  allowExtensions: [".jsx", ".tsx", ".js", ".ts", ".html", ".rsc"],
  blackListedFolderPaths: [
    "./.next/cache",
    /\.next\/server\/pages\/api/,
    /_document..*js/,
    /_app-.*/,
    /__.*/,
  ],
  ignorePatterns: {
    selectors: ["dark"],
    idents: [],
  },
  removeOriginalCss: true,
  logLevel: "error",
};