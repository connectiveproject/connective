<script>
import ProgramsExplorer from "../../src/views/ProgramsExplorer/ProgramsExplorer"
import InfoCard from "@/components/InfoCard"


export default {
  extends: ProgramsExplorer,
  components: { InfoCard },
  mounted() {
    console.log("hi")
  }
}
</script>
