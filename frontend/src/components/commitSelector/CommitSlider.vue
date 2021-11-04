<template lang="html">
  <v-slide-group
    :value="selected"
    @change="$emit('update:selected', $event)"
    show-arrows
  >
    <v-slide-item
      v-for="n in commits"
      :key="n.id"
      v-slot="{ active, toggle }"
      :value="n"
    >
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-card
            v-bind="attrs"
            v-on="on"
            :color="active ? 'primary' : 'grey lighten-1'"
            :disabled="n.id === disabledId"
            :elevation="0"
            class="ma-1"
            @click="toggle"
            v-on:click="$emit('click:commit', n)"
          >
            <div class="d-flex fill-height justify-center align-center">
              <v-scale-transition mode="out-in">
                <div
                  class="d-flex flex-column justify-center align-center white--text ma-3"
                  v-if="!active"
                >
                  <v-avatar :size="30" class="mb-2">
                    <img :src="n.authorAvatar" />
                  </v-avatar>
                  <v-chip small color="primary" class="mb-4">
                    {{ appInitials(n.sourceApplication) }}
                  </v-chip>
                  <span style="writing-mode: vertical-rl;">
                    <timeago :datetime="n.createdAt"></timeago>
                  </span>
                </div>
                <div v-else class="ma-3">
                  <v-icon
                    color="white"
                    size="24"
                    v-text="'mdi-close-circle-outline'"
                  ></v-icon>
                </div>
              </v-scale-transition>
            </div>
          </v-card>
        </template>
        <span>{{ n.authorName }} — {{ n.message }}</span>
      </v-tooltip>
    </v-slide-item>
  </v-slide-group>
</template>

<script>
export default {
  props: ["selected", "commits", "disabledId"],
  methods: {
    appInitials(sourceApplication) {
      console.log(sourceApplication)
      switch (sourceApplication) {
        case "Rhino6":
        case "Rhino7":
          return "RH"
        case "Revit2019":
        case "Revit2020":
        case "Revit2021":
        case "Revit2022":
          return "RVT"
        case sourceApplication.startsWith("Autocad"):
          return "ACAD"
        case "Grasshopper":
          return "GH"
        default:
          break
      }
    }
  }
}
</script>

<style></style>
