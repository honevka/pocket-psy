<template>
    <v-app>
        
      <v-app-bar app
       height="80"
      >


      <v-container max-width="1200" fluid>
        <div class="d-flex align-center justify-space-between">
            <img
            src="../src/assets/logo.png"
            alt="Логотип"
            class='logo'
            transition='false'
            />
        <div>
      <v-btn  fluid variant="plain" class="font-idealist" to="/">Главная</v-btn>
      <v-btn  fluid variant="plain" class="font-idealist" to="/about">Мои записи</v-btn>
  
      </div>
      
        <div>
        <v-avatar  fluid ><v-icon size="40">mdi-account-circle</v-icon></v-avatar>
    </div>
</div>
    </v-container>
      </v-app-bar>

        <v-container style="padding-top: 80px;">
           <slot></slot>
        </v-container>

    </v-app>
  </template>

<style>
.logo{
  max-width: 200px;
}

</style>