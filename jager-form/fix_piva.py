with open('public/index.html', 'r') as f:
    html = f.read()

# Inietta una funzione lookupPIVA pulita prima del tag </script> finale
new_fn = """
function lookupPIVA(el){
  var v=el.value.replace(/\\D/g,'');el.value=v;
  var spin=document.getElementById('piva-spinner');
  var lt=document.getElementById('vies-loading-text');
  var pr=document.getElementById('piva-result');
  var ok=document.getElementById('vies-ok');
  var err=document.getElementById('vies-err');
  if(window.pivaTimer)clearTimeout(window.pivaTimer);
  if(window.manualTimer)clearTimeout(window.manualTimer);
  if(spin)spin.style.display='none';
  if(lt)lt.style.display='none';
  if(pr)pr.style.display='none';
  if(ok)ok.style.display='none';
  if(err)err.style.display='none';
  if(v.length!==11)return;
  if(spin)spin.style.display='block';
  if(lt){lt.style.display='block';}
  var mb=document.getElementById('vies-manual-timeout-btn');
  window.manualTimer=setTimeout(function(){if(mb)mb.style.display='block';},5000);
  window.pivaTimer=setTimeout(function(){
    fetch('/api/vies/'+v)
      .then(function(r){return r.json();})
      .then(function(d){
        if(spin)spin.style.display='none';
        if(lt)lt.style.display='none';
        if(window.manualTimer)clearTimeout(window.manualTimer);
        if(mb)mb.style.display='none';
        if(pr)pr.style.display='block';
        if(d.isValid&&d.name&&d.name!=='---'&&d.name.trim()!==''){
          var name=d.name.trim();
          var addr='';
          if(d.address)addr=d.address.split('\\n').filter(function(x){return x.trim();}).join(', ');
          if(ok){ok.style.display='block';}
          if(err)err.style.display='none';
          var n=document.getElementById('vies-name-ok');if(n)n.textContent=name;
          var a=document.getElementById('vies-addr-ok');if(a)a.textContent=addr||'Indirizzo registrato VIES';
          el.className='field-input valid';
        } else if(d.isValid){
          if(ok){ok.style.display='block';}
          if(err)err.style.display='none';
          var n=document.getElementById('vies-name-ok');if(n)n.textContent='P.IVA valida';
          var a=document.getElementById('vies-addr-ok');if(a)a.textContent='Ragione sociale non disponibile nel registro VIES';
          el.className='field-input valid';
        } else {
          if(ok)ok.style.display='none';
          if(err){err.style.display='block';}
          var et=document.getElementById('vies-err-text');if(et)et.textContent='P.IVA non trovata su VIES — verifica il numero';
          el.className='field-input invalid';
        }
      })
      .catch(function(){
        if(spin)spin.style.display='none';
        if(lt)lt.style.display='none';
        if(pr)pr.style.display='block';
        if(ok)ok.style.display='none';
        if(err){err.style.display='block';}
        var et=document.getElementById('vies-err-text');if(et)et.textContent='Verifica VIES non disponibile — inserisci i dati manualmente';
        var mb=document.getElementById('vies-manual-timeout-btn');if(mb)mb.style.display='block';
      });
  },900);
}
"""

# Inserisci prima del tag </script> finale
html = html.replace('</script>\n</body>', new_fn + '</script>\n</body>')

with open('public/index.html', 'w') as f:
    f.write(html)

print("Funzione lookupPIVA riscritta!")
