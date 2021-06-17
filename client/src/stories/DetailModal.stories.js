import { action } from "@storybook/addon-actions"
import DetailModal from "../components/DetailModal.vue"

export default {
  title: "DetailModal",
  component: DetailModal,
}

const Template = args => ({
  components: { DetailModal },
  methods: { action },
  data: () => ({ args }),
  template: `
    <div>
      <detail-modal
      class="mx-auto"
      v-bind="args"
      v-model="args.value"
      @input="action('input')()"
      >
      {{ args.defaultSlot }}
      </detail-modal>

      <div v-if="!args.value" class="my-16">
        <v-btn
          class="d-block mx-auto"
          @click="e => { args.value = true }"
        >
          Open
        </v-btn>
        <div class="text-center pt-10">
        (button is for demonstration purposes only)
        </div>
      </div>
    </div>
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  value: true,
  topSubtitle: "שיר השבוע",
  title: "מסיבה",
  bottomSubtitle: "יסמין מועלם",
  buttonText: "תוציאו אותי מפה",
  defaultSlot:
    "למה שאתה תגיד לי איך עושים את זה נכון \
      זה זורם בי כמו הדם בוריד שלי, כמו הים התיכון \
      הכל כחול אני כל יכולה \
      השגחה מלמעלה \
      אם משהו לא בא אז הוא לא בא מסיבה \
      לא בא מסיבה. \
      \n\n\
      ולמה שאתה תגיד לי איך עושים את זה נכון \
    אם זה זורם בי כמו הדם בוריד שלי, כמו הים התיכון \
    הכל כחול אני כל יכולה \
    השגחה מלמעלה \
    אם משהו לא בא אז הוא לא בא מסיבה \
    לא בא מסיבה.",
}
