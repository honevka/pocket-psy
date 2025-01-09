<template>
    <v-app>
      <v-container>
        <h1>Добро пожаловать в about!</h1>
    <v-text-field label="Введите текст"></v-text-field>
      </v-container>
    </v-app>
  </template>
  
  <script>
  export default {
    head() {
      return {
        title: 'Мое Nuxt приложение'
      }
    }
  }
  </script>