import InfoCard from "../components/InfoCard.vue"

export default {
  title: "InfoCard",
  component: InfoCard,
}

const Template = args => ({
  components: { InfoCard },
  data() {
    return { args }
  },
  template: `<info-card v-bind="args" />`,
})

export const Primary = Template.bind({})
Primary.args = {
  imgUrl: "https://picsum.photos/200/300",
  title: "כותרת",
  subtitle: "תת כותרת",
  body: `Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus dictum ipsum eleifend sem egestas, vel consequat sapien porttitor. Pellentesque tristique nunc turpis, non rutrum urna gravida vitae. Ut dolor nibh, semper ut pellentesque ut, dictum ut neque. Maecenas dignissim ultrices scelerisque. Suspendisse felis enim, luctus sed rutrum sit amet, viverra ac quam. Vestibulum et eros et purus ornare viverra non quis velit. Mauris hendrerit eros ut nibh elementum, at vulputate dui fermentum. Praesent porta diam a purus tempor euismod. Integer ligula lectus, elementum vel arcu ac, porta consectetur ante.
  Donec ultricies pulvinar lacus, in viverra ante porttitor vel. Aliquam hendrerit ipsum ut porttitor vestibulum. Donec id pellentesque augue. Vestibulum at elementum quam, at facilisis odio. Integer pellentesque ut nibh et dignissim. Nullam vel metus nec lorem tincidunt maximus. Nullam metus nibh, hendrerit sodales pharetra nec, euismod eu lacus. Vestibulum a varius purus, eleifend iaculis orci. Praesent bibendum mollis dignissim. Praesent vehicula justo quis laoreet congue. Proin nulla odio, rutrum sed ex vitae, placerat dapibus eros. Duis vel libero quis velit ultricies porttitor vitae vel ligula. Sed in nunc id mi tincidunt faucibus at non lorem. Morbi interdum varius pellentesque. Aliquam erat volutpat. Morbi mauris ante, varius aliquet quam in, ornare ultrices neque.`,
}
