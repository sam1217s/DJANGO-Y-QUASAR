<template>
  <div class="q-pa-md q-gutter-sm">
    <q-carousel
      animated
      v-model="slide"
      infinite
    >
      <q-carousel-slide name="Emprendimiento SENA">
        <q-video
          class="absolute-full"
          src="https://www.youtube.com/embed/n4wSraxuzNI"
        />
      </q-carousel-slide>

      <q-carousel-slide name="Seguridad Industrial">
        <q-video
          class="absolute-full"
          src="https://www.youtube.com/embed/BJAItkbCE5g"
        />
      </q-carousel-slide>

      <q-carousel-slide name="Servicio al Cliente">
        <q-video
          class="absolute-full"
          src="https://www.youtube.com/embed/MjYTz9vzCFw"
         
        />
      </q-carousel-slide>
    </q-carousel>

    <div class="row justify-center">
    <q-btn-toggle
      glossy
      v-model="slide"
      :options="[
        { label: 'Emprendimiento SENA', value: 'Emprendimiento SENA' },
        { label: 'Seguridad Industrial', value: 'Seguridad Industrial' },
        { label: 'Servicio al Cliente', value: 'Servicio al Cliente' }
      ]"
      />
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  setup () {
    return {
      slide: ref('Rihanna')
    }
  }
}
</script>
