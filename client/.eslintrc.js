module.exports = {
  root: true,
  env: {
    node: true,
  },
  plugins: ["cypress"],
  extends: ["plugin:vue/essential", "eslint:recommended", "plugin:cypress/recommended"],
  parserOptions: {
    parser: "babel-eslint",
  },
  rules: {
    semi: ["error", "never"],
    "object-curly-spacing": ["error", "always"],
    "comma-spacing": ["error", { "before": false, "after": true }],
    "no-tabs": ["error", { allowIndentationTabs: false }],
    "no-console": process.env.NODE_ENV === "production" ? "error" : "warn",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "warn",
    indent: ["error", 2, { ignoredNodes: ["TemplateLiteral"], SwitchCase: 1 }],
    quotes: [
      "error",
      "double",
      { avoidEscape: true, allowTemplateLiterals: true },
    ],
  },
  overrides: [
    {
      files: [
        "**/__tests__/*.{j,t}s?(x)",
        "**/tests/unit/**/*.spec.{j,t}s?(x)",
      ],
      env: {
        jest: true,
      },
    },
  ],
}
