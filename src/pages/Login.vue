<style lang="css">
.login-card {
  min-width: 400px;
}
.bg-page {
  background: url(assets/login-bg.jpg);
  background-size: cover;
  background-position: 80% 20%;
}
</style>
<template>
  <q-page class="flex flex-center bg-page"
    ><q-card class="my-card bg-blue-grey-9  text-white login-card" bordered>
      <q-form @submit="login">
        <q-card-section>
          <div class="text-h6" align="center">3D OrganixInsight</div>
        </q-card-section>

        <q-card-section>
          <q-input
            outlined
            bg-color="white"
            placeholder="Enter Username"
            label="Username"
            v-model="username"
            required
          />
          <br />
          <q-input
            type="password"
            outlined
            bg-color="white"
            placeholder="Enter Password"
            label="Password"
            v-model="password"
            required
          />
        </q-card-section>
        <q-card-section>
          <div class="q-gutter-sm">
            <!-- <q-checkbox v-model="user" label="User" color="grey-8" :disable="admin==true"/>
            <q-checkbox v-model="admin" label="Admin" color="grey-8" :disable="user==true"/> -->
          </div>
        </q-card-section>

        <q-card-section v-if="error">
          <q-banner inline-actions class="text-white bg-red" dense>
            {{ error }}
          </q-banner>
        </q-card-section>
        <q-separator dark />

        <q-card-actions class="text-center" > <q-btn type="submit" flat>Login</q-btn> </q-card-actions>
      </q-form>
    </q-card>
  </q-page>
</template>
<script>
import { Platform, Dialog } from 'quasar'
import { STORAGE_TOKEN } from "src/constants";
import API from "../api.js";

export default {
  data: () => ({
    username: "",
    password: "",
    error: null,
    // user:true,
    // admin:false
  }),
  methods: {
    async login() {
      const result = await API("auth.login", {
        username: this.username,
        password: this.password,
      });

      if (result && result.error) {
        return (this.error = result.error);
      }


      // // //if Role admin==>gotoHome
      // if(result  && result.role=="admin"){
      // localStorage.setItem(STORAGE_TOKEN_ADMIN, result.token);
      // this.error = null;
      // this.$router.push("admin");
      // }

      // if(result && result.role=="user"){
      // localStorage.setItem(STORAGE_TOKEN, result.token);
      // this.error = null;
      // this.$router.push("design");
      // }
      if (result && result.token) {
      localStorage.setItem(STORAGE_TOKEN, result.token);
      localStorage.setItem("username", this.username);
      this.error = null;

      if (result.role === "admin") {
        this.$router.push("/admin");
      } else if (result.role === "user") {
        this.$router.push("/design");
      } else {
        this.error = "Unknown role. Please contact support.";
      }
    } else {
      this.error = "Login failed. Please try again.";
    }

    },

    showBrowserNotification() {
      if (Platform.is.mobile && !Platform.is.cordova) {
        const dialog = Dialog.create({
          title: 'Please Open in Browser',
          message: 'For a better experience, we recommend accessing this app through a desktop browser on a laptop or desktop computer.',
          persistent: true,

          ok: {
        label: 'Warnig',
        color: 'red',
        handler: () => {
          // Do nothing, effectively preventing the dialog from being closed
        }
      }

        });

        dialog.onDismiss(() => {
          dismiss(false);
      // Do nothing, effectively preventing the dialog from being closed
    });

      }
    }

  },

  async mounted() {
    // API("auth.createUser", { username: "sample", password: "123", role: "user" });
    // API("auth.createUser", { username: "laborganix", password: "laborganix123!@#", role: "user" });
    this.showBrowserNotification();
  }

};
</script>
