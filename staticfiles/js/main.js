function mudarCor() {
  document.body.style.backgroundColor = "darkblue";
}

function alertarMensagem() {
  alert("Este botao ainda nao esta funcionando!");
}

function confirmarExclusao() {
  return confirm("Tem certeza que deseja excluir?");
}

function toast(msg) {
  const t = document.createElement("div");
  t.className = "toast";
  t.innerText = msg;
  document.body.appendChild(t);

  setTimeout(() => t.remove(), 3000);
}