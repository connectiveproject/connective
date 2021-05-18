module.exports = {
  devServer: {
    disableHostCheck: true,
  },

  transpileDependencies: ["vuetify"],

  pluginOptions: {
    i18n: {
      locale: "he",
      fallbackLocale: "he",
      localeDir: "locales",
      enableInSFC: false,
    },
  },
}
