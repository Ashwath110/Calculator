async function evaluateExpr(){
  const expr = document.getElementById('expr').value.trim();
  const out = document.getElementById('exprResult');
  if(!expr){ out.textContent = 'Enter an expression'; return; }
  out.textContent = 'Computing...';
  try{
    const resp = await fetch('/api/evaluate', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({expr})
    });
    const j = await resp.json();
    if(j.ok){ out.textContent = j.result; }
    else { out.textContent = 'Error: ' + j.error; }
  }catch(e){ out.textContent = 'Network error: ' + e; }
}

function insertSample(){
  document.getElementById('expr').value = 'sin(pi/2) + ln(10) + 2**3';
}

async function matrixOp(op){
  const aText = document.getElementById('matA').value.trim();
  const bText = document.getElementById('matB').value.trim();
  const out = document.getElementById('matResult');
  out.textContent = 'Working...';
  try{
    const a = aText ? JSON.parse(aText) : null;
    const b = bText ? JSON.parse(bText) : null;
    const resp = await fetch('/api/matrix', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({op, a, b})
    });
    const j = await resp.json();
    if(j.ok){ out.textContent = JSON.stringify(j.result, null, 2); }
    else { out.textContent = 'Error: ' + j.error; }
  }catch(e){ out.textContent = 'Parse or network error: ' + e; }
}
