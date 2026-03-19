module.exports = {
  enable: process.env.ENVIRONMENT === "production",
  mode: "random",
  buildFolderPath: ".next",
  refreshFileTypes: ["js", "css", "html"],
  whiteListedFolderPaths: [],
  blackListedFolderPaths: [],
}