import Utils from "../helpers/utils"
import ActionsCalendar from "../components/ActionsCalendar"
import moment from "moment"

export default {
  title: "ActionsCalendar",
  component: ActionsCalendar,
}

const Template = args => ({
  components: { ActionsCalendar },
  data: () => ({ args }),
  template: `
      <actions-calendar
      v-model="args.value"
      first-interval="5"
      interval-count="19"
      :displayType.sync="args.displayType"
      :events="args.events"
      />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  displayType: "week",
  value: "",
  events: [
    {
      name: "תופסים פוקימונים בפארק הירקון",
      start: moment().toDate(),
      end: moment().add(2, "hours").toDate(),
      timed: true,
      color: Utils.stringToPsuedoRandomColor("תופסים פוקימונים בפארק הירקון"),
    },
    {
      name: "ראיון עבודה",
      start: moment().add(1, "hours").toDate(),
      end: moment().add(3, "hours").toDate(),
      timed: true,
      color: Utils.stringToPsuedoRandomColor("ראיון עבודה"),
    },
    {
      name: "על האש בפארק לאומי",
      start: moment().subtract(15, "hours").toDate(),
      end: moment().subtract(10, "hours").toDate(),
      timed: true,
      color: Utils.stringToPsuedoRandomColor("על האש בפארק לאומי"),
    },
    {
      name: "טורניר שחמט אקטיבי",
      start: moment().add(100, "hours").toDate(),
      end: moment().add(103, "hours").toDate(),
      timed: true,
      color: Utils.stringToPsuedoRandomColor("טורניר שחמט אקטיבי"),
    },
    {
      name: "יום כיף בפתח תקווה",
      start: moment().add(300, "hours").toDate(),
      end: moment().add(306, "hours").toDate(),
      timed: true,
      color: Utils.stringToPsuedoRandomColor("יום כיף בפתח תקווה"),
    },
  ]
}
