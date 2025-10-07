<script setup>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref, reactive } from "vue";
import Loader from "@/components/Loader.vue";
import CustomModal from "@/components/CustomModal.vue";
import { MailIcon, LockIcon } from "lucide-vue-next";

const router = useRouter();
const isLoading = ref(false);
const failModal = ref(false);

const data = reactive({
  phone: "",
  password: "",
});

const login = async () => {
  isLoading.value = true;
  try {
    // 🔹 Прямой запрос без .env
    const response = await axios.post(
        "https://api.injoo.duckdns.org/auth/login",
        {
          phone: data.phone,
          password: data.password,
        }
    );

    const token = response.data.access_token;
    const user_role = response.data.user_role;

    if (token) {
      localStorage.setItem("authToken", token);
      localStorage.setItem("userRole", user_role);
    }

    if (user_role === "customer" || user_role === "admin") {
      router.push("/CliMain");
    } else {
      console.log("no route");
    }
  } catch (error) {
    failModal.value = true;
    setTimeout(() => {
      failModal.value = false;
    }, 3000);
  } finally {
    isLoading.value = false;
  }
};
</script>
