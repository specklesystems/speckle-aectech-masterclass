<template lang="html">
  <v-sheet class="pa-4" elevation="8">
    <p>Compare commit</p>
    <v-row dense no-gutters>
      <v-col cols="6">
        <v-slide-group v-model="commitA" center-active show-arrows>
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
                  :color="active ? 'success' : 'primary lighten-1'"
                  class="ma-1"
                  height="100"
                  width="40"
                  @click="toggle"
                >
                  <div class="d-flex fill-height justify-center align-center">
                    <v-scale-transition mode="out-in">
                      <span v-if="!active" style="writing-mode: vertical-rl;">
                        {{ n.id }}
                      </span>
                      <v-icon
                        v-else
                        color="white"
                        size="20"
                        v-text="'mdi-close-circle-outline'"
                      ></v-icon>
                    </v-scale-transition>
                  </div>
                </v-card>
              </template>
              <span>{{ n.message }}</span>
            </v-tooltip>
          </v-slide-item>
        </v-slide-group>
      </v-col>
      <v-col cols="6">
        <v-slide-group v-model="commitB" center-active show-arrows>
          <v-slide-item
            v-for="n in commits"
            :key="n.id"
            v-slot="{ active, toggle }"
            :value="n"
            :disabled="commitA && n.id === commitA['id']"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-card
                  v-bind="attrs"
                  v-on="on"
                  :color="active ? 'success' : 'primary lighten-1'"
                  class="ma-1"
                  height="100"
                  width="40"
                  @click="toggle"
                  :disabled="commitA && n.id === commitA['id']"
                >
                  <div class="d-flex fill-height justify-center align-center">
                    <v-scale-transition mode="out-in">
                      <span v-if="!active" style="writing-mode: vertical-rl;">
                        {{ n.id }}
                      </span>
                      <v-icon
                        v-else
                        color="white"
                        size="20"
                        v-text="'mdi-close-circle-outline'"
                      ></v-icon>
                    </v-scale-transition>
                  </div>
                </v-card>
              </template>
              <span>{{ n.message }}</span>
            </v-tooltip>
          </v-slide-item>
        </v-slide-group>
      </v-col>
      <div>
        You are about to compare commit
        <v-chip :close="commitA" @click:close="commitA = null">
          {{ commitA ? commitA.id : "Select commit" }}
        </v-chip>
        against
        <v-chip :close="commitB" @click:close="commitB = null">
          {{ commitB ? commitB.id : "Select commit" }}
        </v-chip>
        <v-btn color="success" :disabled="!commitA || !commitB">
          Run this!
        </v-btn>
      </div>
    </v-row>
  </v-sheet>
</template>

<script>
export default {
  name: "CommitPanel",
  components: {},
  props: ["commits"],
  data() {
    return {
      commitA: null,
      commitB: null
    }
  }
}
</script>

<style></style>
