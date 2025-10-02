<template>
  <div
    class="min-h-screen bg-[url('/src/assets/InhooBubbleTea.jpg')] bg-center px-6 py-8"
  >
    <div class="max-w-7xl mx-auto">
      <!-- FAQ Badge -->
      <div class="mb-8">
        <span
          class="inline-block bg-green-200 text-gray-900 px-6 py-2 rounded-full font-medium text-lg"
        >
          FAQ
        </span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
        <!-- Left Side - Title -->
        <div>
          <h1
            class="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight"
          >
            Часто<br />
            задаваемые<br />
            вопросы
          </h1>
        </div>

        <!-- Right Side - FAQ Items -->
        <div class="space-y-4">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="bg-white rounded-2xl shadow-sm overflow-hidden transition-all duration-300 ease-in-out"
            :class="{ 'shadow-lg': faq.isOpen }"
          >
            <!-- Question Header -->
            <button
              @click="toggleFaq(index)"
              class="w-full px-6 py-5 flex items-center justify-between text-left hover:bg-gray-50 transition-colors duration-200"
            >
              <span class="text-lg font-medium text-gray-900 pr-4">
                {{ faq.question }}
              </span>
              <div
                class="flex-shrink-0 w-8 h-8 border-2 border-gray-300 rounded-full flex items-center justify-center transition-transform duration-300"
                :class="{ 'rotate-45 border-gray-500': faq.isOpen }"
              >
                <svg
                  class="w-4 h-4 text-gray-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  ></path>
                </svg>
              </div>
            </button>

            <!-- Answer Content -->
            <transition
              name="slide-down"
              @enter="enter"
              @after-enter="afterEnter"
              @leave="leave"
            >
              <div v-if="faq.isOpen" class="overflow-hidden">
                <div class="px-6 pb-5 text-gray-700 leading-relaxed">
                  {{ faq.answer }}
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const faqs = ref([
  {
    question: "Что такое бабл ти?",
    answer:
      "Бабл ти (bubble tea) - это тайваньский напиток, который состоит из чая, молока и жевательных шариков тапиоки. Шарики тапиоки придают напитку уникальную текстуру и делают его особенно интересным для употребления.",
    isOpen: false,
  },
  {
    question: "Какие ингредиенты вы используете?",
    answer:
      "Мы используем только качественные натуральные ингредиенты: премиальные сорта чая, свежее молоко, натуральные сиропы, свежие фрукты и тапиоку высшего качества. Все ингредиенты проходят строгий контроль качества.",
    isOpen: false,
  },
  {
    question: "Есть ли у вас веганские варианты?",
    answer:
      "Да, у нас есть множество веганских вариантов! Мы можем приготовить напитки на растительном молоке (овсяном, кокосовом, миндальном), а также предлагаем фруктовые чаи без добавления молочных продуктов.",
    isOpen: false,
  },
  {
    question: "Как сделать заказ?",
    answer:
      "Вы можете сделать заказ несколькими способами: через наш сайт, по телефону, через приложения доставки или посетив наши точки продаж. Мы также предлагаем доставку и самовывоз.",
    isOpen: false,
  },
  {
    question: "Какие добавки доступны?",
    answer:
      "У нас большой выбор добавок: классические шарики тапиоки, фруктовые желе, кокосовое желе, пудинг, взбитые сливки, сырная пенка и многое другое. Вы можете комбинировать несколько добавок в одном напитке.",
    isOpen: false,
  },
]);

const toggleFaq = (index) => {
  faqs.value[index].isOpen = !faqs.value[index].isOpen;
};

// Animation methods
const enter = (el) => {
  el.style.height = "0";
};

const afterEnter = (el) => {
  el.style.height = "auto";
};

const leave = (el) => {
  el.style.height = el.scrollHeight + "px";
  el.offsetHeight; // trigger reflow
  el.style.height = "0";
};
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: height 0.3s ease-in-out;
  overflow: hidden;
}

.slide-down-enter-from,
.slide-down-leave-to {
  height: 0;
}
</style>
