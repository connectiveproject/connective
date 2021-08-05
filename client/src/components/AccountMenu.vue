<template>
  <v-menu v-model="menu" offset-x>
    <template v-slot:activator="{ on, attrs }">
      <v-sheet color="transparent" icon v-bind="attrs" v-on="on">
          <avatar
            v-bind="attrs"
            v-on="on"
            class="avatar cursor-pointer"
            :avatar-options="avatarOptions"
          />
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
            @click="btn.onClick"
          >
            <v-list-item-icon>
              <v-icon color="primary" v-text="btn.icon" />
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
import Avatar from "./Avatar/Avatar"

export default {
  components: { Avatar },
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
}
</script>
<style scoped>
.avatar {
  transition: transform 0.3s;
  width: 75px;
}
.avatar:hover {
  transform: scale(1.1);
}
</style>
