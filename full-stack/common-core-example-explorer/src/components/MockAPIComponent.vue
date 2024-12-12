//hard coded based on jupyter notebook responses //(instead of actual server)

<template>
  <!-- <p>mockapi</p> -->
</template>

<script>
export default {
  name: "MockApiComponent",

  data() {
    return {
      queriesAndResponses: [], // This will hold the loaded JSON data
    };
  },

  async created() {
    try {
      // Fetch the JSON file from the public directory
      const response = await fetch("/mockApiData.json");

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      this.queriesAndResponses = data;

      console.log("Loaded queries and responses:", this.queriesAndResponses);
    } catch (error) {
      console.error("Failed to load mock API data:", error);
    }
  },

  methods: {
    findResponse(searchQuery) {
      if (!searchQuery) return null;

      console.log(`User search query: "${searchQuery}"`);

      let bestMatch = null;
      let highestScore = 0;

      this.queriesAndResponses.forEach((item) => {
        const score = this.calculateSimilarity(searchQuery, item.query);
        console.log(
          `Comparing with: "${item.query}" - Similarity Score: ${score}`,
        );

        if (score > highestScore) {
          highestScore = score;
          bestMatch = item.response;
        }
      });

      console.log("Best match response:", bestMatch);

      return bestMatch || null;
    },

    calculateSimilarity(userQuery, predefinedQuery) {
      const userWords = userQuery.toLowerCase().split(" ");
      const queryWords = predefinedQuery.toLowerCase().split(" ");

      const matchingWords = userWords.filter((word) =>
        queryWords.includes(word),
      );
      return matchingWords.length / queryWords.length;
    },
  },
};
</script>
