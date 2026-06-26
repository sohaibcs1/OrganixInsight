<template>
    <div class="q-pa-md" style="width: 100%;">
    <!-- {{experiment_id}}
    {{passEx_type}} -->

    <!-- <div class="q-mb-xl flex justify-center" v-if="['2D Experiment', '2D Simple Experiment'].includes(passEx_type)"> -->

    <div class="q-mb-xl flex justify-center">
           <div class="q-mb-xl"> <q-badge color="primary">Select Range</q-badge></div>

        <q-range
            v-model="redModel"
            marker-labels
            label-always
            color="negative"
            :step="1"
            :min="0"
            :max="15"
        />
        <q-btn color="primary" label="Apply Multi-Scal Log" dense class="q-mt-lg q-mr-lg" @click="dialogcellCount"/>
         <div class="text-h4 q-mt-lg" v-if="cellCount">
                {{ cellCount }}
                <q-badge align="top" >Cell Count</q-badge>
                </div>
            </div>
        <q-spinner v-if="loading" size="30px" color="primary" class="q-mt-md" />

        <q-img
            v-else-if="url"
            :src="url"
            class="rounded-borders q-mr-sm q-mb-sm"
            spinner-color="white"
            ratio="1"
            style=" margin: 0 auto; min-width: 500px; max-width: 90%; cursor: zoom-in; transform-origin: center center;"
            @wheel.prevent="zoomImage"
        />
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import API from "src/api";


export default {
    props: {
        experiment_id: String,
        file_name: String,
        passEx_type: String,
    },
    mounted() {
            // const experiment_id= this.experiment_id
            // const file_name=this.file_name
            // this.exp_typeo=this.passEx_type

            // const BASE_URL = window.location.hostname === 'localhost'
            //     ? 'http://localhost:6085'
            //     : `http://${window.location.hostname}:6085`;

            // API("auth.getsepfileOne",{experiment_id,file_name} ).then((res) => {
            //     this.urlserver = res.map(item => `${BASE_URL}/${item.encrypt_image.replace(/\\/g, '/')}`);
            //     this.nameserver=res[0].file_name
            //     console.log(this.nameserver,"kkkkkk")

            //         });
    },
    setup(props) {
        const redModel = ref({ min: 8, max: 12 });
        const f_name = ref('');
        const url = ref('');
        const loading = ref(false);
        const cellCount = ref(0);
        const zoomLevel = ref(1);

        const zoomImage = (event) => {
    event.preventDefault();

    const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1;

    // clamp scale between min and max
    const minZoom = 0.5;
    const maxZoom = 5.0;

    zoomLevel.value = Math.min(maxZoom, Math.max(minZoom, zoomLevel.value * zoomFactor));

    const el = event.currentTarget;
    el.style.transformOrigin = "center center";
    el.style.transform = `scale(${zoomLevel.value})`;
};




        const dialogcellCount = async () => {
            try {


                loading.value = true;
                const experiment_id= props.experiment_id
                const file_name=props.file_name
                const apires=await API("auth.getsepfileOne", { experiment_id, file_name });
                var u = apires.map(item => item.encrypt_image.replace(/\\/g, '/').split('/').pop());
                // console.log(u[0])
               const jpgName=u[0]
               const sendToServer = await API('home.getCellcount', {
                    id:props.experiment_id,
                    name: jpgName,
                    min_sigma: parseFloat(redModel.value.min),
                    max_sigma: parseFloat(redModel.value.max)
                });

                console.log(sendToServer, "ServerResponse");

                if (sendToServer.status === 'success' && sendToServer.image_base64) {
                    url.value = `data:image/png;base64,${sendToServer.image_base64}`;
                    cellCount.value = sendToServer.cell_count;
                } else {
                    console.error("Error fetching the image:", sendToServer.message);
                }
            } catch (error) {
                console.error("API error:", error);
            } finally {
                loading.value = false;
            }
        };

        // onMounted(() => {



        // });

        return {
            redModel,
            f_name,
            url,
            loading,
            cellCount,
            zoomImage,
            dialogcellCount,
        };
    }
};
</script>
