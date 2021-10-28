<template lang="html">
  <v-container fill-height class="home flex-column justify-center align-center primary--text">
    <v-img src="@/assets/logo.png" max-height="140px" max-width="140px"></v-img>
    <h1>Welcome to the Speckle Revit Dashboard</h1>
    <p>This app allows you to analyse the data sent from Revit to Speckle.</p>
    <v-alert type="info" text color="primary">
      Check out the <a href="https://speckle.systems/blog" target="_blank">blog post</a> for more info!
    </v-alert>
    <p class="grey--text">Please log in to access you Speckle data.</p>
  </v-container>
</template>
<script>
export default {
  name: 'WelcomeView'
}
</script>
