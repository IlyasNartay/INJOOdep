import { watch, onBeforeUnmount } from 'vue'

export function useAutoClose(refVar, delay = 2000) {
  let timer = null

  watch(refVar, (val) => {
    if (!val) return

    if (timer) clearTimeout(timer)

    timer = setTimeout(() => {
      refVar.value = false
    }, delay)
  })

  onBeforeUnmount(() => {
    if (timer) clearTimeout(timer)
  })
}
