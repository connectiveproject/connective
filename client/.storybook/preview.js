import "!style-loader!css-loader!sass-loader!../src/styles/main.scss"
// import vuetify from '@/plugins/vuetify';     

export const parameters = {
  actions: { argTypesRegex: "^on[A-Z].*" },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
}

// export const decorators = [
//   Story => (
//     <div style={{ margin: "3em" }}>
//       <Story />
//     </div>
//   ),
// ]
