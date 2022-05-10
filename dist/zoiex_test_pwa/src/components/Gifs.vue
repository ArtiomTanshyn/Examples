<template>
  <v-container>
    <v-row dense>
      <v-col v-for="gif in data_gifs" :key="gif.title">
        <v-card>
          <v-img
            :src="gif.gif_url"
            class="white--text align-end"
            gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"
            height="300px"
            width="auto"
          ></v-img>
          <v-btn @click="copyInfo(gif)" icon>
            <v-icon>mdi-share-variant</v-icon>
          </v-btn>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Gifs",

  props: {
    gifs: {
      type: Array,
    },
  },

  data: () => ({
    data_gifs: [],
  }),

  computed: {
    webShareApiSupported() {
      return navigator.share;
    },
  },

  methods: {
    copyInfo(gif) {
      if (this.webShareApiSupported) {
        navigator.share(gif);
      } else {
        alert("oooops...");
      }
    },
  },

  watch: {
    gifs: {
      deep: true,
      handler(value) {
        this.data_gifs = [...value];
      },
    },
  },
};
</script>