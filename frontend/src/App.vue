<template lang="html">
  <v-app>
    <v-app-bar app color="primary" dark dense>
      <v-btn text link to="/" small>
        <v-img class="mr-2" src="@/assets/img.png" height="14" width="14" />
        <v-badge
          offset-y="7px"
          offset-x="0px"
          color="error"
          content="master class"
        >
          <h3 class="text--white">AEC Tech</h3>
        </v-badge>
      </v-btn>

      <v-spacer></v-spacer>

      <stream-search
        v-if="isAuthenticated"
        @selected="$router.push(`/streams/${$event.id}`)"
      />

      <v-spacer></v-spacer>

      <div>
        <v-tooltip left>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              x-small
              v-bind="attrs"
              v-on="on"
              icon
              link
              href="https://speckle.community"
              target="_blank"
              class="mr-3"
            >
              <v-icon size="x-large">mdi-help-circle-outline</v-icon>
            </v-btn>
          </template>
          <span>
            Have any questions?
            <b>Join our Community!</b>
          </span>
        </v-tooltip>
      </div>

      <v-btn
        class="ma-2"
        small
        outlined
        v-if="!isAuthenticated"
        @click="$store.dispatch('redirectToAuth')"
      >
        <v-img class="mr-2" src="@/assets/img.png" height="14" width="14" />
        <span>Login/Register</span>
      </v-btn>
      <v-menu v-else offset-y open-on-hover>
        <template v-slot:activator="{ on, attrs }">
          <v-avatar v-bind="attrs" v-on="on" size="32" color="grey lighten-3">
            <v-img
              v-if="$store.state.user.avatar"
              :src="$store.state.user.avatar"
            />
            <v-img
              v-else
              :src="`https://robohash.org/${$store.user.id}.png?size=32x32`"
            />
          </v-avatar>
        </template>
        <v-list dense nav subheader id="login-menu">
          <v-subheader class="caption">Logged in as:</v-subheader>
          <p class="caption ml-3 mb-1">
            {{ $store.state.user.name }}
            <span v-if="$store.state.user.email">
              ({{ $store.state.user.email }})
            </span>
          </p>
          <v-divider class="ma-1"></v-divider>
          <v-list-item link :href="`${serverUrl}/profile`" target="_blank">
            <v-list-item-title>Go to profile</v-list-item-title>
            <v-list-item-icon>
              <v-icon small>mdi-account</v-icon>
            </v-list-item-icon>
          </v-list-item>
          <v-list-item link @click="$store.dispatch('logout')">
            <v-list-item-title class="error--text">Log out</v-list-item-title>
            <v-list-item-icon>
              <v-icon small color="error">mdi-logout</v-icon>
            </v-list-item-icon>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <transition name="fade">
        <router-view />
      </transition>
    </v-main>
  </v-app>
</template>

<script>
import StreamSearch from "@/components/StreamSearch"

export default {
  name: "App",
  components: { StreamSearch },
  data() {
    return {
      serverUrl: process.env.VUE_APP_SERVER_URL
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated
    }
  }
}
</script>

<style lang="scss">
$heading-font-family: "Space Grotesk";

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */
 {
  opacity: 0;
}

.floating {
  position: fixed;
  top: 4em;
  right: 2em;
  z-index: 1;
}
</style>
