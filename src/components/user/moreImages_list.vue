<template>
  <div class="q-pa-md">
    <!-- <q-card-section class="row ">
          <q-space/>
          <q-btn icon="close"  round dense v-close-popup />
        </q-card-section> -->
    <q-btn
      push
      color="teal"
      class="q-mb-md"
    >{{ file_name }} </q-btn>

  <br>


    <div v-if="exp_typeo==='3D Simple Experiment' || exp_typeo === '3D Experiment' || exp_typeo === '3D morphogenesis' ">
    <q-img
      v-for="(url, index) in urls"
      :key="index"
      :src="url"
      style="max-width: 100%; height: 500px; width: 500px; position: relative; cursor: pointer;"
      ratio="1"
      spinner-color="white"
      class="rounded-borders q-mr-sm q-mb-sm"
      @click="toggleZoom(index)"
      @mouseleave="zoomOut(index)"
      :class="{ 'zoomed': zoomed.includes(index) }"
    >
      <q-badge class="badge-left">{{ index + 1 }}</q-badge>
    </q-img>
  </div>

    <div v-if="exp_typeo==='2D Simple Experiment' || exp_typeo === '2D Experiment' ">
    <q-img
      v-for="(url, index) in urls"
      :key="index"
      :src="url"
      style="max-width: 80%; height: 400px; width: 500px; position: relative; cursor: pointer;"
      ratio="1"
      spinner-color="white"
      class="rounded-borders q-mr-sm q-mb-sm"
      @click="toggleZoom(index)"
      @mouseleave="zoomOut(index)"
      :class="{ 'zoomed': zoomed.includes(index) }"
    >
      <q-badge class="badge-left">{{ index + 1 }}</q-badge>
    </q-img>
  </div>

  <!-- <div v-if="exp_typeo==='2D Simple Experiment' || exp_typeo === '3D Doss Response (LR)' || exp_typeo === '2D Doss Response'  ">
    <q-img
        v-for="(url, index) in urls"
        :key="index"
        :src="url"
        class="rounded-borders q-mr-sm q-mb-sm"
        spinner-color="white"
        @click="toggleZoom(index)"
        @mouseleave="zoomOut(index)"
        ratio="1"
        style="max-width: 100%; height: 300px; width: 300px; position: relative; cursor: pointer;"
      >
        <q-badge class="badge-left">{{ index + 1 }}</q-badge>
      </q-img>

  </div> -->







  </div>


  <div>
    <q-dialog v-model="show_3dimge_dialog" >
        <q-card style="width: 2000px; max-width: 2000px">

          <q-card-section align="center" >
            <div class="row text-center">
            </div>
          </q-card-section>
        </q-card>
      </q-dialog>
  </div>
</template>

<script>
 import API from "src/api";
 import { ref } from "vue";
  import { exportFile, useQuasar } from "quasar";
export default {

  components: {},  props: {

experiment_id: String,
file_name: String,
exp_type:String,

},

  data() {

    return {
      show_3dimge_dialog:ref(false),
      show_dialog: false,
      currentImageColor: 'red',
      urls:[],
      zoomed: [],
      exp_typeo:null,
      f_name:"",
      url:require('/src/assets/cc.jpg'),
      transitions: [
          'slide-right',
          'slide-left',
          'slide-up',
          'slide-down',
          'fade',
          'scale',
          'rotate',
          'flip-right',
          'flip-left',
          'flip-up',
          'flip-down',
          'jump-right',
          'jump-left',
          'jump-up',
          'jump-down',
          'slide-right',
          'slide-left',
          'slide-up',
          'slide-down',
          'fade',
          'scale',
          'rotate',
          'flip-right',
          'flip-left',
          'flip-up',
          'flip-down',
          'jump-right',
          'jump-left',
          'jump-up',
          'jump-down'
        ]
    };
  },
mounted(){
  const experiment_id= this.experiment_id
  const file_name=this.file_name
  this.exp_typeo=this.exp_type

  const BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:6085'
    : `http://${window.location.hostname}:6085`;

  API("auth.getsepfile",{experiment_id,file_name} ).then((res) => {
    this.urls = res.map(item => `${BASE_URL}/${item.encrypt_image.replace(/\\/g, '/')}`);
    this.f_name=res[0].file_name
        });
// console.log(this.exp_type,"dd")
},
  computed: {
    currentImageSrc() {
      return require('/src/assets/cc.jpg');
    },
  },

  methods: {
    toggleZoom(index) {
      const isZoomed = this.zoomed.includes(index);

      if (isZoomed) {
        this.zoomed = this.zoomed.filter((i) => i !== index);
      } else {
        this.zoomed.push(index);
      }
    },
    zoomOut(index) {
      this.zoomed = this.zoomed.filter((i) => i !== index);
    },
    trigger() {
      this.url=require('/src/assets/cc.jpg');
    },

    changeImageColor(color) {
      this.currentImageColor = color;
    },
  },
};
</script>

<style scoped>

.q-img {
  transition: transform 0.3s ease-in-out;
}
.q-img.zoomed {
  transform: scale(1.5);
}


.badge-left {
  position: absolute;
  top: 0;
  left: 0;
}
</style>
