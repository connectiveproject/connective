const path = require("path")

module.exports = {
  stories: [
    "../src/stories/*.stories.mdx",
    "../src/stories/*.stories.@(js|jsx|ts|tsx)",
  ],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-actions",
    "@storybook/addon-essentials",
    "@storybook/preset-scss",
  ],
  webpackFinal: async (config, { configType }) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      "@": path.resolve(__dirname, "../src/"),
      "~@": path.resolve(__dirname, "../src/"),
    }
    return config
  },
}
