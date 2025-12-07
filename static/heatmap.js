// Get the base path from the current location
const pathParts = window.location.pathname.split('/').filter(Boolean);
let basePath = '';
if (pathParts.length > 0) {
    const firstPath = pathParts[0].toLowerCase();
    if (firstPath === 'risk-reward' || firstPath === 'riskreward') {
        basePath = '/' + pathParts[0]; // Use the actual case from URL
    }
}

// Category mappings - using short names that match the CSV columns
const categories = {
    'Broad': ['N50', 'NN50', 'N100', 'N200', 'NTOTLM', 'N500', 'NMC5025', 'N500EQ', 'NMC150', 'NMC50', 'NMCSEL', 'NMC100', 'NSC250', 'NSC50', 'NSC100', 'NMICRO', 'NLMC250', 'NMSC400', 'NT10EWT', 'NT15EWT', 'NT20EWT', 'N50EQWGT', 'NIFTY500 EQUAL WEIGHT.1'],
    'Sector': ['NAUTO', 'NBANK', 'NCHEM', 'NFINSERV', 'NFINS2550', 'NFINSXB', 'NFMCG', 'NHEALTH', 'NTECH', 'NMEDIA', 'NMETAL', 'NPHARMA', 'NPVTBANK', 'NPSUBANK', 'NREALTY', 'NCONDUR', 'NOILGAS', 'NMSFINS', 'NMSHC', 'NMSITT', 'NCAPMRKT', 'NCOMM', 'NSERVSEC'],
    'Strategy': ['N100EWT', 'N100LV30', 'N200M30', 'N200AL30', 'N100AL30', 'NAL50', 'NALV30', 'NAQLV30', 'NAQVLV30', 'NDIVOP50', 'NLV50', 'NHBET50', 'NGROW15', 'N100QL30', 'N200QL30', 'NQLLV30', 'N500QL50', 'N500M50', 'N500LV50', 'N500V50', 'N500MQLV', 'N500MQ50', 'N50V20', 'N200V30', 'NMC150M50', 'NMC150Q', 'N500FQ30', 'NSC250Q', 'NMSCMQ', 'NSC250MQ', 'N100LIQ15', 'NMCL15', 'N50SH', 'N500SH', 'NSH25'],
    'Thematic': ['NICON', 'NIDEF', 'NIDIGI', 'NIIL', 'NIMFG', 'NCPSE', 'NENRGY', 'NEVNAA', 'NHOUS', 'N100ESG', 'N100ESGE', 'N100ESGSL', 'NINFRA', 'NTOUR', 'NINACON', 'NCHOUS', 'NMSICON', 'NMOBIL', 'NNCCON', 'NRURAL', 'NTRANS', 'NIINT', 'NPSE', 'NMNC', 'NREIT', 'NIPO', 'NSMEE', 'NIRLPSU', 'NBIRLA', 'NMAHIN', 'NTATA', 'NTATA25', 'NMAATR', 'NMF5032', 'NINF5032', 'NWAVES', 'DSPQ', 'DSP ELSS', 'KBIK CON', 'KBIK GOLD', 'AXISINVE', 'UTI FLEX', 'ICICI SIL', 'N10YRGS', 'NIFTY 10 YR BENCHMARK G-SEC.1']
};

const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

let currentData = [];
let currentSort = { column: 'name', ascending: true };

// Load and display data based on URL parameters
async function loadHeatmapData() {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');
    const index = urlParams.get('index');

    // If index parameter exists, show monthly heatmap for that index
    if (index) {
        await loadIndexHeatmap(index);
    } 
    // If category parameter exists, show category table
    else if (category) {
        await loadCategoryTable(category);
    } 
    else {
        document.getElementById('loading').textContent = 'No index or category specified';
    }
}

// Load monthly heatmap for a specific index
async function loadIndexHeatmap(indexName) {
    try {
        const mode = document.getElementById('return-mode')?.value || 'trailing';
        const timeline = document.getElementById('timeline')?.value || '3';
        const cacheBuster = new Date().getTime();
        const res = await fetch(`${basePath}/api/heatmap_data?index=${encodeURIComponent(indexName)}&duration=all&mode=${mode}&timeline=${timeline}&_=${cacheBuster}`);
        if (!res.ok) throw new Error('Failed to fetch heatmap data');
        
        const data = await res.json();
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('heatmap-container').classList.remove('hidden');
        document.getElementById('category-title').textContent = indexName;
        
        renderMonthlyHeatmap(data);
    } catch (err) {
        document.getElementById('loading').textContent = 'Failed to load data: ' + err.message;
        console.error(err);
    }
}

// Load category table view
async function loadCategoryTable(category) {
    try {
        const res = await fetch(`${basePath}/api/metrics?duration=3years`);
        if (!res.ok) throw new Error('Failed to fetch data');
        
        const allData = await res.json();
        const categoryIndices = categories[category] || [];
        const categoryData = allData.filter(item => 
            categoryIndices.includes(item['Index Name'])
        );
        
        if (categoryData.length === 0) {
            document.getElementById('loading').textContent = 'No data found for this category';
            return;
        }

        categoryData.sort((a, b) => a['Index Name'].localeCompare(b['Index Name']));
        currentData = categoryData;
        
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('heatmap-container').classList.remove('hidden');
        document.getElementById('category-title').textContent = category;
        document.getElementById('category-label').textContent = category;

        renderCategoryTable(categoryData);
    } catch (err) {
        document.getElementById('loading').textContent = 'Failed to load data: ' + err.message;
        console.error(err);
    }
}

// Render monthly heatmap for an index
function renderMonthlyHeatmap(data) {
    const mode = document.getElementById('return-mode')?.value || 'trailing';
    const timeline = document.getElementById('timeline')?.value || '3';
    const modeText = mode === 'trailing' ? 'Trailing' : 'Rolling';
    const titleText = `${modeText} ${timeline}-Year Returns Heatmap`;
    
    const container = document.getElementById('heatmap-container');
    container.innerHTML = `
        <h1 style="font-size: 24px; font-weight: 700; margin-bottom: 20px;">${data.indexName}</h1>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
            <div style="background: linear-gradient(135deg, #007E6E 0%, #005550 100%); padding: 20px; border-radius: 10px; color: white;">
                <div style="font-size: 11px; opacity: 0.9; margin-bottom: 8px;">RETURN (CAGR)</div>
                <div style="font-size: 24px; font-weight: 700;">${data.cagr ? (data.cagr * 100).toFixed(2) + '%' : 'N/A'}</div>
            </div>
            <div style="background: linear-gradient(135deg, #73AF6F 0%, #5a8a57 100%); padding: 20px; border-radius: 10px; color: white;">
                <div style="font-size: 11px; opacity: 0.9; margin-bottom: 8px;">VOLATILITY</div>
                <div style="font-size: 24px; font-weight: 700;">${data.volatility ? (data.volatility * 100).toFixed(2) + '%' : 'N/A'}</div>
            </div>
            <div style="background: linear-gradient(135deg, #007E6E 0%, #005550 100%); padding: 20px; border-radius: 10px; color: white;">
                <div style="font-size: 11px; opacity: 0.9; margin-bottom: 8px;">CURRENT PRICE</div>
                <div style="font-size: 24px; font-weight: 700;">${data.currentPrice ? data.currentPrice.toFixed(2) : 'N/A'}</div>
            </div>
        </div>
        
        <h2 style="font-size: 16px; font-weight: 600; color: #666; margin-bottom: 20px; text-align: center;">${titleText}</h2>
        
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #628141;">
            <h3 style="font-size: 14px; font-weight: 600; color: #628141; margin-bottom: 12px;">📊 FORMULA USED:</h3>
            <div style="font-family: 'Courier New', monospace; font-size: 13px; color: #333; line-height: 1.8;">
                ${data.mode === 'trailing' 
                    ? `<strong>Trailing Return (Annualized):</strong><br>
                       ((Current_Price / Price_${data.timeline}_Years_Ago)^(1/${data.timeline}) - 1) × 100<br>
                       <span style="font-size: 11px; color: #666; font-family: sans-serif;">
                       Shows: Annualized return in the last ${data.timeline} years up to this month
                       </span>`
                    : `<strong>Rolling Return (Annualized):</strong><br>
                       ((Price_${data.timeline}_Years_After / Current_Price)^(1/${data.timeline}) - 1) × 100<br>
                       <span style="font-size: 11px; color: #666; font-family: sans-serif;">
                       Shows: Annualized return if you invested at this month for ${data.timeline} years
                       </span>`
                }<br><br>
                <strong>Color Legend:</strong><br>
                <span style="background: #628141; color: white; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">&gt; 30%</span>
                <span style="background: #8BAE66; color: white; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">20-30%</span>
                <span style="background: #A3D78A; color: white; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">10-20%</span>
                <span style="background: #C1E59F; color: #333; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">0-10%</span>
                <span style="background: #EBD5AB; color: #333; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">0 to -10%</span>
                <span style="background: #FF937E; color: white; padding: 2px 8px; border-radius: 4px; margin-right: 8px;">-10 to -30%</span>
                <span style="background: #FF5555; color: white; padding: 2px 8px; border-radius: 4px;">&lt; -30%</span>
            </div>
        </div>
        
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); overflow-x: auto;">
            <div id="heatmap-grid" style="display: grid; grid-template-columns: 60px repeat(12, 1fr); gap: 2px;"></div>
        </div>
    `;
    
    const grid = document.getElementById('heatmap-grid');
    const heatmapData = data.heatmapData;
    
    console.log('Full data received:', data);
    console.log('HeatmapData keys:', Object.keys(heatmapData));
    
    const years = Object.keys(heatmapData).sort((a, b) => b - a);
    
    console.log('Heatmap data years:', years);
    console.log('Total years:', years.length);
    
    // Header row
    const yearHeader = document.createElement('div');
    yearHeader.style.cssText = 'text-align: center; font-size: 11px; font-weight: 600; color: #666; padding: 8px;';
    yearHeader.textContent = 'Year';
    grid.appendChild(yearHeader);
    
    MONTH_NAMES.forEach(month => {
        const monthHeader = document.createElement('div');
        monthHeader.style.cssText = 'text-align: center; font-size: 10px; font-weight: 600; color: #666; padding: 8px;';
        monthHeader.textContent = month;
        grid.appendChild(monthHeader);
    });
    
    // Data rows
    years.forEach(year => {
        const yearCell = document.createElement('div');
        yearCell.style.cssText = 'text-align: center; font-weight: 700; padding: 8px; color: #333;';
        yearCell.textContent = year;
        grid.appendChild(yearCell);
        
        for (let month = 1; month <= 12; month++) {
            const value = heatmapData[year]?.[month.toString()];
            const cell = document.createElement('div');
            cell.style.cssText = `
                padding: 12px 8px;
                text-align: center;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            `;
            
            if (value !== null && value !== undefined) {
                const percentage = value;  // Value is already a percentage from backend
                cell.textContent = (percentage >= 0 ? '+' : '') + percentage.toFixed(1) + '%';
                cell.style.background = getMonthlyReturnColor(percentage);
                cell.style.color = Math.abs(percentage) > 3 ? 'white' : '#333';
            } else {
                cell.textContent = '-';
                cell.style.background = '#f5f5f5';
                cell.style.color = '#999';
            }
            
            cell.addEventListener('mouseenter', () => {
                cell.style.transform = 'scale(1.1)';
                cell.style.zIndex = '10';
            });
            cell.addEventListener('mouseleave', () => {
                cell.style.transform = 'scale(1)';
                cell.style.zIndex = '1';
            });
            
            grid.appendChild(cell);
        }
    });
}

function getMonthlyReturnColor(percentage) {
    // Red shades for negative returns
    if (percentage <= -30) return '#FF5555';  // Bright red (< -30%)
    if (percentage <= -10) return '#FF937E';  // Light red (-30% to -10%)
    if (percentage <= 0) return '#EBD5AB';    // Beige (0% to -10%)
    // Green shades for positive returns
    if (percentage <= 10) return '#C1E59F';   // Light green (0% to 10%)
    if (percentage <= 20) return '#A3D78A';   // Medium green (10% to 20%)
    if (percentage <= 30) return '#8BAE66';   // Forest green (20% to 30%)
    return '#628141';                          // Dark green (> 30%)
}

// Get color class based on metric value and type
function getColorClass(value, type) {
    if (value === null || value === undefined) return '';
    
    const numValue = parseFloat(value);
    
    if (type === 'ret') {
        // Return: Higher is better
        if (numValue >= 20) return 'green-dark';
        if (numValue >= 15) return 'light-green';
        if (numValue >= 10) return 'yellow';
        if (numValue >= 5) return 'orange';
        return 'red';
    } else if (type === 'v1') {
        // V1 (Percentile): Higher is better (1 = best, 0 = worst)
        if (numValue >= 0.8) return 'green-dark';
        if (numValue >= 0.6) return 'light-green';
        if (numValue >= 0.4) return 'yellow';
        if (numValue >= 0.2) return 'orange';
        return 'red';
    } else if (type === 'absmom') {
        // Absolute Momentum: Higher is better (green), lower/negative is worse (red)
        if (numValue >= 30) return 'green-dark';
        if (numValue >= 20) return 'light-green';
        if (numValue >= 10) return 'yellow';
        if (numValue >= 0) return 'orange';
        return 'red';
    } else if (type === 'risk') {
        // Risk (Std * 3.45): Lower is better
        if (numValue <= 35) return 'green-dark';
        if (numValue <= 50) return 'light-green';
        if (numValue <= 65) return 'yellow';
        if (numValue <= 80) return 'orange';
        return 'red';
    } else if (type === 'mom') {
        // Momentum: Higher is better
        if (numValue >= 20) return 'green-dark';
        if (numValue >= 10) return 'light-green';
        if (numValue >= 0) return 'yellow';
        if (numValue >= -10) return 'orange';
        return 'red';
    }
    
    return '';
}

// Render category table
function renderCategoryTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    data.forEach(item => {
        const tr = document.createElement('tr');
        
        // Index name cell
        const nameTd = document.createElement('td');
        nameTd.textContent = item['Index Name'];
        tr.appendChild(nameTd);
        
        // Ret cell
        const retTd = document.createElement('td');
        const retCell = document.createElement('div');
        retCell.className = `metric-cell ${getColorClass(item.Ret, 'ret')}`;
        retCell.textContent = item.Ret;
        retTd.appendChild(retCell);
        tr.appendChild(retTd);
        
        // V1 cell
        const v1Td = document.createElement('td');
        const v1Cell = document.createElement('div');
        v1Cell.className = `metric-cell ${getColorClass(item.V1, 'v1')}`;
        v1Cell.textContent = item.V1 !== null ? item.V1 : '-';
        v1Td.appendChild(v1Cell);
        tr.appendChild(v1Td);
        
        // Risk cell
        const riskTd = document.createElement('td');
        const riskCell = document.createElement('div');
        riskCell.className = `metric-cell ${getColorClass(item.Risk, 'risk')}`;
        riskCell.textContent = item.Risk + '%';
        riskTd.appendChild(riskCell);
        tr.appendChild(riskTd);
        
        // AbsMom cell
        const absMomTd = document.createElement('td');
        const absMomCell = document.createElement('div');
        absMomCell.className = `metric-cell ${getColorClass(item.AbsMom, 'absmom')}`;
        absMomCell.textContent = item.AbsMom !== null ? item.AbsMom : '-';
        absMomTd.appendChild(absMomCell);
        tr.appendChild(absMomTd);
        
        // Momentum cell
        const momTd = document.createElement('td');
        const momCell = document.createElement('div');
        momCell.className = `metric-cell ${getColorClass(item.Momentum, 'mom')}`;
        momCell.textContent = item.Momentum;
        momTd.appendChild(momCell);
        tr.appendChild(momTd);
        
        tbody.appendChild(tr);
    });
}

// Sort table by column
function sortTable(column) {
    // Toggle sort direction if clicking same column
    if (currentSort.column === column) {
        currentSort.ascending = !currentSort.ascending;
    } else {
        currentSort.column = column;
        currentSort.ascending = false; // Start with descending for metrics
        if (column === 'name') currentSort.ascending = true; // Ascending for names
    }
    
    // Sort the data
    const sorted = [...currentData].sort((a, b) => {
        let valA, valB;
        
        if (column === 'name') {
            valA = a['Index Name'];
            valB = b['Index Name'];
            return currentSort.ascending 
                ? valA.localeCompare(valB)
                : valB.localeCompare(valA);
        } else if (column === 'ret') {
            valA = a.Ret;
            valB = b.Ret;
        } else if (column === 'v1') {
            valA = a.V1;
            valB = b.V1;
        } else if (column === 'risk') {
            valA = a.Risk;
            valB = b.Risk;
        } else if (column === 'absmom') {
            valA = a.AbsMom !== null ? a.AbsMom : -999;
            valB = b.AbsMom !== null ? b.AbsMom : -999;
        } else if (column === 'mom') {
            valA = a.Momentum;
            valB = b.Momentum;
        }
        
        return currentSort.ascending 
            ? valA - valB
            : valB - valA;
    });
    
    renderCategoryTable(sorted);
}

window.sortTable = sortTable;

// Function to update heatmap title dynamically
function updateHeatmapTitle() {
    const mode = document.getElementById('return-mode')?.value || 'trailing';
    const timeline = document.getElementById('timeline')?.value || '3';
    const modeText = mode === 'trailing' ? 'Trailing' : 'Rolling';
    const titleText = `${modeText} ${timeline}-Year Returns Heatmap`;
    
    const titleElement = document.querySelector('#heatmap-container h2');
    if (titleElement) {
        titleElement.textContent = titleText;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadHeatmapData();
    
    // Add return mode change listener
    const returnMode = document.getElementById('return-mode');
    if (returnMode) {
        returnMode.addEventListener('change', () => {
            updateHeatmapTitle();
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('heatmap-container').classList.add('hidden');
            loadHeatmapData();
        });
    }
    
    // Add timeline change listener
    const timeline = document.getElementById('timeline');
    if (timeline) {
        timeline.addEventListener('change', () => {
            updateHeatmapTitle();
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('heatmap-container').classList.add('hidden');
            loadHeatmapData();
        });
    }
    
    // Add year filter change listener
    const yearFilter = document.getElementById('year-filter');
    if (yearFilter) {
        yearFilter.addEventListener('change', () => {
            filterHeatmapByYear(yearFilter.value);
        });
    }
});

function filterHeatmapByYear(selectedYear) {
    const allYearRows = document.querySelectorAll('.heatmap-grid > div');
    
    if (selectedYear === 'all') {
        // Show all rows
        allYearRows.forEach(row => {
            row.style.display = '';
        });
    } else {
        // Filter to show only selected year
        const grid = document.querySelector('#heatmap-grid');
        if (!grid) return;
        
        const children = Array.from(grid.children);
        const headerCount = 13; // Year header + 12 month headers
        
        // Show headers
        for (let i = 0; i < headerCount; i++) {
            if (children[i]) children[i].style.display = '';
        }
        
        // Process year rows (each row = 13 cells: 1 year label + 12 months)
        for (let i = headerCount; i < children.length; i += 13) {
            const yearCell = children[i];
            if (yearCell && yearCell.textContent.trim() === selectedYear) {
                // Show this year's row
                for (let j = 0; j < 13; j++) {
                    if (children[i + j]) children[i + j].style.display = '';
                }
            } else {
                // Hide this year's row
                for (let j = 0; j < 13; j++) {
                    if (children[i + j]) children[i + j].style.display = 'none';
                }
            }
        }
    }
}
