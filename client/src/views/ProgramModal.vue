<template>
  <v-row justify="center">
    <v-dialog v-if="program" :value="value" @input="close" width="540px">
      <v-card class="px-5">
        <v-card-title v-text="program.name" class="py-8 justify-center" />
        <v-card-text>
          <title-to-text
            v-if="program.organization"
            :text="program.organization"
            :title="$t('program.organization')"
          />
          <title-to-text
            v-if="program.targetAudience.length"
            :text="
              program.targetAudience.map(num => $t(`grades.${num}`)).join(', ')
            "
            :title="$t('program.targetAudience')"
          />
          <title-to-text
            v-if="program.description"
            :text="program.description"
            :title="$t('program.description')"
          />
          <title-to-text
            v-if="program.contactName"
            :text="program.contactName"
            :title="$t('program.contactName')"
          />
          <title-to-text
            v-if="program.phoneNumber"
            :text="program.phoneNumber"
            :title="$t('program.contactPhone')"
          />
          <title-to-text
            v-if="program.domain"
            :text="
              $t(
                `programFilters.${Object.keys(SERVER.domains).find(
                  key => SERVER.domains[key] === program.domain
                )}`
              )
            "
            :title="$t('program.domain')"
          />
          <tags-input
            :small="true"
            :editable="false"
            v-if="program.tags"
            :initialTags="program.tags"
          />
        </v-card-text>
        <carousel v-if="mediaList.length" :media-list="mediaList" />
        <v-card-actions class="py-6">
          <v-btn
            large
            class="mx-auto"
            v-text="$t('userActions.close')"
            color="orange"
            text
            @click="close"
          />
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { SERVER } from "../helpers/constants/constants"
import TitleToText from "../components/TitleToText"
import Carousel from "../components/Carousel"
import TagsInput from "@/components/TagsInput"

export default {
  components: { TitleToText, Carousel, TagsInput },
  props: {
    value: {
      // indicates whether dialog is open or not
      type: Boolean,
      required: true,
    },
    program: {
      type: Object,
      required: true,
    },
    mediaList: {
      type: Array,
      required: true,
    },
  },
  methods: {
    close() {
      this.$emit("input", false)
    },
  },
  data() {
    return {
      SERVER,
    }
  },
}
</script>

<style lang="scss" scoped>
.carousel {
  width: 85%;
}
</style>
