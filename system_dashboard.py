import http.server
import socketserver
import webbrowser
import json
import os
import threading
from datetime import datetime

# --- CONFIGURATION ---
PORT = 8080
DATA_FILE = "tracker_data.json"

# --- HTML WITH ORIGINAL CSS PRESERVED ---
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ultimate Habit Tracker</title>
    <style>
    
        /* -------------------------------------------------------------
             DARK ADVANCED THEME — preserves all ids, classNames & JS
             only CSS variables, selectors, backdrop effects, animations
        ------------------------------------------------------------- */
        
        :root {
            /* dark base — smooth deep background, neon‑touched accents */
            --bg-body: #0c0f15;
            --surface: #1a1e26;
            --surface-hover: #252b36;
            --border-subtle: #2d3440;
            --border-strong: #404b5c;
            --text-primary: #e9edf2;
            --text-secondary: #a6b3cc;
            --text-muted: #6f7c94;
            --primary-accent: green;        /* fresh mint green */
            --primary-glow: rgba(39, 196, 111, 0.25);
            --accent-blue: #4d8cff;
            --danger-accent: #ff5f6d;
            --danger-glow: rgba(255, 95, 109, 0.2);
            --chart-line: #4d8cff;
            --chart-fill-start: rgba(77, 140, 255, 0.25);
            --chart-fill-end: rgba(77, 140, 255, 0.02);
            --shadow-elevation: 0 10px 30px -10px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(75, 130, 200, 0.1) inset;
            --radius-lg: 20px;
            --radius-md: 14px;
            --radius-sm: 10px;
            --transition-smooth: all 0.2s cubic-bezier(0.2, 0.9, 0.3, 1);
        }
        * {box-sizing: border-box;outline: none;}
        body {font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;background-color: var(--bg-body);color: var(--text-primary);margin: 0;padding: 10px;min-height: 100vh;background-image: radial-gradient(circle at 10% 20%, rgba(45, 140, 255, 0.03) 0%, transparent 40%),radial-gradient(circle at 90% 70%, rgba(39, 196, 111, 0.03) 0%, transparent 40%);font-weight: 400;line-height: 1.5;font-size: 14px;}
        .toolbar {background: rgba(26, 30, 38, 0.8);backdrop-filter: blur(15px) saturate(180%);-webkit-backdrop-filter: blur(15px) saturate(180%);border: 1px solid rgba(64, 75, 92, 0.5);box-shadow: 0 12px 30px -10px black, 0 0 0 1px rgba(77, 140, 255, 0.15) inset;padding: 8px 15px;border-radius: var(--radius-lg);display: flex;justify-content: space-between;align-items: center;margin-bottom: 15px;flex-wrap: wrap;gap: 10px;}
        .brand h1 {margin: 0;font-size: 1.2rem;font-weight: 700;background: linear-gradient(130deg, #b3e6ff, #9effb4);-webkit-background-clip: text;background-clip: text;color: transparent;letter-spacing: -0.02em;text-shadow: 0 0 10px rgba(77, 140, 255, 0.4);}
        .brand p {margin: 2px 0 0;font-size: 0.6rem;color: var(--text-secondary);text-transform: uppercase;letter-spacing: 1px;}
        .nav-controls {display: flex;gap: 8px;align-items: center;}
        button {padding: 4px 12px;border: 1px solid var(--border-strong);background: var(--surface);color: var(--text-secondary);border-radius: 20px;font-weight: 500;font-size: 0.8rem;cursor: pointer;transition: var(--transition-smooth);box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3), 0 1px 0 rgba(255, 255, 255, 0.03) inset;backdrop-filter: blur(5px);letter-spacing: 0.3px;}
        button:hover {background: var(--surface-hover);border-color: var(--primary-accent);color: white;transform: translateY(-2px);box-shadow: 0 10px 20px -5px rgba(39, 196, 111, 0.3);}
        .btn-primary {background: linear-gradient(145deg, #1f8a4f, #13663a);border: none;color: white;font-weight: 600;box-shadow: 0 6px 14px rgba(39, 196, 111, 0.3), 0 0 0 1px rgba(255,255,255,0.06) inset;}
        .btn-primary:hover {background: linear-gradient(145deg, #27c46f, #188f4b);box-shadow: 0 12px 22px -6px #27c46f;border: none;transform: translateY(-2px);}
        #monthDisplay {font-weight: 600;min-width: 100px;text-align: center;color: var(--text-primary);background: rgba(0,0,0,0.3);padding: 4px 8px;border-radius: 30px;border: 1px solid var(--border-strong);letter-spacing: 0.5px;font-size: 0.9rem;}
        .main-layout {display: flex;flex-direction: column;flex-wrap: nowrap;justify-content: center;gap: 15px;}
        .card {background: var(--surface);border-radius: var(--radius-lg);box-shadow: 0 20px 35px -12px black, 0 0 0 1px rgba(77, 140, 255, 0.15) inset;padding: 15px;display: flex;flex-direction: column;backdrop-filter: blur(2px);transition: var(--transition-smooth);}
        .card:hover {box-shadow: 0 24px 45px -12px black, 0 0 0 1px var(--primary-accent) inset;}
        h2 {margin-top: 0;margin-bottom: 10px;color: var(--text-primary);font-size: 1.1rem;font-weight: 500;border-bottom: 2px solid transparent;border-image: linear-gradient(90deg, var(--primary-accent), var(--accent-blue)) 1;border-bottom-style: solid;padding-bottom: 6px;display: inline-block;letter-spacing: -0.2px;}
        .table-wrapper {overflow-x: auto;border: 1px solid var(--border-subtle);border-radius: var(--radius-md);margin-bottom: 10px;background: #13171f;box-shadow: inset 0 4px 10px rgba(0,0,0,0.6);}
        table {width: 100%;border-collapse: collapse;min-width: 600px;background: transparent;font-size: 0.8rem;}
        th {background-color: #1f2632;color: var(--primary-accent);font-weight: 600;padding: 8px 5px;text-align: center;position: sticky;top: 0;z-index: 5;border-bottom: 2px solid var(--primary-accent);font-size: 0.75rem;text-transform: uppercase;letter-spacing: 0.5px;backdrop-filter: blur(4px);box-shadow: 0 1px 0 var(--border-strong) inset;}
        td {padding: 6px 4px;border-bottom: 1px solid var(--border-subtle);text-align: center;transition: background 0.15s;color: var(--text-secondary);font-size: 0.75rem;border-right: 1px solid black;}
        .habit-name {text-align: left !important;font-weight: 600;color: var(--text-primary);padding-left: 10px !important;min-width: 150px;font-size: 0.8rem;border-right: 1px solid var(--border-subtle);}
        .checkbox-indicator {width: 18px;height: 18px;display: inline-block;border-radius: 4px;background: transparent;transition: all 0.2s ease;}
        .checked-cell .checkbox-indicator {background: transparent;}
        .input-group {display: flex;gap: 8px;background: #13171f;padding: 10px 12px;border-radius: 30px;border: 1px solid var(--border-strong);box-shadow: 0 2px 8px rgba(0,0,0,0.5), inset 0 1px 2px rgba(255,255,255,0.02);}
        input[type="text"] {flex: 1;padding: 8px 12px;border: 1px solid var(--border-subtle);border-radius: 30px;font-size: 0.8rem;background: #0d121b;color: var(--text-primary);transition: var(--transition-smooth);box-shadow: inset 0 3px 8px rgba(0,0,0,0.6);}
        input[type="text"]:focus {border-color: var(--primary-accent);background: #111722;box-shadow: 0 0 0 3px var(--primary-glow), inset 0 2px 5px black;}
        .status-bar {margin-top: 10px;font-size: 0.7rem;color: var(--text-secondary);display: flex;align-items: center;gap: 8px;padding: 5px 12px;border-radius: 30px;background: #1a1f29;border: 1px solid var(--border-strong);backdrop-filter: blur(2px);}
        .dot {width: 8px;height: 8px;border-radius: 50%;background: #4f5b6b;box-shadow: 0 0 8px currentColor;transition: background 0.3s, box-shadow 0.3s;}
        .saved .dot {background: var(--primary-accent);box-shadow: 0 0 14px #27c46f;}
        .saving .dot {background: var(--accent-blue);animation: pulse-blue 1.2s infinite ease-in-out;box-shadow: 0 0 12px #4d8cff;}
        .error .dot {background: var(--danger-accent);box-shadow: 0 0 14px #ff5f6d;}@keyframes pulse-blue {0% { opacity: 0.7; transform: scale(1);}50% { opacity: 1; transform: scale(1.3); background: #7aabff; }100% { opacity: 0.7; transform: scale(1); }}
        .chart-container {background: #13171f;border-radius: var(--radius-md);padding: 10px;border: 1px solid var(--border-strong);height: 200px;display: flex;align-items: center;justify-content: center;box-shadow: inset 0 0 25px rgba(0,0,0,0.8), 0 8px 18px black;}
        canvas {width: 100%;height: 100%;display: block;border-radius: 8px;filter: drop-shadow(0 4px 10px rgba(39, 196, 111, 0.2));}
        .habit-name span {color: var(--danger-accent) !important;opacity: 0.8 !important;font-size: 1rem;font-weight: 500;transition: var(--transition-smooth);background: rgba(255,95,109,0.1);width: 20px;height: 20px;display: inline-flex;align-items: center;justify-content: center;border-radius: 50%;margin-left: 5px;}
        .habit-name span:hover {opacity: 1 !important;background: rgba(255,95,109,0.25);transform: scale(1.15);box-shadow: 0 0 12px var(--danger-glow);}
        @media (max-width: 900px) {.main-layout { grid-template-columns: 1fr; }
        .toolbar { flex-direction: column; align-items: flex-start; }
        .card { padding: 15px; }}
        .table-wrapper::-webkit-scrollbar {width: 8px;height: 8px;}
        .table-wrapper::-webkit-scrollbar-track {background: #1a1f29;border-radius: 10px;}
        .table-wrapper::-webkit-scrollbar-thumb {background: #3a4555;border-radius: 10px;border: 2px solid #1a1f29;}
        .table-wrapper::-webkit-scrollbar-thumb:hover {background: var(--primary-accent);}
        .nav-controls > div[style*="background:var(--border)"] {background: var(--border-strong) !important;width: 1px !important;height: 16px !important;opacity: 0.5;}
        input::placeholder { color: #536277; font-style: italic; font-size: 0.8rem; }
        .checked-cell {background: green !important;box-shadow: inset 0 0 12px rgba(39, 196, 111, 0.4);transition: 0.2s;border: 1px solid black;}
        .past-missed-cell {background: #ff4d4d !important;box-shadow: inset 0 0 12px rgba(255, 0, 0, 0.4);border: 1px solid black;opacity: 0.9;}
        td {position: relative;}
        td[onclick]{cursor: pointer;}
        td:active {transform: scale(0.95);}
        .analytics-grid {display: grid;grid-template-columns: 1fr 1fr;gap: 10px;margin-bottom: 15px;}
        .summary-stats {display: grid;grid-template-columns: repeat(3, 1fr);gap: 8px;margin-bottom: 15px;}
        .stat-box {background: #1e2531;border-radius: var(--radius-md);padding: 8px;text-align: center;border: 1px solid var(--border-strong);}
        .stat-value {font-size: 1.2rem;font-weight: 700;color: var(--primary-accent);}
        .stat-label {font-size: 0.6rem;color: var(--text-muted);text-transform: uppercase;}
        .habit-progress-item {background: #1e2531;border-radius: var(--radius-md);padding: 8px;margin-bottom: 6px;border: 1px solid var(--border-strong);}
        .progress-bar-container {width: 100%;height: 26px;background: var(--surface);overflow: hidden;box-shadow: 0 0 10px 4px black;position: relative;border-radius: 4px;margin: 10px 0;}
        .progress-bar-fill {height: 100%;background: linear-gradient(90deg,transparent 0%, green 10%);transition: width 0.3s ease;position: relative;}
        .progress-text {position: absolute;right: 8px;top: 50%;transform: translateY(-50%);color: white;font-size: 0.8rem;font-weight: 700;text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);}
        .weekly-breakdown {display: flex;flex-wrap: nowrap;flex-direction: column;}
        .week-card {background: #1e2531;border-radius: var(--radius-md);margin: 25px;border: 1px solid var(--border-strong);}
        .week-title {color: green;font-weight: 700;margin-bottom: 15px;text-align: center;font-size: 1rem;}
        .daily-bars {display: flex;gap: 25px;justify-content: center;}
        .daily-bar {width: 65px; height: 204px;box-shadow: 0 0 10px 4px black; background: #0000001a;margin: 0 auto; position: relative; overflow: hidden;border-radius: 4px;transform: matrix3d(1, 0.1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1);}
        .daily-fill {position: absolute; bottom: 0; width: 100%; height: 18.8%;background: linear-gradient(transparent 0%, green 10%)}
        .current-missed-cell{background: radial-gradient(black,transparent);}
    </style>
</head>
<body>
    <div class="toolbar">
        <div class="brand">
            <h1>Ultimate Tracker</h1>
            <p>HD Auto-Save Edition</p>
        </div>
        <div class="nav-controls">
            <button onclick="changeMonth(-1)">❮ Prev</button>
            <span id="monthDisplay">January 2025</span>
            <button onclick="changeMonth(1)">Next ❯</button>
            <div style="width:1px; height:16px; background:var(--border-strong); margin:0 5px;"></div>
            <button class="btn-primary" onclick="forceSave()">💾 Save</button>
        </div>
    </div>

    <!-- Summary Stats -->
    <div class="summary-stats">
        <div class="stat-box">
            <div class="stat-value" id="overallCompleted">0%</div>
            <div class="stat-label">Overall</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="totalHabits">0</div>
            <div class="stat-label">Habits</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="bestStreak">0</div>
            <div class="stat-label">Streak</div>
        </div>
    </div>

    <div class="main-layout">
        <!-- Left Column: Daily Habits -->
        <div class="card">
            <h2>Daily Habits</h2>
            <div class="table-wrapper">
                <table>
                    <thead>
                        <tr id="headerRow"></tr>
                    </thead>
                    <tbody id="gridBody"></tbody>
                </table>
            </div>
            <div class="input-group">
                <input type="text" id="newHabit" placeholder="New habit..." autocomplete="off">
                <button class="btn-primary" onclick="addHabit()">+ Add</button>
            </div>
            <div class="status-bar" id="statusBar">
                <div class="dot"></div> 
                <span>Ready</span>
            </div>
        </div>

        <!-- Right Column: Analytics -->
        <div class="card">
            <h2>Progress Analytics</h2>
            
            <!-- Donut Chart -->
            <div class="analytics-grid">
                <div>
                    <p style="color:var(--text-secondary); font-size:0.7rem;">Overview</p>
                    <canvas id="donutChart" style="max-height: 120px;"></canvas>
                </div>
                <div>
                    <p style="color:var(--text-secondary); font-size:0.7rem;">Daily</p>
                    <canvas id="lineChart" style="max-height: 120px;"></canvas>
                </div>
            </div>

            <!-- Global Progress -->
            <div style="margin-top: 15px;">
                <p style="color:var(--text-secondary); margin-bottom: 8px; font-size:0.8rem;">Weekly Progress</p>
                <div id="globalProgress" style="display: flex; gap: 8px; justify-content: space-around;">
                    <!-- Populated by JS -->
                </div>
            </div>

            <!-- Per Habit Progress -->
            <div style="margin-top: 15px;">
                <p style="color:var(--text-secondary); margin-bottom: 8px; font-size:0.8rem;">Habit Progress</p>
                <div id="habitProgress" style="overflow-y: auto;">
                    <!-- Populated by JS -->
                </div>
            </div>

            <!-- Weekly Breakdown -->
            <div style="margin-top: 15px;">
                <p style="color:var(--text-secondary); margin-bottom: 8px; font-size:0.8rem;">Weekly Breakdown</p>
                <div class="weekly-breakdown" id="weeklyBreakdown">
                    <!-- Populated by JS -->
                </div>
            </div>

            <!-- Max Score Label -->
            <div style="text-align:center; margin-top:10px; font-size:0.7rem; color:var(--text-muted);">
                <span id="maxScoreLabel">Max: 0</span> points
            </div>
        </div>
    </div>

    <script>
    // ===== STATE MANAGEMENT =====
    let currentDate = new Date();
    console.log(currentDate);
    let trackerData = { habits: [], checks: {} };
    let saveTimeout;
    let lastSaveTime = null;
    let donutChart, lineChart;

    // ===== API FUNCTIONS =====
    async function loadData() {
        try {
            const res = await fetch('http://localhost:8080/load', { method: 'GET' });
            if (!res.ok) throw new Error('Server error');
            const data = await res.json();
            trackerData = data;
            if (!trackerData.habits) trackerData.habits = [];
            if (!trackerData.checks) trackerData.checks = {};
            updateStatus("Connected", "saved");
            renderApp();
        } catch (e) {
            updateStatus("Connection Failed", "error");
        }
    }

    async function saveData(showMsg = false) {
        updateStatus("Saving...", "saving");
        try {
            await fetch('http://localhost:8080/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(trackerData)
            });
            lastSaveTime = new Date();
            if(showMsg) updateStatus("Saved", "saved");
            else updateStatus("Synced", "saved");
        } catch (e) { 
            updateStatus("Save Failed", "error"); 
        }
    }

    function updateStatus(msg, type) {
        const el = document.getElementById('statusBar');
        el.innerHTML = `<div class="dot"></div> <span>${msg}</span>`;
        el.className = "status-bar " + type;
    }

    function triggerAutoSave() {
        updateStatus("Pending...", "saving");
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => saveData(false), 1000); 
    }
    
    function forceSave() { 
        saveData(true); 
    }

    function getMonthKey() { 
        return currentDate.getFullYear() + "-" + String(currentDate.getMonth()+1).padStart(2,'0'); 
    }

    // ===== RENDERING =====
    function renderApp() {
        const key = getMonthKey();
        if(!trackerData[key]) {
            trackerData[key] = { 
                habits: trackerData.habits.length ? [...trackerData.habits] : ["Eat Healthy", "Exercise", "Drink Water"], 
                checks: {} 
            };
        }
        
        const monthData = trackerData[key];
        const days = new Date(currentDate.getFullYear(), currentDate.getMonth()+1, 0).getDate();
        
        document.getElementById('monthDisplay').innerText = 
            currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });

        // Render table header
        let hHTML = "<th>Habit Name</th>";
        for(let i=1; i<=days; i++) {
            const isToday = i === new Date().getDate() && 
                           currentDate.getMonth() === new Date().getMonth() &&
                           currentDate.getFullYear() === new Date().getFullYear();
            hHTML += `<th style="${isToday ? 'color: var(--primary-accent); font-weight: bold;' : ''}">${i}</th>`;
        }
        document.getElementById('headerRow').innerHTML = hHTML;

        // Get current date info
        const today = new Date();
        const isCurrentMonth = currentDate.getMonth() === today.getMonth() && 
                              currentDate.getFullYear() === today.getFullYear();
        const todayIndex = today.getDate() - 1; // 0-based index

        // Render table body
        let bHTML = "";
        monthData.habits.forEach((habit, r) => {
            bHTML += `<tr><td class="habit-name">${habit} <span onclick="deleteHabit(${r})" title="Delete">&times;</span></td>`;
            if(!monthData.checks[r]) monthData.checks[r] = [];
            while(monthData.checks[r].length < days) monthData.checks[r].push(false);
            
            for(let d=0; d<days; d++) {
                const isChecked = monthData.checks[r][d];
                
                // Cell class logic
                let cellClass = "";
                
                if(isChecked) {
    cellClass = "checked-cell";
}
else {
    if(isCurrentMonth && d < todayIndex) {
        cellClass = "past-missed-cell";
    }
    else if(!isCurrentMonth) {
        cellClass = "past-missed-cell";
    }
    else if(isCurrentMonth && d === todayIndex) {
        cellClass = "current-missed-cell";
    }
}
                // Clickable only for current month, past dates and today
                const clickable = isCurrentMonth && (d <= todayIndex);
                
                bHTML += `<td class="${cellClass}" ${clickable ? 'onclick="toggleCheck(' + r + ',' + d + ')"' : ''}></td>`;
            }
            bHTML += "</tr>";
        });
        document.getElementById('gridBody').innerHTML = bHTML;

        // Update all charts and stats
        updateStats(monthData, days);
        renderDonutChart(monthData, days);
        renderLineChart(monthData, days);
        renderGlobalProgress(monthData, days);
        renderHabitProgress(monthData, days);
        renderWeeklyBreakdown(monthData, days);
    }

    function toggleCheck(r, d) {
        const key = getMonthKey();
        if (!trackerData[key] || !trackerData[key].checks[r]) return;
        
        // Double-check that we're only modifying current month
        const today = new Date();
        const isCurrentMonth = currentDate.getMonth() === today.getMonth() && 
                              currentDate.getFullYear() === today.getFullYear();
        const todayIndex = today.getDate() - 1;
        const isPastOrToday = d <= todayIndex;
        
        if (isCurrentMonth && isPastOrToday) {
            trackerData[key].checks[r][d] = !trackerData[key].checks[r][d];
            triggerAutoSave();
            renderApp();
        }
    }

    function addHabit() {
        const val = document.getElementById('newHabit').value.trim();
        if(!val) return;
        
        const key = getMonthKey();
        if(!trackerData[key]) trackerData[key] = { habits: [], checks: {} };
        
        const days = new Date(currentDate.getFullYear(), currentDate.getMonth()+1, 0).getDate();
        trackerData[key].habits.push(val);
        trackerData[key].checks[trackerData[key].habits.length-1] = new Array(days).fill(false);
        
        document.getElementById('newHabit').value = "";
        triggerAutoSave();
        renderApp();
    }

    function deleteHabit(idx) {
        if(!confirm("Delete this habit permanently?")) return;
        
        const key = getMonthKey();
        trackerData[key].habits.splice(idx, 1);
        delete trackerData[key].checks[idx];
        
        // Reindex checks
        const newChecks = {};
        Object.keys(trackerData[key].checks).forEach((oldIndex, newIndex) => {
            if(parseInt(oldIndex) !== idx) {
                if(parseInt(oldIndex) > idx) {
                    newChecks[newIndex] = trackerData[key].checks[oldIndex];
                } else {
                    newChecks[oldIndex] = trackerData[key].checks[oldIndex];
                }
            }
        });
        trackerData[key].checks = newChecks;
        
        triggerAutoSave();
        renderApp();
    }

    function changeMonth(delta) {
        currentDate.setMonth(currentDate.getMonth() + delta);
        const key = getMonthKey();
        if(!trackerData[key]) {
            trackerData[key] = { 
                habits: trackerData.habits.length ? [...trackerData.habits] : ["Eat Healthy", "Exercise", "Drink Water"], 
                checks: {} 
            };
        }
        renderApp();
    }

    // ===== STATISTICS =====
    function updateStats(monthData, days) {
        let totalCompleted = 0;
        let totalPossible = 0;
        const today = Math.min(new Date().getDate(), days);
        
        for(let day=0; day<today; day++) {
            for(let habit=0; habit<monthData.habits.length; habit++) {
                if(monthData.checks[habit] && monthData.checks[habit][day]) {
                    totalCompleted++;
                }
                totalPossible++;
            }
        }
        
        const overallPercent = totalPossible > 0 ? ((totalCompleted / totalPossible) * 100).toFixed(1) : 0;
        
        document.getElementById('overallCompleted').textContent = overallPercent + '%';
        document.getElementById('totalHabits').textContent = monthData.habits.length;
        document.getElementById('maxScoreLabel').textContent = 'Max: ' + monthData.habits.length;

        // Calculate best streak
        let bestStreak = 0;
        let currentStreak = 0;
        
        for(let day=0; day<today; day++) {
            let allChecked = true;
            for(let habit=0; habit<monthData.habits.length; habit++) {
                if(!monthData.checks[habit] || !monthData.checks[habit][day]) {
                    allChecked = false;
                    break;
                }
            }
            
            if(allChecked) {
                currentStreak++;
                bestStreak = Math.max(bestStreak, currentStreak);
            } else {
                currentStreak = 0;
            }
        }
        
        document.getElementById('bestStreak').textContent = bestStreak;
    }

    function renderDonutChart(monthData, days) {
        const ctx = document.getElementById('donutChart').getContext('2d');
        
        let totalCompleted = 0;
        let totalPossible = 0;
        const today = Math.min(new Date().getDate(), days);
        
        for(let day=0; day<today; day++) {
            for(let habit=0; habit<monthData.habits.length; habit++) {
                if(monthData.checks[habit] && monthData.checks[habit][day]) {
                    totalCompleted++;
                }
                totalPossible++;
            }
        }
        
        const completed = totalPossible > 0 ? (totalCompleted / totalPossible) * 100 : 0;
        const left = 100 - completed;

        if(donutChart) donutChart.destroy();

        donutChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'Left'],
                datasets: [{
                    data: [completed, left],
                    backgroundColor: ['#27c46f', '#ff5f6d'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                cutout: '70%',
                plugins: { legend: { display: false } }
            }
        });
    }

    function renderLineChart(monthData, days) {
        const ctx = document.getElementById('lineChart').getContext('2d');
        
        const labels = [];
        const data = [];
        
        for(let day=0; day<days; day++) {
            labels.push(day + 1);
            let completed = 0;
            for(let habit=0; habit<monthData.habits.length; habit++) {
                if(monthData.checks[habit] && monthData.checks[habit][day]) {
                    completed++;
                }
            }
            const percentage = (completed / monthData.habits.length) * 100;
            data.push(percentage);
        }

        if(lineChart) lineChart.destroy();

        lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    borderColor: '#27c46f',
                    backgroundColor: 'rgba(39, 196, 111, 0.1)',
                    borderWidth: 2,
                    pointBackgroundColor: '#27c46f',
                    pointBorderColor: 'white',
                    pointRadius: 3,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { callback: value => value + '%', font: { size: 8 } }
                    },
                    x: { display: false }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    function renderGlobalProgress(monthData, days) {
        const container = document.getElementById('globalProgress');
        const weeks = Math.ceil(days / 7);
        let html = '';
        
        for(let week=0; week<weeks; week++) {
            let weekCompleted = 0;
            let weekTotal = 0;
            
            const startDay = week * 7;
            const endDay = Math.min(startDay + 7, days);
            
            for(let day=startDay; day<endDay; day++) {
                for(let habit=0; habit<monthData.habits.length; habit++) {
                    if(monthData.checks[habit] && monthData.checks[habit][day]) {
                        weekCompleted++;
                    }
                    weekTotal++;
                }
            }
            
            const percentage = weekTotal > 0 ? ((weekCompleted / weekTotal) * 100).toFixed(1) : 0;
            
            html += `
                <div style="text-align: center;">
                    <div style="width: 65px; height: 204px;box-shadow: 0 0 10px 4px black; background: #0000001a;margin: 0 auto; position: relative; overflow: hidden;border-radius: 4px;transform: matrix3d(1, 0.1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1);">
                        <div style="position: absolute; bottom: 0; width: 100%; height: ${percentage}%;background: linear-gradient(transparent 0%, green 10%)"></div>
                    </div>
                    <div style="margin-top: 3px; color: #27c46f; font-weight: 600; font-size:0.7rem;">${percentage}%</div>
                    <div style="font-size: 0.6rem; color: #a6b3cc;">W${week+1}</div>
                </div>
            `;
        }
        
        container.innerHTML = html;
    }

    function renderHabitProgress(monthData, days) {
        const container = document.getElementById('habitProgress');
        const today = Math.min(new Date().getDate(), days);
        let html = '';
        
        monthData.habits.forEach((habit, index) => {
            let completed = 0;
            for(let day=0; day<today; day++) {
                if(monthData.checks[index] && monthData.checks[index][day]) {
                    completed++;
                }
            }
            
            const percentage = ((completed / today) * 100).toFixed(1);
            
            html += `
                <div class="habit-progress-item">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                        <span style="color: #e9edf2; font-size:0.75rem;">${habit}</span>
                        <span style="color: #a6b3cc; font-size:0.7rem;">${completed}/${today}</span>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill" style="width: ${percentage}%;">
                            <span class="progress-text">${percentage}%</span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
    }

    function renderWeeklyBreakdown(monthData, days) {
        const container = document.getElementById('weeklyBreakdown');
        const weeks = Math.ceil(days / 7);
        let html = '';
        
        for(let week=0; week<weeks; week++) {
            const startDay = week * 7;
            const endDay = Math.min(startDay + 7, days);
            
            html += `
                <div class="week-card">
                    <div class="week-title">W${week+1}</div>
                    <div class="daily-bars">
            `;
            
            for(let day=startDay; day<endDay; day++) {
                let completed = 0;
                for(let habit=0; habit<monthData.habits.length; habit++) {
                    if(monthData.checks[habit] && monthData.checks[habit][day]) {
                        completed++;
                    }
                }
                
                const height = (completed / monthData.habits.length) * 100;
                
                html += `
                    <div class="daily-bar">
                        <div class="daily-fill" style="height: ${height}%;"></div>
                    </div>
                `;
            }
            
            html += `
                    </div>
                    <div style="text-align: center; margin-top: 15px; color: #a6b3cc; font-size: 1rem;">
                        ${startDay+1}-${endDay}
                    </div>
                </div>
            `;
        }
        
        container.innerHTML = html;
    }

    // ===== INITIALIZATION =====
    window.onload = loadData;
    window.addEventListener('resize', () => renderApp());
</script>
"""

# ===== ENHANCED PYTHON SERVER =====
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
        elif self.path == "/load":
            try:
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        data = f.read()
                else:
                    default_data = {
                        "habits": [
                            "Eat Healthy",
                            "Exercise",
                            "Drink Water",
                            "Read",
                            "Meditate",
                        ],
                        "checks": {},
                    }
                    data = json.dumps(default_data, indent=2)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/save":
            try:
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)

                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    f.write(post_data.decode("utf-8"))

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                self.send_response(500)
                self.end_headers()


def start_server():
    global PORT
    server = None
    retry_count = 0

    while retry_count < 3:
        try:
            server = ThreadedHTTPServer(("localhost", PORT), CORSRequestHandler)
            break
        except OSError:
            print(f"Port {PORT} busy, trying {PORT + 1}")
            PORT += 1
            retry_count += 1

    if not server:
        print("No available port found")
        return

    print("\n" + "=" * 60)
    print("🚀 Ultimate Habit Tracker")
    print("=" * 60)
    print(f"📱 Local URL: http://localhost:{PORT}")
    print(f"💾 Data file: {DATA_FILE}")
    print("=" * 60)
    print("\n✅ Features:")
    print("   • Only current month editable")
    print("   • Past missed dates: 🔴 Red background")
    print("   • Current day: ⚪ Transparent with green border + dot")
    print("   • Checked dates: 🟢 Green background")
    print("   • No checkboxes - click cells to toggle")
    print("   • All analytics preserved")
    print("\n📝 Press Ctrl+C to stop\n")

    webbrowser.open(f"http://localhost:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")


if __name__ == "__main__":
    start_server()
