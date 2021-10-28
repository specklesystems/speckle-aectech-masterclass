<template>
  <v-sheet color="white" rounded class="pa-3" elevation="1">
    <v-row dense>
      <v-col v-for="i in 5" :key="i">
        <commit-button></commit-button>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script>
import CommitButton from "./CommitButton.vue"
export default {
  components: { CommitButton }
}
</script>

<style></style>
