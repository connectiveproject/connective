<template>
  <v-menu v-model="menu" offset-x>
    <template v-slot:activator="{ on, attrs }">
      <v-sheet
        class="d-flex justify-space-between avatar-wrapper"
        color="transparent"
        icon
        v-bind="attrs"
        v-on="on"
      >
        <v-icon :class="{ rotate: menu }" size="55" dark>
          mdi-menu-down
        </v-icon>
        <avatar
          v-bind="attrs"
          v-on="on"
          class="avatar cursor-pointer"
          :avatar-options="avatarOptions"
        />
        <v-badge bordered color="error" icon="mdi-bell" overlap v-if="hasNew" />
      </v-sheet>
    </template>
    <v-card>
      <v-list>
        <v-list-item>
          <v-list-item-avatar>
            <avatar :avatar-options="avatarOptions" />
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title v-text="name" />
            <v-list-item-subtitle v-text="email" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider />
      <v-list class="pb-5">
        <v-list-item-group>
          <v-list-item
            v-for="btn in buttons"
            :key="btn.id"
            :data-testid="btn.id"
            @click="btn.onClick"
          >
            <v-list-item-icon>
              <v-icon color="primary" v-text="btn.icon" />
              <v-badge
                bordered
                color="error"
                v-if="alertVisible(btn)"
                dot
                overlap
              />
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="btn.text" />
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </v-menu>
</template>

<script>
import Avatar from "@/components/Avatar/Avatar"
import { mapState } from "vuex"
import { VUEX_STATE } from "@/helpers/constants/constants"

export default {
  components: { Avatar },
  computed: {
    ...mapState("notification", ["hasNew"]),
  },
  props: {
    avatarOptions: {
      type: Object,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    email: {
      type: String,
      required: true,
    },
    buttons: {
      // [ { text: string, icon: string, onClick: function } ]
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      menu: false,
    }
  },
  methods: {
    alertVisible(btn) {
      if (!btn.alert) {
        return false
      }
      if (btn.alert === VUEX_STATE.notificationHasNew) {
        return this.hasNew
      }
      return false
    },
  },
}
</script>
<style scoped>
.avatar {
  width: 80px;
}
.avatar-wrapper {
  transition: transform 0.3s;
}
.avatar-wrapper:hover {
  transform: scale(1.1);
}
.rotate {
  transform: rotate(-180deg);
}
</style>
