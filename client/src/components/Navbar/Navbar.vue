<template>
  <v-toolbar dark prominent :src="bg">
    <v-tooltip v-for="btn in buttons" :key="btn.id" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn :data-testid="btn.id" icon v-bind="attrs" v-on="on" @click="btn.onClick">
          <v-icon>{{ btn.icon }}</v-icon>
        </v-btn>
      </template>
      <span> {{ btn.text() }} </span>
    </v-tooltip>
    <v-toolbar-title :class="{ absolute: $vuetify.breakpoint.mobile }">
      {{ $t("general.connective") }}
    </v-toolbar-title>
    <v-spacer />
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn large icon v-bind="attrs" v-on="on" @click="$router.go(-1)">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </template>
      <span v-text="$t('general.toThePreviousPage')" />
    </v-tooltip>
  </v-toolbar>
</template>

<script>
import { BACKGROUNDS } from "../../helpers/constants/images"
import { userToButtons } from "./constants"

export default {
  props: {
    userType: {
      type: String,
      required: true,
      validator(value) {
        return ["coordinator", "consumer", "instructor", "vendor"].includes(
          value
        )
      },
    },
  },
  data() {
    return {
      bg: BACKGROUNDS.navbar,
      buttons: userToButtons[this.userType],
    }
  },
}
</script>
