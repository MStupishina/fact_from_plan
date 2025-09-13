/** =========================
 *  Основной скрипт
 *  ========================= */
const $ = (sel) => document.querySelector(sel);
const toast = (msg, type="ok", timeout=3200) => {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.toggle("error", type==="error");
  t.style.display = "block";
  setTimeout(()=>{t.style.display="none"}, timeout);
};

const serializeForm = (form) => {
  const data = Object.fromEntries(new FormData(form).entries());
  const numberFields = ["plannedEffort","actualEffort","operationalEffort","normativeEffort","workCost"];
  numberFields.forEach(k=>{
    if(data[k]!=="") data[k]=Number(data[k]);
    else delete data[k];
  });
  return data;
};

const validateBusinessRules = (payload)=>{
  const problems=[];
  if(payload.plannedEffort!==undefined && payload.actualEffort!==undefined){
    if(payload.actualEffort>0 && payload.plannedEffort===0) problems.push("Фактические трудозатраты указаны при нуле плановых.");
  }
  ["plannedEffort","actualEffort","operationalEffort","normativeEffort","workCost"].forEach(k=>{
    if(payload[k]!==undefined && payload[k]<0) problems.push(`Поле "${k}" не может быть отрицательным.`);
  });
  return problems;
};

const showPreview = (payload)=> $("#preview").textContent = JSON.stringify(payload,null,2);
const saveDraft = (payload)=> { localStorage.setItem(DRAFT_KEY, JSON.stringify(payload)); toast("Черновик сохранён."); };
const loadDraft = ()=>{
  const raw = localStorage.getItem(DRAFT_KEY);
  if(!raw){ toast("Черновик не найден","error"); return; }
  try{
    const draft = JSON.parse(raw);
    Object.entries(draft).forEach(([k,v])=>{
      const el=document.querySelector(`[name="${k}"]`);
      if(!el) return;
      el.value=(typeof v==="number")?String(v):(v??"");
    });
    showPreview(draft);
    toast("Черновик загружен.");
  }catch{ toast("Ошибка чтения черновика","error"); }
};
const copyToClipboard = async (text)=>{
  try{ await navigator.clipboard.writeText(text); toast("JSON скопирован в буфер обмена."); }
  catch{ toast("Не удалось скопировать JSON","error"); }
};

const form=$("#workForm");
let autosaveTimer=null;
form.addEventListener("input",()=>{
  $("#autosaveState").textContent="Черновик: есть несохранённые изменения…";
  if(autosaveTimer) clearTimeout(autosaveTimer);
  autosaveTimer=setTimeout(()=>{
    saveDraft(serializeForm(form));
    $("#autosaveState").textContent="Автосохранение включено";
  },2000);
});

$("#previewBtn").addEventListener("click",()=>{
  const payload=serializeForm(form);
  const problems=validateBusinessRules(payload);
  if(problems.length) toast(problems[0],"error");
  showPreview(payload);
});

$("#copyJsonBtn").addEventListener("click",()=> copyToClipboard($("#preview").textContent || JSON.stringify(serializeForm(form),null,2)));
$("#saveDraftBtn").addEventListener("click",()=> saveDraft(serializeForm(form)));
$("#loadDraftBtn").addEventListener("click",()=> loadDraft());
$("#clearBtn").addEventListener("click",()=>{ form.reset(); $("#preview").textContent=""; toast("Форма очищена."); });

form.addEventListener("submit", async (e)=>{
  e.preventDefault();
  if(!form.checkValidity()){ form.reportValidity(); return; }
  const payload=serializeForm(form);
  const problems=validateBusinessRules(payload);
  if(problems.length){ toast(problems[0],"error"); return; }
  showPreview(payload);
  $("#serverState").textContent="Отправляем…";
  try{
    const headers = USE_JSON ? {"Content-Type":"application/json"} : {"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"};
    const body = USE_JSON ? JSON.stringify(payload) : new URLSearchParams(payload).toString();
    const res = await fetch(API_ENDPOINT,{method:"POST",headers,body});
    if(!res.ok){
      const text=await res.text().catch(()=>"");
      throw new Error(`HTTP ${res.status} ${res.statusText}${text?": "+text:""}`);
    }
    const data=await res.json().catch(()=>({}));
    $("#serverState").textContent="Готово";
    toast("Данные успешно отправлены.");
    console.log("Server response:",data);
  }catch(err){
    console.error(err);
    $("#serverState").textContent="";
    toast(`Ошибка отправки: ${err.message}`,"error",5000);
  }
});

window.addEventListener("DOMContentLoaded",()=>{
  const raw=localStorage.getItem(DRAFT_KEY);
  if(raw){
    try{
      const draft=JSON.parse(raw);
      Object.entries(draft).forEach(([k,v])=>{
        const el=document.querySelector(`[name="${k}"]`);
        if(!el) return;
        el.value=(typeof v==="number")?String(v):(v??"");
      });
      showPreview(draft);
      $("#autosaveState").textContent="Черновик подгружен";
    }catch{}
  }
});
