<template>
  <v-toolbar dark prominent :src="bg">
    <v-tooltip v-for="btn in buttons" :key="btn.id" bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          :data-testid="btn.id"
          icon
          v-bind="attrs"
          v-on="on"
          @click="btn.onClick"
        >
          <v-icon>{{ btn.icon }}</v-icon>
        </v-btn>
      </template>
      <span> {{ btn.text() }} </span>
    </v-tooltip>
    <v-toolbar-title :class="{ absolute: $vuetify.breakpoint.mobile }">
      {{ $t("general.connective") }}
    </v-toolbar-title>
    <v-spacer />
    <v-menu
      v-model="menu"
      offset-x
    >
      <template v-slot:activator="{ on, attrs }">
        <v-sheet icon v-bind="attrs" v-on="on">
          <avatar
            v-bind="attrs"
            v-on="on"
            style="width: 75px"
            :avatar-options="profile.profilePicture"
            class="cursor-pointer"
          />
        </v-sheet>
      </template>

      <v-card>
        <v-list>
          <v-list-item>
            <v-list-item-avatar>
              <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title v-text="name" />
              <v-list-item-subtitle v-text="email" />
            </v-list-item-content>

            <v-list-item-action>
              <v-btn :class="fav ? 'red--text' : ''" icon @click="fav = !fav">
                <v-icon>mdi-heart</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
          <v-list-item>
            <v-list-item-action>
              <v-switch v-model="message" color="purple"></v-switch>
            </v-list-item-action>
            <v-list-item-title>Enable messages</v-list-item-title>
          </v-list-item>

          <v-list-item>
            <v-list-item-action>
              <v-switch v-model="hints" color="purple"></v-switch>
            </v-list-item-action>
            <v-list-item-title>Enable hints</v-list-item-title>
          </v-list-item>
        </v-list>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="menu = false"> Cancel </v-btn>
          <v-btn color="primary" text @click="menu = false"> Save </v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </v-toolbar>
</template>

<script>
import { mapState } from "vuex"
import Avatar from "../Avatar/Avatar"
import { BACKGROUNDS } from "../../helpers/constants/images"
import { userToButtons } from "./constants"

export default {
  components: { Avatar },
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

      fav: true,
      menu: false,
      message: false,
      hints: true,
    }
  },
  computed: {
    ...mapState("coordinator", ["profile"]),
    ...mapState("user", ["name", "email"]),
  },
}
</script>
