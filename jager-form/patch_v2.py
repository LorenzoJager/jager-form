with open('public/index.html', 'r') as f:
    html = f.read()

# ============================================================
# FIX 1: Aggiungi corso Preparazioni Sterili
# ============================================================
old_courses = '''        <div class="course-btn" id="cbtn-2" onclick="selectCourse(\'Cannabis Terapeutica — 29, 30, 31 Maggio 2026\',\'cbtn-2\')">
          <div class="course-icon" id="cicon-2"><svg width="26" height="26" stroke="#0d6fa8"><use href="#icon-cannabis"/></svg></div>
          <div><div class="course-name">Cannabis Terapeutica</div><div class="course-dates">29 · 30 · 31 Maggio 2026</div></div>
        </div>'''

new_courses = '''        <div class="course-btn" id="cbtn-2" onclick="selectCourse(\'Cannabis Terapeutica — 29, 30, 31 Maggio 2026\',\'cbtn-2\')">
          <div class="course-icon" id="cicon-2"><svg width="26" height="26" stroke="#0d6fa8"><use href="#icon-cannabis"/></svg></div>
          <div><div class="course-name">Cannabis Terapeutica</div><div class="course-dates">29 · 30 · 31 Maggio 2026</div></div>
        </div>
        <div class="course-btn" id="cbtn-3" onclick="selectCourse(\'Preparazioni Sterili — 12, 13, 14 Giugno 2026\',\'cbtn-3\')">
          <div class="course-icon" id="cicon-3"><svg width="26" height="26" stroke="#0d6fa8"><use href="#icon-sterili"/></svg></div>
          <div><div class="course-name">Preparazioni Sterili</div><div class="course-dates">12 · 13 · 14 Giugno 2026</div></div>
        </div>'''

html = html.replace(old_courses, new_courses)

# Aggiungi icona siringa per Sterili nelle SVG defs
old_defs_end = '''    <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="#0f6e56" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </symbol>'''

new_defs_end = '''    <symbol id="icon-sterili" viewBox="0 0 24 24" fill="none" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
      <line x1="5" y1="19" x2="10" y2="14"/>
      <path d="M14.5 4.5 L19.5 9.5"/>
      <path d="M10 14 L6 10 L14 2 L18 6 L10 14z"/>
      <line x1="11" y1="5" x2="7" y2="9"/>
      <line x1="13" y1="7" x2="9" y2="11"/>
      <path d="M5 19 Q3 21 2 22"/>
    </symbol>
    <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="#0f6e56" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"/>
    </symbol>'''

html = html.replace(old_defs_end, new_defs_end)

# ============================================================
# FIX 2: Nascondi step 5 quiz per Preparazioni Sterili
# ============================================================
old_select_course = "function selectCourse(val,id){"
new_select_course = """function selectCourse(val,id){
  var isStepQuizVisible = !val.includes('Sterili');
  var dot5 = document.getElementById('dot-5');
  var line4 = document.getElementById('line-4');
  var dot6 = document.getElementById('dot-6');
  var line5 = document.getElementById('line-5');
  if(dot5){dot5.parentElement.style.display = isStepQuizVisible ? '' : 'none';}
  if(line4){line4.style.display = isStepQuizVisible ? '' : 'none';}
  window.skipQuiz = !isStepQuizVisible;"""

html = html.replace(old_select_course, new_select_course)

# Salta step 5 se skipQuiz
old_goto4 = 'onclick="goTo(5)">Rivedi e invia →'
new_goto4 = 'onclick="goTo(window.skipQuiz?6:5)">Rivedi e invia →'
html = html.replace(old_goto4, new_goto4)

# ============================================================
# FIX 3: Allergie con checkbox strutturate
# ============================================================
old_allergy = '''      <div class="allergy-box">
        <div class="allergy-label">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#7a5c00" stroke-width="2" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          ALLERGIE ALIMENTARI
        </div>
        <div class="allergy-sub">Indica eventuali allergie o intolleranze alimentari per la gestione dei pasti durante il corso.</div>
        <textarea class="field-input" id="f-allergie" rows="2" placeholder="Es. celiachia, allergia alle noci, intolleranza al lattosio..."></textarea>
      </div>'''

new_allergy = '''      <div class="allergy-box">
        <div class="allergy-label">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#7a5c00" stroke-width="2" stroke-linecap="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          PREFERENZE E ALLERGIE ALIMENTARI
        </div>
        <div class="allergy-sub">Indica le tue preferenze e allergie — informazioni utili per organizzare i pasti durante il corso.</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px;margin-bottom:10px;">
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-vegetariano" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Vegetariano
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-vegano" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Vegano
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-lattosio" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Intolleranza al lattosio
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-celiaco" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Celiachia / Glutine
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-fruttasecca" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Allergia frutta a guscio
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-uova" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Allergia alle uova
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-pesce" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Allergia al pesce / molluschi
          </label>
          <label style="display:flex;align-items:center;gap:8px;padding:8px 10px;background:#fff;border-radius:8px;border:0.5px solid #f0d070;cursor:pointer;font-size:13px;color:#5a4000;">
            <input type="checkbox" id="all-halal" style="width:16px;height:16px;cursor:pointer;accent-color:#0d6fa8;"> Dieta Halal / Kosher
          </label>
        </div>
        <div style="font-size:12px;color:#9a7a1a;margin-bottom:5px;font-weight:500;">Altre allergie o note per la cucina</div>
        <textarea class="field-input" id="f-allergie" rows="2" placeholder="Es. allergia alle arachidi, diabetico, preferenze particolari..." style="background:#fff;"></textarea>
      </div>'''

html = html.replace(old_allergy, new_allergy)

# ============================================================
# FIX 4: Quiz diverso per Cannabis (vuoto per ora)
# ============================================================
old_quiz_render = "function renderQuiz(){"
new_quiz_render = """var quizCompresse=[
  {text:"Cosa si intende per preparazione galenica magistrale?",options:["Un farmaco prodotto industrialmente in serie","Una preparazione eseguita in farmacia su prescrizione medica individuale","Un integratore alimentare a base di erbe officinali"],correct:1},
  {text:"Quale strumento viene utilizzato per pesare i principi attivi in laboratorio galenico?",options:["Misurino volumetrico graduato","Densimetro ad immersione","Bilancia analitica di precisione"],correct:2},
  {text:"Cosa indica la sigla FU nel contesto della farmacia italiana?",options:["Farmaco ad Uso urgente","Farmacopea Ufficiale della Repubblica Italiana","Formulazione Unificata per preparati officinali"],correct:1},
  {text:"In cosmetologia, un'emulsione O/A indica:",options:["Acqua dispersa in fase oleosa continua","Olio disperso in fase acquosa continua","Una miscela anidra di oli vegetali e cere"],correct:1},
  {text:"Quale delle seguenti è una forma farmaceutica semisolida tipicamente preparata in farmacia?",options:["Fiala per uso parenterale","Compressa a rilascio modificato","Unguento o crema galenica"],correct:2}
];
var quizCannabis=[];
function getActiveQuiz(){
  var corso=document.getElementById('f-corso').value;
  if(corso.includes('Cannabis'))return quizCannabis;
  return quizCompresse;
}
function renderQuiz(){"""

html = html.replace(old_quiz_render, new_quiz_render)

# Usa getActiveQuiz() invece di questions hardcoded
html = html.replace(
    'questions.forEach(function(q,qi){',
    'var activeQ=getActiveQuiz();if(activeQ.length===0){var c=document.getElementById(\'qcont\');c.innerHTML=\'<div style="text-align:center;padding:20px;color:#666;font-size:13px;">Le domande per questo corso saranno disponibili a breve.</div>\';return;}activeQ.forEach(function(q,qi){'
)
html = html.replace(
    'questions[qi].options.forEach',
    'activeQ[qi].options.forEach'
)
html = html.replace(
    'if(oi===q.correct){opt.className=\'answer-option correct\';radio.className=\'answer-radio correct-dot\';if(ua===oi)correct++;}',
    'if(oi===q.correct){opt.className=\'answer-option correct\';radio.className=\'answer-radio correct-dot\';if(ua===oi)correct++;}'
)

# ============================================================
# FIX 5: Badge quiz piu grandi e visibili
# ============================================================
old_badges = '''          <div class="quiz-badge-row">
            <span class="quiz-badge opt"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#0a4f7a" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>Facoltativo</span>
            <span class="quiz-badge anon"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#0a4a38" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>Risposte anonime</span>
            <span class="quiz-badge util"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#7a5c00" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>Migliora il corso</span>
          </div>'''

new_badges = '''          <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;">
            <span style="display:inline-flex;align-items:center;gap:7px;font-size:14px;font-weight:700;padding:8px 16px;border-radius:30px;background:#e8f3fb;color:#0a4f7a;border:1.5px solid #a8d4ee;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0a4f7a" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              FACOLTATIVO
            </span>
            <span style="display:inline-flex;align-items:center;gap:7px;font-size:14px;font-weight:700;padding:8px 16px;border-radius:30px;background:#e1f5ee;color:#0a4a38;border:1.5px solid #9fd8c0;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0a4a38" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              ANONIMO
            </span>
            <span style="display:inline-flex;align-items:center;gap:7px;font-size:14px;font-weight:700;padding:8px 16px;border-radius:30px;background:#fff8e1;color:#7a5c00;border:1.5px solid #f9c74f;">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#7a5c00" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              MIGLIORA IL CORSO
            </span>
          </div>'''

html = html.replace(old_badges, new_badges)

with open('public/index.html', 'w') as f:
    f.write(html)

print("Patch v2 applicata!")
print("  1. Aggiunto corso Preparazioni Sterili")
print("  2. Quiz nascosto per Sterili")
print("  3. Allergie con checkbox strutturate")
print("  4. Quiz Cannabis vuoto per ora")
print("  5. Badge quiz piu grandi")
