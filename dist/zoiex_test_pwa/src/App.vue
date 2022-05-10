<template>
  <v-card v-if="gifs" class="overflow-hidden">
    <v-app-bar color="#333" dark>
      <v-app-bar-title>Gifs</v-app-bar-title>

      <v-spacer></v-spacer>

      <Search @getSearchGifs="getSearchGifs" />
    </v-app-bar>
    <v-sheet>
      <Gifs v-if="!gifs.not_found" :gifs="gifs" />
      <v-container v-else>
        <v-row dense>
          <h2>Ooooops! Gifs not found</h2>
        </v-row>
      </v-container>
    </v-sheet>
  </v-card>
</template>

<script>
import Gifs from "./components/Gifs";
import Search from "./components/Search";
import axios from "axios";

export default {
  name: "App",

  components: {
    Gifs,
    Search,
  },

  data: () => ({
    api: "v1/gifs/trending?api_key=Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g&pingback_id=180aa3a2570776ef",
    gifs: [],
    axios: axios.create({
      baseURL: "https://api.giphy.com",
    }),
  }),

  async mounted() {
    await this.getGifs();
  },
  methods: {
    async getGifs() {
      const response = await this.axios.get(this.api);

      this.gifs = this.convertArray(response.data.data);
      return this.gifs;
    },

    convertArray(data) {
      return data.map((item) => ({
        gif_url: item.images.downsized.url,
        name: item.title,
      }));
    },

    async getSearchGifs(gifs) {
      this.gifs = gifs == null ? await this.getGifs() : gifs;
    },
  },
};
</script>
