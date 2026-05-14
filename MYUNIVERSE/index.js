document.addEventListener('DOMContentLoaded', function() {
    const chapterSelect = document.getElementById('chapterSelect');
    const loadBtn = document.getElementById('loadBtn');
    const storyContent = document.getElementById('storyContent');

    // Dynamically detect available chapters from folder
    // Note: This is a DEMO list. In real scenario, you need a backend.
    // But for local txt files, we'll use a manual list approach.
    
    // Option 1: Manual list (simple)
    const chapters = ['chapter1', 'chapter2', 'chapter3'];
    
    // Dynamically add to dropdown
    chapters.forEach(ch => {
        if (![...chapterSelect.options].some(opt => opt.value === ch)) {
            const option = document.createElement('option');
            option.value = ch;
            option.textContent = ch.replace('chapter', 'Chapter ');
            chapterSelect.appendChild(option);
        }
    });

    async function loadStory(chapterId) {
        storyContent.innerHTML = '<p>📖 Loading story... Please wait.</p>';
        
        try {
            // Important: Browser security blocks direct file access.
            // So best solution: Use fetch with a local server OR
            // for pure local viewing, use an input file selector alternative.
            
            // Simple alternative: User manually selects txt file
            // But here we'll show a message and provide a manual file picker option
            
            storyContent.innerHTML = `
                <div style="text-align: center; padding: 40px;">
                    <p>⚠️ <strong>Note:</strong> Browser security doesn't allow direct loading of local .txt files automatically.</p>
                    <p>But don't worry! Aap yeh karein:</p>
                    <br>
                    <label for="filePicker" style="background: #3498db; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer; display: inline-block;">📁 Select ${chapterId}.txt file</label>
                    <input type="file" id="filePicker" accept=".txt" style="display: none;">
                    <br><br>
                    <p>Ya fir, ek simple local server use karein (jaise VS Code Live Server)</p>
                    <p><strong>Best solution:</strong> Apne stories folder mein <code>chapter1.txt, chapter2.txt</code> rakhein aur VS Code ka "Live Server" use karein.</p>
                </div>
            `;
            
            // File picker functionality
            const filePicker = document.getElementById('filePicker');
            if (filePicker) {
                filePicker.remove(); // remove old if exists
            }
            
            const newFilePicker = document.createElement('input');
            newFilePicker.type = 'file';
            newFilePicker.accept = '.txt';
            newFilePicker.id = 'dynamicFilePicker';
            newFilePicker.style.display = 'none';
            document.body.appendChild(newFilePicker);
            
            const label = document.querySelector('label[for="filePicker"]');
            if (label) {
                label.setAttribute('for', 'dynamicFilePicker');
                newFilePicker.addEventListener('change', function(event) {
                    const file = event.target.files[0];
                    if (file) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const content = e.target.result;
                            storyContent.innerHTML = `<pre style="white-space: pre-wrap; font-family: inherit;">${escapeHtml(content)}</pre>`;
                        };
                        reader.readAsText(file, 'UTF-8');
                    }
                });
            }
            
        } catch (error) {
            storyContent.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    loadBtn.addEventListener('click', () => {
        const selectedChapter = chapterSelect.value;
        loadStory(selectedChapter);
    });
    
    // Alternative better approach: (For advanced users)
    // Agar aapke paas local server hai (jaise XAMPP ya python http.server)
    // toh fetch('/stories/chapter1.txt') directly kaam karega.
    
    // Yahan maine dusra version bhi likh raha hu jo local server ke liye hai (uncomment karein agar aapke paas server hai)
    
    /*
    async function loadStoryFromServer(chapterId) {
        storyContent.innerHTML = '<p>Loading...</p>';
        try {
            const response = await fetch(`/stories/${chapterId}.txt`);
            if (!response.ok) throw new Error('Chapter not found');
            const text = await response.text();
            storyContent.innerHTML = `<pre style="white-space: pre-wrap;">${escapeHtml(text)}</pre>`;
        } catch (err) {
            storyContent.innerHTML = `<p style="color:red;">Error: ${err.message}. Ensure stories folder exists and files are there.</p>`;
        }
    }
    
    loadBtn.addEventListener('click', () => loadStoryFromServer(chapterSelect.value));
    */
});