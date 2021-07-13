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
            :text="program.targetAudience.join(', ')"
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
            :text="program.domain"
            :title="$t('program.domain')"
          />
        </v-card-text>
        <carousel
          v-if="mediaList.length"
          :media-list="mediaList"
        />
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
import TitleToText from "../components/TitleToText"
import Carousel from "../components/Carousel"

export default {
  components: { TitleToText, Carousel },
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
}
</script>

<style lang="scss" scoped>
.carousel {
  width: 85%;
}
</style>
