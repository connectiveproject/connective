module.exports = {
  stories: ["../src/stories/*.stories.mdx", "../src/stories/*.stories.@(js|jsx|ts|tsx)"],
  addons: [
    "@storybook/addon-links",
    "@storybook/addon-essentials",
    '@storybook/preset-scss'
  ],
  webpackFinal: async (config, { configType }) => {
    config.module.rules.push({
      // this is for both css and scss
      test: /.*\.(?:c|sc)ss$/,
      loaders: ["css-loader", "resolve-url-loader", "sass-loader"],
    })
    return config
  },
}
