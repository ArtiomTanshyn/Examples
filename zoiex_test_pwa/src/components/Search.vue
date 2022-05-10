<template>
  <v-text-field
    placeholder="Search"
    prepend-inner-icon="mdi-magnify"
    v-model="search"
    filled
    dense
  >
  </v-text-field>
</template>

<script>
import axios from "axios";
import debounce from "lodash/debounce";

export default {
  name: "Search",

  data: () => ({
    search: null,
    api: "v1/channels/search",
    api_key: "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g",
    // api: "v1/gifs",
    // api_key: "bHXi6e54UeAetadh1gr7DAe5QnOG0Fr0"
    gifs: [],
    axios: axios.create({
      baseURL: "https://api.giphy.com",
    }),
  }),

  methods: {
    getGifs: debounce(async function (value) {
      if (value == "") {
        this.gifs = null;
      } else {
        const response = await this.axios(this.api, {
          params: {
            api_key: this.api_key,
            q: value,
          },
        });
        this.gifs =
          response.data.data.length != 0
            ? this.convertArray(response.data.data)
            : { not_found: true };
      }
      this.$emit("getSearchGifs", this.gifs);
    }, 500),
    convertArray(data) {
      return data
        .filter((item) => item.banner_image != null)
        .map((item) => ({
          gif_url: item.banner_image,
          name: item.display_name,
        }));
    },
  },
  watch: {
    search: {
      deep: true,
      async handler(value) {
        await this.getGifs(value);
      },
    },
  },
};
</script>