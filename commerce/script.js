let currentData = null;
let currentChapter = null;
let currentSubject = null;

fetch('commerce/data.json')
  .then(res => res.json())
  .then(data => {
    currentData = data;
    loadSidebar(data);
  })
  .catch(err => {
    console.error('Error loading data:', err);
    document.getElementById('tabContent').innerHTML = 
      '<div class="empty-state">❌ Error loading data. Make sure commerce/data.json exists.</div>';
  });

function loadSidebar(data) {
  const sidebar = document.getElementById('sidebar');
  sidebar.innerHTML = '';

  for (let subject in data) {
    const subjectTitle = document.createElement('h3');
    subjectTitle.innerText = subject;
    sidebar.appendChild(subjectTitle);

    for (let chapter in data[subject]) {
      const chap = document.createElement('div');
      chap.innerText = chapter;
      chap.className = "chapter";
      chap.onclick = () => {
        loadChapter(subject, chapter);
        if (window.innerWidth <= 768) {
          toggleSidebar();
        }
        document.querySelectorAll('.chapter').forEach(c => c.classList.remove('active'));
        chap.classList.add('active');
      };
      sidebar.appendChild(chap);
    }
  }
}

function loadChapter(subject, chapter) {
  currentSubject = subject;
  currentChapter = currentData[subject][chapter];
  document.getElementById('chapterTitle').innerText = chapter;
  
  document.querySelectorAll('.tabs button').forEach(btn => btn.classList.remove('active-tab'));
  
  showTab('formulas');
}

function showTab(type) {
  if (!currentChapter) {
    document.getElementById('tabContent').innerHTML = 
      '<div class="empty-state">👈 Please select a chapter first</div>';
    return;
  }

  document.querySelectorAll('.tabs button').forEach(btn => {
    btn.classList.remove('active-tab');
    if (btn.textContent.includes(type === 'formulas' ? 'Formulas' : 
                                 type === 'derivations' ? 'Derivations' :
                                 type === 'pyq' ? 'PYQ' : 'Notes')) {
      btn.classList.add('active-tab');
    }
  });

  const tabContent = document.getElementById('tabContent');
  tabContent.innerHTML = '';

  if (type === 'notes') {
    const div = document.createElement('div');
    div.innerText = currentChapter.notes || '📝 No notes available for this chapter.';
    tabContent.appendChild(div);
    return;
  }

  const items = currentChapter[type];
  if (!items || items.length === 0) {
    const div = document.createElement('div');
    div.innerText = `📌 No ${type} available for this chapter.`;
    tabContent.appendChild(div);
    return;
  }

  items.forEach((item, index) => {
    const div = document.createElement('div');
    div.innerText = `${index + 1}. ${item}`;
    tabContent.appendChild(div);
  });
}

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');
  
  sidebar.classList.toggle('active');
  overlay.classList.toggle('active');
  
  if (sidebar.classList.contains('active')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
}

window.addEventListener('orientationchange', () => {
  if (window.innerWidth > 768) {
    document.getElementById('sidebar').classList.remove('active');
    document.getElementById('overlay').classList.remove('active');
    document.body.style.overflow = '';
  }
});
