function confirmarExclusao(itemName = "este item") {
  return confirm(`Tem certeza que deseja remover "${itemName}"?`);
}

function validateEmail(email) {
  const validate = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return validate.test(email);
}

function showNotification(message, type = "info") {
  const notification = document.createElement("div");

  notification.className = `alert alert-${type}`;

  notification.textContent = message;

  setTimeout(() => {
    notification.style.opacity = "0";
    notification.style.transition = "opacity .3s";

    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

function toast(message) {
  showNotification(message, "Concluído");
}

function printBid() {
  window.print();
}
