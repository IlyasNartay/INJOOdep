<script setup>

</script>

<template>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              v-for="restaurant in restaurants"
              :key="restaurant.id"
              class="bg-gray-800/50 border border-gray-700 rounded-lg overflow-hidden hover:bg-gray-800/70 transition-colors cursor-pointer"
              @click="selectRestaurant(restaurant.id)"
            >
              <div class="relative">
                <img
                  :src="restaurant.image"
                  :alt="restaurant.name"
                  class="w-full h-48 object-cover"
                />
              </div>
              <div class="p-4">
                <h3 class="font-semibold text-white mb-1">{{ restaurant.name }}</h3>
                <!-- <p class="text-sm text-gray-400 mb-3">{{ restaurant.description }}</p> -->
                <div class="flex items-center justify-between text-sm">
                  <div class="flex items-center space-x-4">
                    <div class="flex items-center space-x-1 text-cyan-400">
                      <ClockIcon class="w-4 h-4" />
                      <span>{{ restaurant.deliveryTime }}</span>
                      <span class="text-gray-400">мин</span>
                    </div>
                    <div class="flex items-center space-x-1 text-yellow-400">
                      <StarIcon class="w-4 h-4 fill-current" />
                      <span class="text-white">{{ restaurant.rating }}</span>
                    </div>
                  </div>
                  <!-- <div class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">
                    {{ restaurant.tags[0] }}
                  </div> -->
                </div>
              </div>
            </div>
          </div>
</template>