const path = require("path")

module.exports = {
  stories: [
    "../src/stories/*.stories.mdx",
    "../src/stories/*.stories.@(js|jsx|ts|tsx)",
  ],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    "@storybook/preset-scss",
  ],
  webpackFinal: async (config, { configType }) => {
    config.module.rules.push({
      test: /.*\.(?:c|sc)ss$/,
      loaders: ["css-loader", "sass-loader"],
    })
    config.resolve.alias = {
      ...config.resolve.alias,
      "~@": path.resolve(__dirname, "../src/"),
    }
    return config
  },
}
