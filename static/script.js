document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-form");
  const input = document.getElementById("title");
  const errorBox = document.getElementById("client-error");

  form.addEventListener("submit", (event) => {
    if (input.value.trim() === "") {
      event.preventDefault();
      errorBox.textContent = "タスク名を入力してください。";
      errorBox.classList.remove("hidden");
      input.classList.add("invalid");
      input.focus();
    }
  });

  input.addEventListener("input", () => {
    errorBox.classList.add("hidden");
    input.classList.remove("invalid");
  });

  document.querySelectorAll(".delete-form").forEach((deleteForm) => {
    deleteForm.addEventListener("submit", (event) => {
      const title = deleteForm.closest(".task").querySelector(".task-title").textContent;
      if (!confirm(`タスク「${title}」を削除しますか？`)) {
        event.preventDefault();
      }
    });
  });
});
