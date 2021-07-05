import { action } from "@storybook/addon-actions"
import Carousel from "../components/Carousel"

export default {
  title: "Carousel",
  component: Carousel,
}

const Template = args => ({
  components: { Carousel },
  methods: { action },
  data: () => ({ args }),
  template: `
    <carousel
    style="width: 650px;"
    class="mx-auto"
    :media-list="args.mediaList"
    />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  mediaList: [
    {
      mediaType: "image",
      imageUrl: "https://picsum.photos/200/300",
    },
    {
      mediaType: "video",
      videoUrl: "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    },
  ],
}
