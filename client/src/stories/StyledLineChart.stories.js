import StyledLineChart from "../components/StyledLineChart"

export default {
  title: "StyledLineChart",
  component: StyledLineChart,
}

const Template = args => ({
  components: { StyledLineChart },
  data: () => ({ args }),
  template: `
      <styled-line-chart
      :chart-data="args.chartData"
      :options="args.options"
      />
    `,
})

export const Primary = Template.bind({})
Primary.args = {
  chartData: {
    labels: [10, 11],
    datasets: [
      {
        label: "Data One",
        backgroundColor: "#f87979",
        data: [10, 11, 12, 13],
      },
      {
        label: "Data Two",
        backgroundColor: "#ddd979",
        data: [14, 11, 12, 13],
      },
    ],
  },
}
