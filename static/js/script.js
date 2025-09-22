async function copyText (){
    const text = document.getElementById("preview").textContent;
    try{ await navigator.clipboard.writeText(text); console.log("скопирован в буфер обмена."); }
    catch{ console.error("Не удалось скопировать","error"); }
};

async function clearForm(){
    document.getElementById("project").value = ""
    document.getElementById("department").value = ""
    document.getElementById("specialty").value = ""
    document.getElementById("productType").value = ""
    document.getElementById("docType").value = ""
    document.getElementById("docKind2").value = ""
    document.getElementById("docKind1").value = ""
    document.getElementById("workType").value = ""
    document.getElementById("standardName").value = ""
    document.getElementById("plannedEffort").value = ""
    document.getElementById("operationalEffort").value = ""
    document.getElementById("normativeEffort").value = ""
    document.getElementById("workCost").value = ""
};

document.addEventListener("DOMContentLoaded", ()=>{
    const form = document.getElementById("workForm")

    function calculate_fact(e) {
        e.preventDefault()
        const form_data = new FormData(form)
        const data_input = Object.fromEntries(form_data.entries());
        console.log(data_input)
        fetch("/works", {
          method: "POST", // или GET, PUT, DELETE
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data_input)
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Ошибка сети: " + response.status);
            }
            return response.json(); // или response.text()
          })
          .then(data => {
            console.log("Ответ сервера:", data);
            const result = document.getElementById("preview")
            result.textContent=data.fact_labor
          })
          .catch(error => {
            console.error("Ошибка:", error);
          });

    }
    form.addEventListener("submit", calculate_fact)
})
