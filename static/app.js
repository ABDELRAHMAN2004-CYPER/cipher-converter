
const $=id=>document.getElementById(id);
const names={plain:"Plain Text",caesar:"Caesar Cipher",vigenere:"Vigenère Cipher"};
function ui(){let s=$("source").value,t=$("target").value;$("shiftWrap").classList.toggle("hide",s!=="caesar"&&t!=="caesar");$("keyWrap").classList.toggle("hide",s!=="vigenere"&&t!=="vigenere");$("inType").textContent=names[s];$("outType").textContent=names[t]}
["source","target"].forEach(x=>$(x).onchange=ui);ui();
$("input").oninput=()=>{$("count").textContent=$("input").value.length+" chars"};
$("file").onchange=async e=>{if(!e.target.files[0])return;let fd=new FormData();fd.append("file",e.target.files[0]);let r=await fetch("/api/file",{method:"POST",body:fd}),d=await r.json();if(d.success){$("input").value=d.text;$("input").dispatchEvent(new Event("input"))}else toast(d.error)};
$("convert").onclick=async()=>{let text=$("input").value;if(!text.trim())return toast("Enter some text first.");let r=await fetch("/api/convert",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text,source:$("source").value,target:$("target").value,shift:$("shift").value,key:$("key").value})}),d=await r.json();if(!d.success)return toast(d.error);$("output").value=d.result;renderMap(text,d.result,$("source").value,$("target").value);stats();toast("Conversion completed.")};
$("copy").onclick=()=>{navigator.clipboard.writeText($("output").value);toast("Copied to clipboard.")};
$("clear").onclick=()=>{$("input").value="";$("output").value="";$("mapping").innerHTML='<div class="empty">Run a conversion to visualize the mapping.</div>'};
$("swap").onclick=()=>{let a=$("source").value,b=$("target").value;$("source").value=b;$("target").value=a;let x=$("input").value;$("input").value=$("output").value;$("output").value=x;ui()};
$("download").onclick=async()=>{let text=$("output").value;if(!text)return toast("Nothing to download.");let r=await fetch("/api/download",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text,filename:"cipher-result.txt"})});let blob=await r.blob(),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download="cipher-result.txt";a.click();URL.revokeObjectURL(url)};
async function stats(){let h=await (await fetch("/api/history")).json();$("ops").textContent=h.length;$("enc").textContent=h.filter(x=>x.target!=="plain").length;$("chars").textContent=h.reduce((a,x)=>a+x.input.length,0);let c={};h.forEach(x=>c[x.target]=(c[x.target]||0)+1);let best=Object.keys(c).sort((a,b)=>c[b]-c[a])[0];$("algo").textContent=best?names[best]:"—"}stats();
function renderMap(a,b,s,t){let box=$("mapping");box.innerHTML="";let n=Math.min(a.length,30);for(let i=0;i<n;i++){let x=document.createElement("div");x.className="map";x.innerHTML=`<small>${a[i]===" "?"SPACE":a[i]}</small><b>↓</b><strong>${b[i]===" "?"SPACE":b[i]}</strong>`;box.appendChild(x)}}
function toast(m){$("toast").textContent=m;$("toast").classList.remove("hide");setTimeout(()=>$("toast").classList.add("hide"),2200)}
stats();
