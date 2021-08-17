function createBackendUrl() {
  if (process.env.NODE_ENV === "development") {
    if (process.env.GITPOD_WORKSPACE_URL) {
      return `https://8000-${process.env.GITPOD_WORKSPACE_URL.slice(8)}/api`
    }
    return "http://localhost:8000/api"
  }
  if (process.env.NODE_ENV === "sandbox") {
    return "https://young-fortress-53072.herokuapp.com/api"
  }
  return "https://calm-hamlet-63949.herokuapp.com/api"
}

process.env.VUE_APP_BACKEND_URL = createBackendUrl()

module.exports = {
  devServer: {
    disableHostCheck: true,
  },
  transpileDependencies: ["vuetify"],
  pages: {
    index: {
      entry: "src-2/main.js",
      title: "Connective",
    },
  },
  pluginOptions: {
    i18n: {
      locale: "he",
      fallbackLocale: "he",
      localeDir: "locales",
      enableInSFC: false,
    },
  },
}
