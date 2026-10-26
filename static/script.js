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

  // ブラウザ標準の confirm() は埋め込み表示などでブロックされることがあるため、画面内で2段階確認する
  document.querySelectorAll(".delete-form").forEach((deleteForm) => {
    const deleteBtn = deleteForm.querySelector(".delete-btn");
    const cancelBtn = deleteForm.querySelector(".cancel-btn");

    deleteForm.addEventListener("submit", (event) => {
      if (deleteForm.dataset.confirming !== "true") {
        event.preventDefault();
        deleteForm.dataset.confirming = "true";
        deleteBtn.textContent = "本当に削除";
        deleteBtn.classList.add("confirming");
        cancelBtn.classList.remove("hidden");
      }
    });

    cancelBtn.addEventListener("click", () => {
      deleteForm.dataset.confirming = "false";
      deleteBtn.textContent = "削除";
      deleteBtn.classList.remove("confirming");
      cancelBtn.classList.add("hidden");
    });
  });
});
