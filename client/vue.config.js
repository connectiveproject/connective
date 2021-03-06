function createBackendBaseUrl() {
  if (process.env.NODE_ENV === "development") {
    if (process.env.GITPOD_WORKSPACE_URL) {
      return `https://8000-${process.env.GITPOD_WORKSPACE_URL.slice(8)}/`
    }
    return "http://localhost:8000/"
  }
  if (process.env.NODE_ENV === "sandbox") {
    return "https://young-fortress-53072.herokuapp.com/"
  }
  return "https://calm-hamlet-63949.herokuapp.com/"
}

function getDevelopmentFrontHost() {
  if (process.env.NODE_ENV === "development") {
    if (process.env.GITPOD_WORKSPACE_URL && process.env.GITPOD_WORKSPACE_URL.includes("gitpod.io")) {
      return `8080-${process.env.GITPOD_WORKSPACE_URL.slice(8)}`
    }
    return ["localhost"]
  }
  return null
}

process.env.VUE_APP_BACKEND_URL = process.env.VUE_APP_BACKEND_URL || `${createBackendBaseUrl()}api`
process.env.VUE_APP_ANALYTICS_WRITE_KEY = process.env.VUE_APP_ANALYTICS_WRITE_KEY || "G9jJ5vXWzYyqp777CBQA1783LxRJEyWI"

module.exports = {
  devServer: {
    allowedHosts: getDevelopmentFrontHost()
  },
  transpileDependencies: ["vuetify"],
  pages: {
    index: {
      entry: "src/main.js",
      title: "Connective",
    },
  },
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "./src/styles/main.scss";`,
      },
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
