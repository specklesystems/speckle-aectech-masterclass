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
    toggleDiffView(){
      this.$emit("update:showDiff", !this.showDiff)
    },
    async doesDiffExist(){
      if(!this.currentCommit || !this.prevCommit) return { commit: null }
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
