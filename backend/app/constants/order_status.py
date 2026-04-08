from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    ready = "ready"
    done = "done"
    cancelled = "cancelled"


ORDER_STATUS_LABELS = {
    OrderStatus.pending.value: "Ожидает подтверждения",
    OrderStatus.accepted.value: "Подтвержден",
    OrderStatus.ready.value: "Готовится",
    OrderStatus.done.value: "Доставлен",
    OrderStatus.cancelled.value: "Отменён",
}


ORDER_STATUS_FLOW = (
    OrderStatus.pending.value,
    OrderStatus.accepted.value,
    OrderStatus.ready.value,
    OrderStatus.done.value,
    OrderStatus.cancelled.value,
)
