(function () {
  function initEquipamentosCreateModal() {
    const modal = document.getElementById("modal");
    const openBtn = document.getElementById("btn-open-modal");
    const closeBtn = document.getElementById("btn-close-modal");
    const cancelBtn = document.getElementById("btn-cancel");

    if (!modal || !openBtn || !closeBtn || !cancelBtn) return;

    function openModal() {
      modal.classList.remove("hidden");
      modal.classList.add("flex");
      modal.setAttribute("aria-hidden", "false");
    }

    function closeModal() {
      modal.classList.add("hidden");
      modal.classList.remove("flex");
      modal.setAttribute("aria-hidden", "true");
    }

    openBtn.addEventListener("click", openModal);
    closeBtn.addEventListener("click", closeModal);
    cancelBtn.addEventListener("click", closeModal);

    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeModal();
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeModal();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEquipamentosCreateModal);
  } else {
    initEquipamentosCreateModal();
  }
})();
