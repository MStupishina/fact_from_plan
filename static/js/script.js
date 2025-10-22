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
    let current_file = null

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
    function calculate_fact_from_file(e) {
        console.log("info")
        const form_data = new FormData()
        form_data.append("file", e.target.files[0])
        fetch("/set_works", {
          method: "POST", // или GET, PUT, DELETE
          body: form_data
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Ошибка сети: " + response.status);
            }
            return response.blob(); // или response.text()
          })
          .then(data => {
            console.log("Ответ сервера:", data);
            current_file = data
            const result = document.getElementById("preview")
            result.textContent="Расчет выполнен, нажмите кнопку Выгрузить результат"
          })
          .catch(error => {
            console.error("Ошибка:", error);
          });

    }

    document.getElementById("result").addEventListener("click", () => {
      if (!current_file) {
        alert("Нет данных для скачивания");
        return;
      }

      const url = URL.createObjectURL(current_file);
      const a = document.createElement("a");
      a.href = url;
      a.download = "result.xlsx"; // имя скачиваемого файла
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    });


    form.addEventListener("submit", calculate_fact)
    console.log("change")
    document.getElementById("file_input").addEventListener("change", calculate_fact_from_file)
})
