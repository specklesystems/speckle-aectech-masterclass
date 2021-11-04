<template lang="html">
  <v-sheet class="pa-4" elevation="8">
    <div class="d-flex align-center">
      <span style="white-space: nowrap;">
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
      </span>
      <div class="pl-2">
        <v-btn
          v-if="!diffCommit"
          color="success"
          :disabled="!currentCommit || !prevCommit"
          :loading="loading"
          @click="requestDiff"
        >
          Request diff
        </v-btn>
        <v-btn
          v-else
          :loading="loading"
          color="primary"
          @click="toggleDiffView"
        >
          {{ showDiff ? "View commits" : "View diff" }}
        </v-btn>
      </div>
    </div>
    <commit-slider
      v-if="show_commit_selector == 'A'"
      :commits="commits"
      :selected="currentCommit"
      :disabled-id="prevCommit ? prevCommit.id : null"
      @update:selected="$emit('update:currentCommit', $event)"
      @click:commit="show_commit_selector = null"
    />
    <commit-slider
      v-if="show_commit_selector == 'B'"
      :commits="commits"
      :selected="prevCommit"
      :disabled-id="currentCommit ? currentCommit.id : null"
      @update:selected="$emit('update:prevCommit', $event)"
      @click:commit="show_commit_selector = null"
    />
  </v-sheet>
</template>

<script lang="js">
import { TOKEN } from "@/speckleUtils"
import CommitSlider from "@/components/commitSelector/CommitSlider.vue"
export default {
  name: "CommitPanel",
  components: { CommitSlider },
  props: ["commits", "diffCommit", "showDiff", "currentCommit", "prevCommit"],
  data() {
    return {
      show_commit_selector: null,
      loading: false,
    }
  },
  methods: {
    async doesDiffExist(){
      console.log("Checking if diff exists...")
      // TODO: Missing implementation
      return { commit: null }
    },
    async requestDiff() {
      console.log("Requesting diff...")
      // TODO: Missing implementation
    },
    toggleDiffView(){
      this.$emit("update:showDiff", !this.showDiff)
    },
    async handleCommitChange(event, value){
      this.loading = true
      this.$emit(event, value)
      this.$emit("update:diff-commit", null)
      if(value){
        var diffRes = await this.doesDiffExist()
        this.$emit("update:diff-commit", diffRes.commit)
      }
      this.loading = false
    }
  },
  watch: {
    currentCommit: {
      handler: async function(newVal, oldVal) {
        this.handleCommitChange("current-commit", newVal)
      }
    },
    prevCommit: {
      handler: async function(newVal, oldVal){
        this.handleCommitChange("prev-commit", newVal)
      }
    }
  }
}
</script>

<style></style>
