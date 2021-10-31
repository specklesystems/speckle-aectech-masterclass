<template lang="html">
  <v-sheet class="pa-4" elevation="8">
    <div>
      Compare commit
      <v-chip
        :close="currentCommit != null"
        @click:close="$emit('update:currentCommit', null)"
        @click="show_commit_selector = 'A'"
      >
        {{ currentCommit ? currentCommit.id : "Select commit" }}
      </v-chip>
      against
      <v-chip
        :close="prevCommit != null"
        @click:close="$emit('update:prevCommit', null)"
        @click="show_commit_selector = 'B'"
      >
        {{ prevCommit ? prevCommit.id : "Select commit" }}
      </v-chip>
      <v-btn
        color="success"
        :disabled="!currentCommit || !prevCommit"
        :loading="loading"
        @click="requestDiff"
      >
        Request diff
      </v-btn>
      <v-btn :disabled="!diffCommit" color="primary" @click="toggleDiffView">
        {{ showDiff ? "View commits" : "View diff" }}
      </v-btn>
    </div>

    <v-slide-group
      v-if="show_commit_selector == 'A'"
      :value="currentCommit"
      @change="$emit('update:currentCommit', $event)"
      center-active
      show-arrows
    >
      <v-slide-item
        v-for="n in commits"
        :key="n.id"
        v-slot="{ active, toggle }"
        :value="n"
        :disabled="prevCommit && n.id === prevCommit['id']"
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
              v-on:click="show_commit_selector = null"
              :disabled="prevCommit && n.id === prevCommit['id']"
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

    <v-slide-group
      v-else-if="show_commit_selector == 'B'"
      :value="prevCommit"
      @change="$emit('update:prevCommit', $event)"
      center-active
      show-arrows
    >
      <v-slide-item
        v-for="n in commits"
        :key="n.id"
        v-slot="{ active, toggle }"
        :value="n"
        :disabled="currentCommit && n.id === currentCommit['id']"
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-card
              v-bind="attrs"
              v-on="on"
              :color="active ? 'success' : 'primary lighten-1'"
              :disabled="currentCommit && n.id === currentCommit['id']"
              class="ma-1"
              height="100"
              width="40"
              @click="toggle"
              v-on:click="show_commit_selector = null"
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
  </v-sheet>
</template>

<script lang="js">
import { TOKEN } from "@/speckleUtils"

export default {
  name: "CommitPanel",
  components: {},
  props: ["commits", "diffCommit", "showDiff", "currentCommit", "prevCommit"],
  data() {
    return {
      show_commit_selector: null,
      loading: false,
    }
  },
  methods: {
    toggleDiffView(){
      this.$emit("update:showDiff", !this.showDiff)
    },
    async doesDiffExist(){
      console.log("diff check requested for", this.currentCommit.id, this.prevCommit.id)
      var diffUrl = `http://localhost:8000/diff_check/${this.$route.params.id}/${this.currentCommit.id}/${this.prevCommit.id}`
      var res = await fetch(diffUrl, {
        headers: {
          method: "GET",
          Authorisation: `Bearer ${localStorage.getItem(TOKEN)}`,
          "Content-type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      })
      return await res.json()
    },
    async requestDiff() {
      this.loading = true
      console.log("diff requested for", this.currentCommit.id, this.prevCommit.id)
      var diffUrl = `http://localhost:8000/diff/${this.$route.params.id}/${this.currentCommit.id}/${this.prevCommit.id}`
      var res = await fetch(diffUrl, {
        headers: {
          method: "GET",
          Authorisation: `Bearer ${localStorage.getItem(TOKEN)}`,
          "Content-type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      })
      if(res.status == 200){
        var body = await res.json()
        console.log("diff body", res, body)
        this.$emit("update:diffCommit", body.commit)
      }
      this.loading = false
    },
  },
  watch: {
    currentCommit: {
      handler: async function(newVal, oldVal) {
        this.$emit("current-commit", newVal)
        this.loading = true
        if(newVal && this.prevCommit){
          var diffRes = await this.doesDiffExist()
          console.log(diffRes)
          if(diffRes.exists)
            this.$emit("update:diffCommit", diffRes.commit)
        }
        this.loading = false
      }
    },
    prevCommit: {
      handler: async function(newVal, oldVal){
        this.$emit("prev-commit", newVal)
        this.loading = true
        if(newVal && this.currentCommit){
          var diffRes = await this.doesDiffExist()
          console.log(diffRes)
          if(diffRes.exists)
            this.$emit("update:diffCommit", diffRes.commit)
        }
        this.loading = false
      }
    }
  }
}
</script>

<style></style>
