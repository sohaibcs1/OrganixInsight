<template>
  <div class="q-pa-md">
    <q-card-section class="row ">
          <q-space/>
          <q-btn icon="close"  round dense v-close-popup />
        </q-card-section>
    <q-btn
      push
      color="teal"
      @click="show_3dimge_dialog=true"
      class="q-mb-md"
    >{{ f_name }}</q-btn>

  <br>
  


  <q-img
      v-for="(url, index) in urls"
      :key="index"
      :src="url"
      style="max-width: 100%; height: 200px; width: 200px; position: relative; cursor: pointer;"
      ratio="1"
      spinner-color="white"
      class="rounded-borders q-mr-sm q-mb-sm"
      @click="toggleZoom(index)"
      @mouseleave="zoomOut(index)"
      :class="{ 'zoomed': zoomed.includes(index) }"
    >
      <q-badge class="badge-left">{{ index + 1 }}</q-badge>
    </q-img>
        <!-- <div class="absolute-bottom text-center text-body2" @click="show_dialog=true">
         <q-badge color="orange" class="text-body2">Segmentation</q-badge> 
        </div> -->

     

    
  </div>


  <!-- <q-dialog v-model="show_dialog">
    <q-card class="fit text-center">
      <q-card-section align="center">
        <div class="row text-center">
          <div class="q-pa-md q-gutter-sm">
            <q-btn color="primary" @click="changeImageColor('blue')" label="Blue" />
            <q-btn color="secondary" @click="changeImageColor('green')" label="Green" />
            <q-btn color="deep-orange" @click="changeImageColor('red')" glossy label="RED" />
            <q-btn color="brown" @click="changeImageColor('teal')" label="Teal" />
            <q-btn color="purple" @click="changeImageColor('purple')" label="Purple" />
            <q-btn color="black" @click="changeImageColor('black')" label="Black" />
          </div>

          <q-img
            :src="currentImageSrc"
            spinner-color="white"
            img-class="my-custom-image"
            class="rounded-borders"
          />
        </div>
      </q-card-section>
    </q-card>
  </q-dialog> -->

  <div>
    <q-dialog v-model="show_3dimge_dialog" >
        <q-card style="width: 2000px; max-width: 2000px">
  
          <!-- add Camra Details Start -->
          <q-card-section align="center" >
            <div class="row text-center">
              <!-- Define attributes table -->
              <!-- <visulizer3d fit></visulizer3d> -->
              <!-- <moreImages :experiment_id="prop_exp_id"  :file_name="prop_file_name" ></moreImages> -->
              
              <!-- attributes table END -->
            </div>
          </q-card-section>
          <!-- add Camra Details END -->
        </q-card>
      </q-dialog>
  </div>
</template>

<script>
 import API from "src/api";
 import { ref } from "vue";
  import { exportFile, useQuasar } from "quasar";
  // import visulizer3d from 'src/components/user/visulizer3d';
export default {

  components: {},  props: {

experiment_id: String,
file_name: String,

},

  data() {
    
    return {
      show_3dimge_dialog:ref(false),
      show_dialog: false,
      currentImageColor: 'red',
      // url: 'https://picsum.photos/500/300',
      urls:[],
      zoomed: [],
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

  API("auth.getsepfile",{experiment_id,file_name} ).then((res) => {
    this.urls=res.map(item => `http://134.197.75.35:6085/${item.encrypt_image.replace(/\\/g, '/')}`);
    this.f_name=res[0].file_name
          // console.log(res,"dsfsdf" )
        });

},
  computed: {
    currentImageSrc() {
      // return `https://picsum.photos/500/300?color=${this.currentImageColor}`;
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
      // this.url = 'https://picsum.photos/500/300?t='+1;
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